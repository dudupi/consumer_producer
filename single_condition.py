from threading import Thread, Condition
import time
import random


class ConsumerProducer(object):
    def __init__(self):
        self.nums = range(5)
        self.queue = []
        self.condition = Condition()
        self.max_num = 10

    def add(self):
        with self.condition:
            if len(self.queue) == self.max_num:
                print("Queue full, producer is waiting")
                self.condition.wait()
                print("Space in queue, Consumer notified the producer")
            self.queue.append(random.choice(self.nums))
            print("Produced", self.queue)
            self.condition.notify()
        time.sleep(random.random())

    def remove(self):
        with self.condition:
            if not self.queue:
                print("Nothing in queue, consumer is waiting")
                self.condition.wait()
                print("Producer added something to queue and notified the consumer")
            self.queue.pop(0)
            print("Consumed", self.queue)
            self.condition.notify()
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
