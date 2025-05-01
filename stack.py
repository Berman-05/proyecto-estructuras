class Stack[T]:
    def __init__(self):
        self.value = [T]

    def is_empty(self):
        return len(self.value) == 0

    def push(self, value: T):
        self.value.append(value)

    def pop(self):
        if not self.is_empty():
            return self.value.pop()
        else:
            raise IndexError("la pila está vacía")

    def peek(self):
        if not self.is_empty():
            return self.value[-1]
        else:
            raise IndexError("La pila esta vacia")

    def size(self):
        return len(self.value)