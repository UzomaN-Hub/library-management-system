"""Times the chosen algorithms against the alternatives at growing data sizes.

Run from the project folder with:  python -m benchmarks.benchmark
Results are printed and saved to benchmarks/results.md for the report.
"""

import bisect
import random
import time
from pathlib import Path

from library.hash_table import HashTable
from library.min_heap import MinHeap
from library.queue import Queue
from library.searching import binary_search, linear_search
from library.sorting import bubble_sort, merge_sort

SIZES = [1_000, 10_000, 100_000, 1_000_000]
BUBBLE_SIZES = [100, 1_000, 5_000]  # bubble sort is too slow beyond this
LOOKUPS = 1_000
RESULTS_FILE = Path(__file__).parent / "results.md"


def timed(function, *args):
    start = time.perf_counter()
    function(*args)
    return time.perf_counter() - start


def ms(seconds):
    return f"{seconds * 1000:,.2f} ms"


def us(seconds):
    return f"{seconds * 1_000_000:,.2f} µs"


# ----- benchmarks -----

def lookup_benchmark():
    rows = []
    for size in SIZES:
        keys = [f"ISBN{n:013d}" for n in range(size)]
        table = HashTable()
        for key in keys:
            table.put(key, key)
        targets = random.sample(keys, LOOKUPS)

        hash_time = timed(lambda: [table.get(k) for k in targets])
        linear_targets = targets[:20]  # linear search is slow, so use fewer
        linear_time = timed(lambda: [linear_search(keys, k) for k in linear_targets])
        linear_per_lookup = linear_time / len(linear_targets)
        rows.append((size, us(hash_time / LOOKUPS), us(linear_per_lookup)))
    return ("Find one book by ISBN (time per lookup)",
            ["Books", "Hash table", "Linear search"], rows)


def sort_benchmark():
    rows = []
    for size in sorted(set(SIZES + BUBBLE_SIZES)):
        values = [random.randint(0, 10_000_000) for _ in range(size)]
        merge_time = timed(merge_sort, values)
        bubble_time = ms(timed(bubble_sort, values)) if size in BUBBLE_SIZES else "not run (too slow)"
        rows.append((size, ms(merge_time), bubble_time))
    return ("Sort all books", ["Books", "Merge sort", "Bubble sort"], rows)


def search_benchmark():
    rows = []
    for size in SIZES:
        values = list(range(size))
        targets = [random.randrange(size) for _ in range(LOOKUPS)]
        binary_time = timed(lambda: [binary_search(values, t) for t in targets])
        linear_targets = targets[:20]
        linear_time = timed(lambda: [linear_search(values, t) for t in linear_targets])
        rows.append((size, us(binary_time / LOOKUPS), us(linear_time / len(linear_targets))))
    return ("Find one book by title in a sorted list (time per search)",
            ["Books", "Binary search", "Linear search"], rows)


def queue_benchmark():
    rows = []
    for size in [1_000, 10_000, 100_000]:
        def use_linked_queue():
            queue = Queue()
            for n in range(size):
                queue.enqueue(n)
            while not queue.is_empty():
                queue.dequeue()

        def use_python_list():
            items = []
            for n in range(size):
                items.append(n)
            while items:
                items.pop(0)

        rows.append((size, ms(timed(use_linked_queue)), ms(timed(use_python_list))))
    return ("Add then serve every reservation",
            ["Reservations", "Linked-list queue", "Python list pop(0)"], rows)


def heap_benchmark():
    rows = []
    for size in [1_000, 10_000, 100_000]:
        due_days = [random.randint(0, 365) for _ in range(size)]

        def use_heap():
            heap = MinHeap()
            for day in due_days:
                heap.push(day, day)
            while not heap.is_empty():
                heap.pop()

        def use_sorted_list():
            items = []
            for day in due_days:
                bisect.insort(items, day)
            while items:
                items.pop(0)

        rows.append((size, ms(timed(use_heap)), ms(timed(use_sorted_list))))
    return ("Add loans then remove them in due-date order",
            ["Loans", "Min-heap", "Sorted Python list"], rows)


# ----- output -----

def as_markdown(title, headers, rows):
    lines = [f"### {title}", "",
             "| " + " | ".join(headers) + " |",
             "|" + "---|" * len(headers)]
    for row in rows:
        lines.append("| " + " | ".join(f"{cell:,}" if isinstance(cell, int) else str(cell)
                                       for cell in row) + " |")
    return "\n".join(lines)


def main():
    random.seed(42)
    sections = []
    for benchmark in [lookup_benchmark, sort_benchmark, search_benchmark,
                      queue_benchmark, heap_benchmark]:
        print(f"Running {benchmark.__name__} ...")
        section = as_markdown(*benchmark())
        print(section, "\n")
        sections.append(section)
    RESULTS_FILE.write_text("# Performance results\n\n" + "\n\n".join(sections) + "\n", encoding="utf-8")
    print(f"Saved to {RESULTS_FILE}")


if __name__ == "__main__":
    main()