"""This module reimplements the ThreadPoolExecutor.
https://github.com/python/cpython/blob/master/Lib/concurrent/futures/thread.py

The only change is the prevention of waiting
for each thread to exit on exiting the script.
"""
import threading
import weakref
import concurrent.futures as futures


def _worker(executor_reference, work_queue):
    # pylint: disable=W0212
    try:
        while True:
            work_item = work_queue.get(block=True)
            if work_item is not None:
                work_item.run()
                del work_item
                continue
            executor = executor_reference()
            if executor is None or executor._shutdown:
                if executor is not None:
                    executor._shutdown = True
                work_queue.put(None)
                return
            del executor
    except BaseException:
        futures._base.LOGGER.critical('Exception in worker', exc_info=True)


class DaemonThreadPoolExecutor(futures.ThreadPoolExecutor):
    """The concurrent.futures.ThreadPoolExecutor extended by
    the prevention of waiting for each thread on exiting the script.
    """

    def _adjust_thread_count(self):
        def weakref_cb(_, queue=self._work_queue):
            queue.put(None)
        num_threads = len(self._threads)
        if num_threads < self._max_workers:
            thread_name = '%s_%d' % (self, num_threads)
            thread = threading.Thread(name=thread_name, target=_worker,
                                      args=(weakref.ref(self, weakref_cb),
                                            self._work_queue))
            thread.daemon = True
            thread.start()
            self._threads.add(thread)
