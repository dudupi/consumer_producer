from threading import Thread, Semaphore
import time
import random


class ConsumerProducer(object):
    def __init__(self):
        self.nums = range(5)
        self.queue = []
        self.max_num = 5
        self.empty = Semaphore(self.max_num)
        self.fill = Semaphore(0)

    def add(self):
        self.empty.acquire()
        self.queue.append(random.choice(self.nums))
        print("Produced", self.queue)
        self.fill.release()
        time.sleep(random.random())

    def remove(self):
        self.fill.acquire()
        self.queue.pop()
        print("Consumed", self.queue)
        self.empty.release()
        time.sleep(random.random())


q = ConsumerProducer()


class ProducerThread(Thread):
    def run(self):
        while True:
            q.add()


class ConsumerThread(Thread):
    def run(self):
        while True:
            q.remove()


ProducerThread().start()
ConsumerThread().start()
