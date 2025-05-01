from nodes import SimpleNode
class SinglyLinkedList[T]:
    def __init__(self):
        self.head = None

    def insert_at_start(self, value:[T]):
        new_node = SimpleNode(value)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, value:[T]):
        new_node = SimpleNode(value)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def delete_from_start(self):
        if not self.head:
            raise IndexError("La lista está vacía")
        self.head = self.head.next

    def delete_from_end(self):
        if not self.head:
            raise IndexError("La lista está vacía")
        if not self.head.next:
            self.head = None
        else:
            current = self.head
            while current.next and current.next.next:
                current = current.next
            current.next = None

    def search(self, value:[T]):
        current = self.head
        while current:
            if current.value == value:
                return True
            current = current.next
        return False