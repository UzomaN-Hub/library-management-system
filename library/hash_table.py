"""Hash table using separate chaining to resolve collisions."""


class HashTable:
    """Maps keys (such as ISBNs) to values (such as Book objects).

    Each slot (bucket) holds a list of (key, value) pairs. Keys that hash
    to the same bucket are stored together in that list (separate chaining).
    """

    def __init__(self, capacity=16, max_load_factor=0.75):
        if capacity < 1:
            raise ValueError("Capacity must be at least 1.")
        self._capacity = capacity
        self._max_load_factor = max_load_factor
        self._buckets = [[] for _ in range(capacity)]
        self._size = 0

    def _bucket_index(self, key):
        return hash(key) % self._capacity

    def put(self, key, value):
        """Add a key-value pair, or replace the value if the key exists."""
        if key is None:
            raise ValueError("Key cannot be None.")
        bucket = self._buckets[self._bucket_index(key)]
        for index, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket[index] = (key, value)
                return
        bucket.append((key, value))
        self._size += 1
        if self._size / self._capacity > self._max_load_factor:
            self._resize(self._capacity * 2)

    def get(self, key, default=None):
        """Return the value for key, or default if the key is not stored."""
        bucket = self._buckets[self._bucket_index(key)]
        for existing_key, value in bucket:
            if existing_key == key:
                return value
        return default

    def remove(self, key):
        """Remove key and return its value. Raise KeyError if missing."""
        bucket = self._buckets[self._bucket_index(key)]
        for index, (existing_key, value) in enumerate(bucket):
            if existing_key == key:
                del bucket[index]
                self._size -= 1
                return value
        raise KeyError(key)

    def keys(self):
        """Return all stored keys."""
        return [key for bucket in self._buckets for key, _ in bucket]

    def values(self):
        """Return all stored values."""
        return [value for bucket in self._buckets for _, value in bucket]

    def _resize(self, new_capacity):
        old_items = [pair for bucket in self._buckets for pair in bucket]
        self._capacity = new_capacity
        self._buckets = [[] for _ in range(new_capacity)]
        for key, value in old_items:
            self._buckets[self._bucket_index(key)].append((key, value))

    @property
    def capacity(self):
        return self._capacity

    def __len__(self):
        return self._size

    def __contains__(self, key):
        sentinel = object()
        return self.get(key, sentinel) is not sentinel