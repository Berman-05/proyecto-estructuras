class SimpleNode[T]:
    def __init__(self, value:T):
        self.value = value
        self.next = None
class CircularNode[T]:
    def __init__(self, value: T):
        self.value = value
        self.next = None
class DoubleNode[T]:
    def __init__(self, value: T):
        self.value = value
        self.next = None
        self.prev = None
class TreeNode[T]:
    def __init__(self, value: T):
        self.value = value
        self.left = None
        self.right = None
    def is_leaf(self):
        return self.left is None and self.right is None