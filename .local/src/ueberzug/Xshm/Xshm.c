#define PY_SSIZE_T_CLEAN  // Make "s#" use Py_ssize_t rather than int.
#include <Python.h>
#include <stdbool.h>
#include <sys/shm.h>
#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <X11/extensions/XShm.h>

#define INVALID_SHM_ID -1
#define INVALID_SHM_ADDRESS (char*)-1
#define BYTES_PER_PIXEL 4

#define min(a,b) (((a) < (b)) ? (a) : (b))
#define max(a,b) (((a) > (b)) ? (a) : (b))

#define Py_INIT_ERROR -1
#define Py_INIT_SUCCESS 0

#define __raise(return_value, Exception, message...) { \
    char errorMessage[500]; \
    snprintf(errorMessage, 500, message); \
    PyErr_SetString( \
        PyExc_##Exception, \
        errorMessage); \
    return return_value; \
}
#define raise(Exception, message...) __raise(NULL, Exception, message)
#define raiseInit(Exception, message...) __raise(Py_INIT_ERROR, Exception, message)


static Display* display = NULL;

typedef struct {
    PyObject_HEAD
    int width;
    int height;
    int buffer_size;
    XShmSegmentInfo segmentInfo;
    XImage *image;
} Image;

static bool
init_display() {
    if (display == NULL) {
        display = XOpenDisplay(NULL);
        if (display == NULL) {
            return false;
        }
    }

    return true;
}

static bool
Image_init_shared_memory(Image *self) {
    self->segmentInfo.shmid = shmget(
        IPC_PRIVATE,
        self->buffer_size,
        IPC_CREAT | 0600);
    return self->segmentInfo.shmid != INVALID_SHM_ID;
}

static bool
Image_map_shared_memory(Image *self) {
    // Map the shared memory segment into the address space of this process
    self->segmentInfo.shmaddr = (char*)shmat(self->segmentInfo.shmid, 0, 0);

    if (self->segmentInfo.shmaddr != INVALID_SHM_ADDRESS) {
        self->segmentInfo.readOnly = true;
        // Mark the shared memory segment for removal
        // It will be removed even if this program crashes
        shmctl(self->segmentInfo.shmid, IPC_RMID, 0);
        return true;
    }

    return false;
}

static bool
Image_create_shared_image(Image *self) {
    int screen = XDefaultScreen(display);
    // Allocate the memory needed for the XImage structure
    self->image = XShmCreateImage(
        display, XDefaultVisual(display, screen),
        DefaultDepth(display, screen), ZPixmap, 0,
        &self->segmentInfo, 0, 0);

    if (self->image) {
        self->image->data = (char*)self->segmentInfo.shmaddr;
        self->image->width = self->width;
        self->image->height = self->height;

        // Ask the X server to attach the shared memory segment and sync
        XShmAttach(display, &self->segmentInfo);
        XSync(display, false);
        return true;
    }
    return false;
}

static void
Image_destroy_shared_image(Image *self) {
    if (self->image) {
        XShmDetach(display, &self->segmentInfo);
        XDestroyImage(self->image);
        self->image = NULL;
    }
}

static void
Image_free_shared_memory(Image *self) {
    if(self->segmentInfo.shmaddr != INVALID_SHM_ADDRESS) {
        shmdt(self->segmentInfo.shmaddr);
        self->segmentInfo.shmaddr = INVALID_SHM_ADDRESS;
    }
}

static int
Image_init(Image *self, PyObject *args, PyObject *kwds) {
    static char *kwlist[] = {"width", "height", NULL};
    if (!PyArg_ParseTupleAndKeywords(
            args, kwds, "ii", kwlist,
            &self->width, &self->height)) {
        return Py_INIT_ERROR;
    }

    self->buffer_size = self->width * self->height * BYTES_PER_PIXEL;

    if (!init_display()) {
        raiseInit(OSError, "could not open a connection to the X server");
    }
    
    if (!Image_init_shared_memory(self)) {
        raiseInit(OSError, "could not init shared memory");
    }

    if (!Image_map_shared_memory(self)) {
        raiseInit(OSError, "could not map shared memory");
    }

    if (!Image_create_shared_image(self)) {
        Image_free_shared_memory(self);
        raiseInit(OSError, "could not allocate the XImage structure");
    }
    
    return Py_INIT_SUCCESS;
}

