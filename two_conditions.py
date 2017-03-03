from threading import Thread, Condition, Lock
import time
import random


class ConsumerProducer(object):
    def __init__(self):
        self.nums = range(5)
        self.queue = []
        lock = Lock()
        self.empty = Condition(lock)
        self.full = Condition(lock)
        self.max_num = 10

    def add(self):
        with self.full:
            if len(self.queue) == self.max_num:
                print("Queue full, producer is waiting")
                self.full.wait()
                print("Space in queue, Consumer notified the producer")
            self.queue.append(random.choice(self.nums))
            print("Produced", self.queue)
            if len(self.queue) == 1:
                self.empty.notify()
        time.sleep(random.random())

    def remove(self):
        with self.empty:
            if not self.queue:
                print("Nothing in queue, consumer is waiting")
                self.empty.wait()
                print("Producer added something to queue and notified the consumer")
            self.queue.pop(0)
            print("Consumed", self.queue)
            if len(self.queue) == (self.max_num - 1):
                self.full.notify()
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
