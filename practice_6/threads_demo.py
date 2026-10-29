import threading
import time

INCREMENTS_PER_THREAD = 100_000
WORKER_COUNT = 4
counter = 0
counter_lock = threading.Lock()


def add_repeatedly(synchronize):
    global counter
    for _ in range(INCREMENTS_PER_THREAD):
        if synchronize:
            with counter_lock:
                counter += 1
        else:
            counter += 1


def benchmark(synchronize):
    global counter
    counter = 0
    workers = [
        threading.Thread(target=add_repeatedly, args=(synchronize,))
        for _ in range(WORKER_COUNT)
    ]
    started = time.perf_counter()
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()
    duration = time.perf_counter() - started

    print(f"Lock: {synchronize}")
    print(f"Counter: {counter}")
    print(f"Time: {duration:.4f} seconds")
    if synchronize:
        assert counter == 400_000
        print("Correct result: 400000")
    print()


if __name__ == "__main__":
    benchmark(False)
    benchmark(True)
