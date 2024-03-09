# Copyright (C) 2024 Ethan Uppal. All rights reserved.
# Timer library in pygame for Makeathon 2024.

from queue import Queue
import time


class TimedQueue:
    def __init__(self, delay):
        self.delay = delay
        self.queue = Queue()

    def enqueue(self, callback):
        self.queue.put((callback, time.time()))

    def handle_requests(self):
        if not self.queue.empty():
            callback, queue_time = self.queue.queue[0]
            if time.time() - queue_time >= self.delay:
                self.queue.get()
                callback(self)
