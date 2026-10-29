import os

child_pid = os.fork()

if child_pid == 0:
    print(f"Я ребёнок, PID={os.getpid()}, PPID={os.getppid()}")
    os._exit(0)

finished_pid, wait_status = os.wait()
exit_code = os.waitstatus_to_exitcode(wait_status)
print(f"Я родитель, PID={os.getpid()}")
print(f"Ребёнок {finished_pid} завершился с кодом {exit_code}")
