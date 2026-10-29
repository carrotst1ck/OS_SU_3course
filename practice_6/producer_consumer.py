import queue
import threading
import time

QUEUE_CAPACITY = 5
STOP_SIGNAL = None
work_queue = queue.Queue(maxsize=QUEUE_CAPACITY)


def produce_items():
    for value in range(10):
        work_queue.put(value)
        print(f"Produced: {value}")
        time.sleep(0.1)
    work_queue.put(STOP_SIGNAL)


def consume_items():
    while True:
        value = work_queue.get()
        try:
            if value is STOP_SIGNAL:
                break
            print(f"Consumed: {value}")
            time.sleep(0.2)
        finally:
            work_queue.task_done()


consumer_thread = threading.Thread(target=consume_items)
producer_thread = threading.Thread(target=produce_items)
consumer_thread.start()
producer_thread.start()
producer_thread.join()
work_queue.join()
consumer_thread.join()
print("Finished!")
