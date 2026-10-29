import os
import time

child_pid = os.fork()

if child_pid == 0:
    os._exit(0)

print(f"PID родителя: {os.getpid()}")
print(f"PID ребёнка: {child_pid}")
print("Родитель ждёт 60 секунд, не вызывая wait()")
time.sleep(60)
os.wait()