static void
Image_dealloc(Image *self) {
    Image_destroy_shared_image(self);
    Image_free_shared_memory(self);
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject *
Image_copyTo(Image *self, PyObject *args, PyObject *kwds) {
    // draws the image on the surface at x, y
    static char *kwlist[] = {"drawable", "x", "y", "width", "height", NULL};
    Drawable surface;
    GC gc;
    int x, y;
    int width, height;

    if (!PyArg_ParseTupleAndKeywords(
            args, kwds, "liiii", kwlist,
            &surface, &x, &y, &width, &height)) {
        return NULL;
    }

    gc = XCreateGC(display, surface, 0, NULL);
    XShmPutImage(display, surface, gc,
                 self->image, 0, 0,
                 x, y, width, height, False);
    XFreeGC(display, gc);
    XSync(display, false);

    Py_RETURN_NONE;
}

static PyObject *
Image_draw(Image *self, PyObject *args, PyObject *kwds) {
    // puts the pixels on the image at x, y
    static char *kwlist[] = {"x", "y", "width", "height", "pixels", NULL};
    int offset_x, offset_y;
    int width, height;
    int pixels_per_row;
    int source_pixels_per_row;
    int destination_pixels_per_row;
    int destination_offset_x_bytes;
    char *pixels;
    Py_ssize_t pixels_size;

    if (!PyArg_ParseTupleAndKeywords(
            args, kwds, "iiiis#", kwlist,
            &offset_x, &offset_y, &width, &height,
            &pixels, &pixels_size)) {
        return NULL;
    }

    destination_offset_x_bytes = max(0, offset_x) * BYTES_PER_PIXEL;
    source_pixels_per_row = width * BYTES_PER_PIXEL;
    destination_pixels_per_row = self->width * BYTES_PER_PIXEL;
    pixels_per_row = min(width + min(offset_x, 0), self->width - max(offset_x, 0)) * BYTES_PER_PIXEL;

    if (offset_x + width > 0 && offset_x < self->width) {
        // < 0 -> start y = 0, min(surface.height, height - abs(offset))
        // > 0 -> start y = offset, height = min(surface.height, height + offset)
        for (int y = max(0, offset_y); y < min(self->height, height + offset_y); y++) {
            // < 0 -> first row = abs(offset) => n row = y + abs(offset)
            // > 0 -> first row = - offset    => n row = y - offset
            // => n row = y - offset
            int pixels_y = y - offset_y;
            void *destination =
                self->image->data + y * destination_pixels_per_row
                + destination_offset_x_bytes;
            void *source = pixels + pixels_y * source_pixels_per_row;

            if (! ((uintptr_t)self->image->data <= (uintptr_t)destination)) {
                raise(AssertionError,
                      "The destination start address calculation went wrong.\n"
                      "It points to an address which is before the start address of the buffer.\n"
                      "%p not smaller than %p",
                      self->image->data, destination);
            }
            if (! ((uintptr_t)destination + pixels_per_row
                   <= (uintptr_t)self->image->data + self->buffer_size)) {
                raise(AssertionError,
                      "The destination end address calculation went wrong.\n"
                      "It points to an address which is after the end address of the buffer.\n"
                      "%p not smaller than %p",
                      destination + pixels_per_row,
                      self->image->data + self->buffer_size);
            }
            if (! ((uintptr_t)pixels <= (uintptr_t)source)) {
                raise(AssertionError,
                      "The source start address calculation went wrong.\n"
                      "It points to an address which is before the start address of the buffer.\n"
                      "%p not smaller than %p",
                      pixels, source);
            }
            if (! ((uintptr_t)source + pixels_per_row
                   <= (uintptr_t)pixels + pixels_size)) {
                raise(AssertionError,
                      "The source end address calculation went wrong.\n"
                      "It points to an address which is after the end address of the buffer."
                      "%p not smaller than %p",
                      source + pixels_per_row,
                      pixels + pixels_size);
            }

            memcpy(destination, source, pixels_per_row);
        }
    }

    Py_RETURN_NONE;
}

static PyMethodDef Image_methods[] = {
    {"copy_to", (PyCFunction)Image_copyTo,
     METH_VARARGS | METH_KEYWORDS,
     "Draws the image on the surface at the passed coordinate.\n"
     "\n"
     "Args:\n"
     "    drawable (int): the surface to draw on\n"
     "    x (int): the x position where this image should be placed\n"
     "    y (int): the y position where this image should be placed\n"
     "    width (int): the width of the area\n"
     "                 which should be copied to the drawable\n"
     "    height (int): the height of the area\n"
     "                  which should be copied to the drawable"},
    {"draw", (PyCFunction)Image_draw,
     METH_VARARGS | METH_KEYWORDS,
     "Places the pixels on the image at the passed coordinate.\n"
     "\n"
     "Args:\n"
     "    x (int): the x position where the pixels should be placed\n"
     "    y (int): the y position where the pixels should be placed\n"
     "    width (int): amount of pixels per row in the passed data\n"
     "    height (int): amount of pixels per column in the passed data\n"
     "    pixels (bytes): the pixels to place on the image"},
    {NULL}  /* Sentinel */
};

static PyTypeObject ImageType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "Xshm.Image",
    .tp_doc = 
        "An shared memory X11 Image\n"
        "\n"
        "Args:\n"
        "    width (int): the width of this image\n"
        "    height (int): the height of this image",
    .tp_basicsize = sizeof(Image),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_new = PyType_GenericNew,
    .tp_init = (initproc)Image_init,
    .tp_dealloc = (destructor) Image_dealloc,
    .tp_methods = Image_methods,
};

static PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    .m_name = "Xshm",
    .m_doc = "Modul which implements the interaction with the Xshm extension.",
    .m_size = -1,
};

PyMODINIT_FUNC
PyInit_Xshm(void) {
    PyObject *module_instance;
    if (PyType_Ready(&ImageType) < 0)
        return NULL;

    module_instance = PyModule_Create(&module);
    if (module_instance == NULL)
        return NULL;

    Py_INCREF(&ImageType);
    PyModule_AddObject(module_instance, "Image", (PyObject*)&ImageType);
    return module_instance;
}
