import threading

account_a = 1000
account_b = 1000
balance_lock = threading.Lock()
starting_total = account_a + account_b
iterations = 100_000


def transfer_between(source, destination, amount):
    global account_a, account_b
    for _ in range(iterations):
        with balance_lock:
            if source == "A":
                account_a -= amount
            else:
                account_b -= amount
            if destination == "A":
                account_a += amount
            else:
                account_b += amount


workers = [
    threading.Thread(target=transfer_between, args=("A", "B", 1)),
    threading.Thread(target=transfer_between, args=("B", "A", 1)),
]
for worker in workers:
    worker.start()
for worker in workers:
    worker.join()

current_total = account_a + account_b
print("Account A:", account_a)
print("Account B:", account_b)
print("Total:", current_total)
assert current_total == starting_total
print("Total balance is correct!")
