/* cc transient.c -o transient -lX11 */

#include <stdlib.h>
#include <unistd.h>
#include <X11/Xlib.h>
#include <X11/Xutil.h>

int main(void) {
	Display *d;
	Window r, f, t = None;
	XSizeHints h;
	XEvent e;

	d = XOpenDisplay(NULL);
	if (!d)
		exit(1);
	r = DefaultRootWindow(d);

	f = XCreateSimpleWindow(d, r, 100, 100, 400, 400, 0, 0, 0);
	h.min_width = h.max_width = h.min_height = h.max_height = 400;
	h.flags = PMinSize | PMaxSize;
	XSetWMNormalHints(d, f, &h);
	XStoreName(d, f, "floating");
	XMapWindow(d, f);

	XSelectInput(d, f, ExposureMask);
	while (1) {
		XNextEvent(d, &e);

		if (t == None) {
			sleep(5);
			t = XCreateSimpleWindow(d, r, 50, 50, 100, 100, 0, 0, 0);
			XSetTransientForHint(d, t, f);
			XStoreName(d, t, "transient");
			XMapWindow(d, t);
			XSelectInput(d, t, ExposureMask);
		}
	}

	XCloseDisplay(d);
	exit(0);
}
