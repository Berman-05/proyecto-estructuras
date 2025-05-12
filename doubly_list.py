from nodes import DoubleNode
class DoublyLinkedList[T]:
    def __init__(self):
        self.head: DoubleNode[T] | None = None
        self.tail: DoubleNode[T] | None = None

    def is_empty(self) -> bool:
        return self.head is None and self.tail is None

    def insert_at_start(self, value: T = None):
        new_node = DoubleNode(value)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

    def insert_at_end(self, value: T = None):
        new_node = DoubleNode(value)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

    def insert_at_position(self, value: T, position: int):
        if position <= 0:
            self.insert_at_start(value)
        else:
            new_node = DoubleNode(value)
            current = self.head
            index = 0
            while current and index < position - 1:
                current = current.next
                index += 1
            if current is None:
                self.insert_at_end(value)
            else:
                new_node.next = current.next
                new_node.prev = current
                if current.next:
                    current.next.prev = new_node
                current.next = new_node
                if new_node.next is None:
                    self.tail = new_node

    def delete_from_start(self):
        if self.is_empty():
            raise IndexError("La lista está vacía")
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None

    def delete_from_end(self):
        if self.is_empty():
            raise IndexError("La lista está vacía")
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None

    def delete_from_position(self, position: int) -> None:
        if self.is_empty():
            raise IndexError("La lista está vacía")
        if position < 0:
            raise IndexError("Posición no válida")
        if position == 0:
            self.delete_from_start()
            return
        current = self.head
        index = 0
        while current and index < position:
            current = current.next
            index += 1

        if current is None:
            raise IndexError("Posición fuera de rango")
        if current == self.tail:
            self.delete_from_end()
            return
        prev_node = current.prev
        next_node = current.next
        if prev_node:
            prev_node.next = next_node
        if next_node:
            next_node.prev = prev_node
        current.prev = None
        current.next = None

    def search(self, value: T) -> bool:
        current = self.head
        while current:
            if current.value == value:
                return True
            current = current.next
        return False