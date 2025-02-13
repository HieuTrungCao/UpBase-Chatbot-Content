import threading
import queue

class SingletonQueue:
    """
    A singleton queue class, ensuring only one instance exists.
    """
    __instance = None
    __lock = threading.Lock()

    def __init__(self):
        if SingletonQueue.__instance is not None:
            raise Exception("Singleton can only be instantiated once!")
        self.queue = queue.Queue()

    @staticmethod
    def get_instance():
        """
        Returns the single instance of the SingletonQueue.
        Creates it if it doesn't exist.
        """
        with SingletonQueue.__lock:
            if SingletonQueue.__instance is None:
                SingletonQueue.__instance = SingletonQueue()
            return SingletonQueue.__instance

    def put(self, item):
        """Puts an item into the queue."""
        self.queue.put(item)

    def get(self, block=True, timeout=None):
        """Gets an item from the queue."""
        return self.queue.get(block, timeout)

    def qsize(self):
        """Returns the size of the queue."""
        return self.queue.qsize()

    def empty(self):
        """Checks if the queue is empty."""
        return self.queue.empty()

    def full(self):
        """Checks if the queue is full."""
        return self.queue.full()

    def put_nowait(self, item):
       """Puts an item into the queue without waiting."""
       self.queue.put_nowait(item)

    def get_nowait(self):
       """Gets an item from the queue without waiting."""
       return self.queue.get_nowait()