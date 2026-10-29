from collections import deque
from dataclasses import dataclass
import sys


@dataclass
class Process:
    pid: str
    arrival: int
    burst: int
    priority: int


def read_processes(filename):
    """Load process records from a whitespace-separated input file."""
    loaded = []
    with open(filename, encoding="utf-8") as source:
        for raw_line in source:
            record = raw_line.strip()
            if not record or record.startswith("#"):
                continue
            pid, arrival, burst, priority = record.split()
            loaded.append(Process(pid, int(arrival), int(burst), int(priority)))
    return loaded


def fcfs(processes):
    """First Come, First Served: run jobs in arrival order."""
    clock = 0
    timeline = []
    for process in sorted(processes, key=lambda item: item.arrival):
        begin = max(clock, process.arrival)
        finish = begin + process.burst
        timeline.append((process.pid, begin, finish))
        clock = finish
    return timeline


def sjf(processes):
    """Non-preemptive Shortest Job First scheduling."""
    clock = 0
    pending = list(enumerate(processes))
    timeline = []

    while pending:
        ready = [(idx, proc) for idx, proc in pending if proc.arrival <= clock]
        if not ready:
            clock = min(proc.arrival for _, proc in pending)
            ready = [(idx, proc) for idx, proc in pending if proc.arrival <= clock]

        chosen_idx, chosen = min(ready, key=lambda pair: (pair[1].burst, pair[0]))
        finish = clock + chosen.burst
        timeline.append((chosen.pid, clock, finish))
        clock = finish
        pending = [(idx, proc) for idx, proc in pending if idx != chosen_idx]

    return timeline


def rr(processes, quantum):
    """Round Robin scheduling using a fixed time quantum."""
    if quantum <= 0:
        raise ValueError("Квант времени должен быть больше нуля")

    arrival_order = sorted(enumerate(processes), key=lambda pair: pair[1].arrival)
    time_left = {idx: proc.burst for idx, proc in arrival_order}
    ready_queue = deque()
    timeline = []
    clock = 0
    next_job = 0

    while next_job < len(arrival_order) or ready_queue:
        if not ready_queue and next_job < len(arrival_order):
            clock = max(clock, arrival_order[next_job][1].arrival)

        while next_job < len(arrival_order) and arrival_order[next_job][1].arrival <= clock:
            ready_queue.append(arrival_order[next_job][0])
            next_job += 1

        if not ready_queue:
            continue

        idx = ready_queue.popleft()
        process = processes[idx]
        begin = clock
        elapsed = min(quantum, time_left[idx])
        clock += elapsed
        time_left[idx] -= elapsed
        timeline.append((process.pid, begin, clock))

        while next_job < len(arrival_order) and arrival_order[next_job][1].arrival <= clock:
            ready_queue.append(arrival_order[next_job][0])
            next_job += 1

        if time_left[idx] > 0:
            ready_queue.append(idx)

    return timeline


def calculate_metrics(processes, timeline):
    """Return average waiting time and average turnaround time."""
    finished_at = {pid: finish for pid, _begin, finish in timeline}
    waiting = []
    turnaround = []
    for process in processes:
        total_turnaround = finished_at[process.pid] - process.arrival
        turnaround.append(total_turnaround)
        waiting.append(total_turnaround - process.burst)
    return sum(waiting) / len(processes), sum(turnaround) / len(processes)


def show_gantt(timeline):
    print("Диаграмма Ганта:")
    if not timeline:
        print("(нет процессов)")
        return
    labels = [f"{pid}[{begin}-{finish}]" for pid, begin, finish in timeline]
    print(" -> ".join(labels))


def main():
    if len(sys.argv) < 2:
        print("Использование: python3 scheduler.py set1.txt [quantum]")
        sys.exit(1)

    filename = sys.argv[1]
    quantum = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    try:
        processes = read_processes(filename)
        if not processes:
            print("Ошибка: файл не содержит процессов.")
            sys.exit(1)

        methods = [
            ("FCFS", fcfs),
            ("SJF", sjf),
            ("RR", lambda jobs: rr(jobs, quantum)),
        ]
        print(f"Файл: {filename}")
        print(f"Квант RR: {quantum}")
        for title, method in methods:
            timeline = method(processes)
            avg_wait, avg_turnaround = calculate_metrics(processes, timeline)
            print(f"\n=== {title} ===")
            show_gantt(timeline)
            print(f"Среднее время ожидания: {avg_wait:.2f}")
            print(f"Среднее время turnaround: {avg_turnaround:.2f}")
    except FileNotFoundError:
        print(f"Ошибка: файл '{filename}' не найден.")
        sys.exit(1)
    except ValueError as error:
        print(f"Ошибка: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
