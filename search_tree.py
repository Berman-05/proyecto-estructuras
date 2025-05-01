from nodes import TreeNode

class BinarySearchTree[T]:
    def __init__(self):
        self.root = None

    def insert(self, value: T):
        if self.root is None:
            self.root = TreeNode(value)
        else:
            self._insert(self.root, value)

    def _insert(self, node: TreeNode[T], value: T):
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._insert(node.right, value)

    def search(self, value: T) -> bool:
        return self._search(self.root, value)

    def _search(self, node: TreeNode[T] | None, value: T) -> bool:
        if node is None:
            return False
        if node.value == value:
            return True
        elif value < node.value:
            return self._search(node.left, value)
        else:
            return self._search(node.right, value)

    def delete(self, value: T):
        self.root = self.__delete(self.root, value)

    def __delete(self, node: TreeNode[T], value: T) -> TreeNode[T]:
        if node is None:
            raise ValueError("valor no encontrado")

        if value < node.value:
            node.left = self.__delete(node.left, value)
        elif value > node.value:
            node.right = self.__delete(node.right, value)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            aux = node.right
            while aux.left:
                aux = aux.left
            node.value = aux.value
            node.right = self.__delete(node.right, aux.value)

        return node