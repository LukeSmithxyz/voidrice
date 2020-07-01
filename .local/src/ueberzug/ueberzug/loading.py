import abc
import queue
import weakref
import os
import threading
import concurrent.futures
import enum

import ueberzug.thread as thread
import ueberzug.pattern as pattern


INDEX_ALPHA_CHANNEL = 3


def load_image(path, upper_bound_size):
    """Loads the image and converts it
    if it doesn't use the RGB or RGBX mode.

    Args:
        path (str): the path of the image file
        upper_bound_size (tuple of (width: int, height: int)):
            the maximal size to load data for

    Returns:
        tuple of (PIL.Image, bool): rgb image, downscaled

    Raises:
        OSError: for unsupported formats
    """
    import PIL.Image
    image = PIL.Image.open(path)
    original_size = image.width, image.height
    downscaled = False
    mask = None

    if upper_bound_size:
        upper_bound_size = tuple(
            min(size for size in size_pair if size > 0)
            for size_pair in zip(upper_bound_size, original_size))
        image.draft(None, upper_bound_size)
        downscaled = (image.width, image.height) < original_size

    image.load()

    if (image.format == 'PNG'
            and image.mode in ('L', 'P')
            and 'transparency' in image.info):
        # Prevent pillow to print the warning
        # 'Palette images with Transparency expressed in bytes should be
        #  converted to RGBA images'
        image = image.convert('RGBA')

    if image.mode == 'RGBA':
        mask = image.split()[INDEX_ALPHA_CHANNEL]

    if image.mode not in ('RGB', 'RGBX'):
        image_rgb = PIL.Image.new(
            "RGB", image.size, color=(255, 255, 255))
        image_rgb.paste(image, mask=mask)
        image = image_rgb

    return image, downscaled


class ImageHolder:
    """Holds the reference of an image.
    It serves as bridge between image loader and image user.
    """
    def __init__(self, path, image=None):
        self.path = path
        self.image = image
        self.waiter = threading.Condition()

    def reveal_image(self, image):
        """Assigns an image to this holder and
        notifies waiting image users about it.

        Args:
            image (PIL.Image): the loaded image
        """
        with self.waiter:
            self.image = image
            self.waiter.notify_all()

    def await_image(self):
        """Waits till an image loader assigns the image
        if it's not already happened.

        Returns:
            PIL.Image: the image assigned to this holder
        """
        if self.image is None:
            with self.waiter:
                if self.image is None:
                    self.waiter.wait()
        return self.image


class PostLoadImageProcessor(metaclass=abc.ABCMeta):
    """Describes the structure used to define callbacks which
    will be invoked after loading an image.
    """
    @abc.abstractmethod
    def on_loaded(self, image):
        """Postprocessor of an loaded image.
        The returned image will be assigned to the image holder.

        Args:
            image (PIL.Image): the loaded image

        Returns:
            PIL.Image:
                the image which will be assigned
                to the image holder of this loading process
        """
        raise NotImplementedError()


