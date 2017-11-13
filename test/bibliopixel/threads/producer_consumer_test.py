import random, threading, time, unittest

from bibliopixel.util.threads import producer_consumer


class ProducerConsumerTest(unittest.TestCase):
    def test_all(self):
        buffer = producer_consumer.Queues([], [])

        counter = [0]

        def producer():
            for i in range(10):
                time.sleep(random.uniform(0.001, 0.020))
                with buffer.produce() as i:
                    i[:] = counter
                    counter[0] += 1
        producer_thread = threading.Thread(target=producer)

        result = []

        def consumer():
            for i in range(10):
                time.sleep(random.uniform(0.003, 0.010))
                with buffer.consume() as o:
                    result.extend(o)
        consumer_thread = threading.Thread(target=consumer)

        producer_thread.start()
        consumer_thread.start()

        producer_thread.join()
        consumer_thread.join()

        self.assertEqual(result, list(range(10)))
