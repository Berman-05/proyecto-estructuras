from nodes import CircularNode
class CircularLinkedList[T]:
    def __init__(self):
        self.tail = None

    def is_empty(self) -> bool:
        return self.tail is None

    def insert_at_start(self, value: T):
        new_node = CircularNode(value)
        if self.is_empty():
            self.tail = new_node
            self.tail.next = new_node
        else:
            new_node.next = self.tail.next
            self.tail.next = new_node

    def insert_at_end(self, value: T):
        new_node = CircularNode(value)
        if self.is_empty():
            self.tail = new_node
            self.tail.next = new_node
        else:
            new_node.next = self.tail.next
            self.tail.next = new_node
            self.tail = new_node

    def delete_from_start(self):
        if self.is_empty():
            raise IndexError("La lista está vacía")
        if self.tail.next == self.tail:
            self.tail = None
        else:
            self.tail.next = self.tail.next.next

    def delete_from_end(self):
        if self.is_empty():
            raise IndexError("La lista está vacía")
        if self.tail.next == self.tail:
            self.tail = None
        else:
            current = self.tail.next
            while current.next != self.tail:
                current = current.next
            current.next = self.tail.next
            self.tail = current

    def search(self, value: T) -> bool:
        if self.is_empty():
            return False
        current = self.tail.next
        while True:
            if current.value == value:
                return True
            current = current.next
            if current == self.tail.next:
                break
        return False

    def rotate_left(self):
        if not self.is_empty() and self.tail.next != self.tail:
            self.tail = self.tail.next

    def rotate_right(self):
        if not self.is_empty() and self.tail.next != self.tail:
            current = self.tail.next
            while current.next != self.tail:
                current = current.next
            self.tail = current