class CoverPostLoadImageProcessor(PostLoadImageProcessor):
    """Implementation of PostLoadImageProcessor
    which resizes an image (if possible -> needs to be bigger)
    such that it covers only just a given resolution.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def on_loaded(self, image):
        import PIL.Image
        resize_ratio = max(min(1, self.width / image.width),
                           min(1, self.height / image.height))

        if resize_ratio != 1:
            image = image.resize(
                (int(resize_ratio * image.width),
                 int(resize_ratio * image.height)),
                PIL.Image.ANTIALIAS)

        return image


class ImageLoader(metaclass=abc.ABCMeta):
    """Describes the structure used to define image loading strategies.

    Defines a general interface used to implement different ways
    of loading images.
    E.g. loading images asynchron
    """
    @pattern.LazyConstant
    def PLACEHOLDER():
        """PIL.Image: fallback image for occuring errors"""
        # pylint: disable=no-method-argument,invalid-name
        import PIL.Image
        return PIL.Image.new('RGB', (1, 1))

    @staticmethod
    @abc.abstractmethod
    def get_loader_name():
        """Returns the constant name which is associated to this loader."""
        raise NotImplementedError()

    def __init__(self):
        self.error_handler = None

    @abc.abstractmethod
    def load(self, path, upper_bound_size, post_load_processor=None):
        """Starts the image loading procedure for the passed path.
        How and when an image get's loaded depends on the implementation
        of the used ImageLoader class.

        Args:
            path (str): the path to the image which should be loaded
            upper_bound_size (tuple of (width: int, height: int)):
                the maximal size to load data for
            post_load_processor (PostLoadImageProcessor):
                allows to apply changes to the recently loaded image

        Returns:
            ImageHolder: which the image will be assigned to
        """
        raise NotImplementedError()

    def register_error_handler(self, error_handler):
        """Set's the error handler to the passed function.
        An error handler will be called with exceptions which were
        raised during loading an image.

        Args:
            error_handler (Function(Exception)):
                the function which should be called
                to handle an error
        """
        self.error_handler = error_handler

    def process_error(self, exception):
        """Processes an exception.
        Calls the error_handler with the exception
        if there's any.

        Args:
            exception (Exception): the occurred error
        """
        if (self.error_handler is not None and
                exception is not None):
            self.error_handler(exception)


class SynchronousImageLoader(ImageLoader):
    """Implementation of ImageLoader
    which loads images right away in the same thread
    it was requested to load the image.
    """
    @staticmethod
    def get_loader_name():
        return "synchronous"

    def load(self, path, upper_bound_size, post_load_processor=None):
        image = None

        try:
            image, _ = load_image(path, None)
        except OSError as exception:
            self.process_error(exception)

        if image and post_load_processor:
            image = post_load_processor.on_loaded(image)

        return ImageHolder(path, image or self.PLACEHOLDER)


class AsynchronousImageLoader(ImageLoader):
    """Extension of ImageLoader
    which adds basic functionality
    needed to implement asynchron image loading.
    """
    @enum.unique
    class Priority(enum.Enum):
        """Enum which defines the possible priorities
        of queue entries.
        """
        HIGH = enum.auto()
        LOW = enum.auto()

    def __init__(self):
        super().__init__()
        self.__queue = queue.Queue()
        self.__queue_low_priority = queue.Queue()
        self.__waiter_low_priority = threading.Condition()

    def _enqueue(self, queue, image_holder, upper_bound_size, post_load_processor):
        """Enqueues the image holder weakly referenced.

        Args:
            queue (queue.Queue): the queue to operate on
            image_holder (ImageHolder):
                the image holder for which an image should be loaded
            upper_bound_size (tuple of (width: int, height: int)):
                the maximal size to load data for
            post_load_processor (PostLoadImageProcessor):
                allows to apply changes to the recently loaded image
        """
        queue.put((
            weakref.ref(image_holder), upper_bound_size, post_load_processor))

    def _dequeue(self, queue):
        """Removes queue entries till an alive reference was found.
        The referenced image holder will be returned in this case.
        Otherwise if there wasn't found any alive reference
        None will be returned.

        Args:
            queue (queue.Queue): the queue to operate on

        Returns:
            tuple of (ImageHolder, tuple of (width: int, height: int),
                      PostLoadImageProcessor):
                an queued image holder or None, upper bound size or None,
                the post load image processor or None
        """
        holder_reference = None
        image_holder = None
        upper_bound_size = None
        post_load_processor = None

        while not queue.empty():
            holder_reference, upper_bound_size, post_load_processor = \
                queue.get_nowait()
            image_holder = holder_reference and holder_reference()
            if (holder_reference is None or
                    image_holder is not None):
                break

        return image_holder, upper_bound_size, post_load_processor

    @abc.abstractmethod
    def _schedule(self, function, priority):
        """Schedules the execution of a function.
        Functions should be executed in different thread pools
        based on their priority otherwise you can wait for a death lock.

        Args:
            function (Function): the function which should be executed
            priority (AsynchronImageLoader.Priority):
                the priority of the execution of this function
        """
        raise NotImplementedError()

    def _load_image(self, path, upper_bound_size, post_load_processor):
        """Wrapper for calling load_image.
        Behaves like calling it directly,
        but allows e.g. executing the function in other processes.
        """
        image, *other_data = load_image(path, upper_bound_size)

        if image and post_load_processor:
            image = post_load_processor.on_loaded(image)

        return (image, *other_data)

    def load(self, path, upper_bound_size, post_load_processor=None):
        holder = ImageHolder(path)
        self._enqueue(
            self.__queue, holder, upper_bound_size, post_load_processor)
        self._schedule(self.__process_high_priority_entry,
                       self.Priority.HIGH)
        return holder

    def __wait_for_main_work(self):
        """Waits till all queued high priority entries were processed."""
        if not self.__queue.empty():
            with self.__waiter_low_priority:
                if not self.__queue.empty():
                    self.__waiter_low_priority.wait()

    def __notify_main_work_done(self):
        """Notifies waiting threads that
        all queued high priority entries were processed.
        """
        if self.__queue.empty():
            with self.__waiter_low_priority:
                if self.__queue.empty():
                    self.__waiter_low_priority.notify_all()

    def __process_high_priority_entry(self):
        """Processes a single queued high priority entry."""
        self.__process_queue(self.__queue)
        self.__notify_main_work_done()

    def __process_low_priority_entry(self):
        """Processes a single queued low priority entry."""
        self.__wait_for_main_work()
        self.__process_queue(self.__queue_low_priority)

    def __process_queue(self, queue):
        """Processes a single queued entry.

        Args:
            queue (queue.Queue): the queue to operate on
        """
        image = None
        image_holder, upper_bound_size, post_load_processor = \
            self._dequeue(queue)
        if image_holder is None:
            return

        try:
            image, downscaled = self._load_image(
                image_holder.path, upper_bound_size, post_load_processor)
            if upper_bound_size and downscaled:
                self._enqueue(
                    self.__queue_low_priority,
                    image_holder, None, post_load_processor)
                self._schedule(self.__process_low_priority_entry,
                               self.Priority.LOW)
        except OSError as exception:
            self.process_error(exception)
        finally:
            image_holder.reveal_image(image or self.PLACEHOLDER)


# * Pythons GIL limits the usefulness of threads.
# So in order to use all cpu cores (assumed GIL isn't released)
# you need to use multiple processes.
# * Pillows load method will read & decode the image.
# So it does the I/O and CPU work.
# Decoding seems to be the bottleneck for large images.
# * Using multiple processes comes with it's own bottleneck
# (transfering the data between the processes).
#
# => Using multiple processes seems to be faster for small images.
#    Using threads seems to be faster for large images.
class ThreadImageLoader(AsynchronousImageLoader):
    """Implementation of AsynchronImageLoader
    which loads images in multiple threads.
    """
    @staticmethod
    def get_loader_name():
        return "thread"

    def __init__(self):
        super().__init__()
        threads = os.cpu_count()
        threads_low_priority = max(1, threads // 2)
        self.__executor = thread.DaemonThreadPoolExecutor(
            max_workers=threads)
        self.__executor_low_priority = thread.DaemonThreadPoolExecutor(
            max_workers=threads_low_priority)
        self.threads = threads + threads_low_priority

    def _schedule(self, function, priority):
        executor = self.__executor
        if priority == self.Priority.LOW:
            executor = self.__executor_low_priority
        executor.submit(function) \
            .add_done_callback(
                lambda future: self.process_error(future.exception()))


class ProcessImageLoader(ThreadImageLoader):
    """Implementation of AsynchronImageLoader
    which loads images in multiple processes.
    Therefore it allows to utilise all cpu cores
    for decoding an image.
    """
    @staticmethod
    def get_loader_name():
        return "process"

    def __init__(self):
        super().__init__()
        self.__executor_loader = concurrent.futures.ProcessPoolExecutor(
            max_workers=self.threads)
        # ProcessPoolExecutor won't work
        # when used first in ThreadPoolExecutor
        self.__executor_loader \
            .submit(id, id) \
            .result()

    @staticmethod
    def _load_image_extern(path, upper_bound_size, post_load_processor):
        """This function is a wrapper for the image loading function
        as sometimes pillow restores decoded images
        received from other processes wrongly.
        E.g. a PNG is reported as webp (-> crash on using an image function)
        So this function is a workaround which prevents these crashs to happen.
        """
        image, *other_data = load_image(path, upper_bound_size)

        if image and post_load_processor:
            image = post_load_processor.on_loaded(image)

        return (image.mode, image.size, image.tobytes(), *other_data)

    def _load_image(self, path, upper_bound_size, post_load_processor=None):
        import PIL.Image
        future = self.__executor_loader.submit(
            ProcessImageLoader._load_image_extern,
            path, upper_bound_size, post_load_processor)
        mode, size, data, downscaled = future.result()
        return PIL.Image.frombytes(mode, size, data), downscaled


@enum.unique
class ImageLoaderOption(str, enum.Enum):
    """Enum which lists the useable ImageLoader classes."""
    SYNCHRONOUS = SynchronousImageLoader
    THREAD = ThreadImageLoader
    PROCESS = ProcessImageLoader

    def __new__(cls, loader_class):
        inst = str.__new__(cls)
        # Based on an official example
        # https://docs.python.org/3/library/enum.html#using-a-custom-new
        # So.. stfu pylint
        # pylint: disable=protected-access
        inst._value_ = loader_class.get_loader_name()
        inst.loader_class = loader_class
        return inst
