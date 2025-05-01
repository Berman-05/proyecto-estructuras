class Queue[T]:
    def __init__(self):
        self.value = [T]

    def is_empty(self):
        return len(self.value) == 0

    def enqueue(self, item:T):
        self.value.insert(0, item)

    def dequeue(self):
        return self.value.pop()

    def size(self):
        return len(self.value)

    def peek(self):
        return self.value[-1] if not self.is_empty() else None