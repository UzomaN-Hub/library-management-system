# Performance results

### Find one book by ISBN (time per lookup)

| Books | Hash table | Linear search |
|---|---|---|
| 1,000 | 0.29 µs | 30.01 µs |
| 10,000 | 0.49 µs | 384.00 µs |
| 100,000 | 0.59 µs | 3,819.26 µs |
| 1,000,000 | 0.72 µs | 33,572.74 µs |

### Sort all books

| Books | Merge sort | Bubble sort |
|---|---|---|
| 100 | 0.39 ms | 1.24 ms |
| 1,000 | 5.57 ms | 74.18 ms |
| 5,000 | 16.65 ms | 2,001.44 ms |
| 10,000 | 36.41 ms | not run (too slow) |
| 100,000 | 469.82 ms | not run (too slow) |
| 1,000,000 | 7,407.06 ms | not run (too slow) |

### Find one book by title in a sorted list (time per search)

| Books | Binary search | Linear search |
|---|---|---|
| 1,000 | 2.03 µs | 37.35 µs |
| 10,000 | 2.49 µs | 329.85 µs |
| 100,000 | 3.17 µs | 4,983.97 µs |
| 1,000,000 | 4.26 µs | 40,366.99 µs |

### Add then serve every reservation

| Reservations | Linked-list queue | Python list pop(0) |
|---|---|---|
| 1,000 | 0.43 ms | 0.13 ms |
| 10,000 | 4.12 ms | 5.18 ms |
| 100,000 | 48.29 ms | 927.59 ms |

### Add loans then remove them in due-date order

| Loans | Min-heap | Sorted Python list |
|---|---|---|
| 1,000 | 3.55 ms | 0.33 ms |
| 10,000 | 52.19 ms | 17.03 ms |
| 100,000 | 689.36 ms | 1,772.37 ms |
