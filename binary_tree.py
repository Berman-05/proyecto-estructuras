from nodes import TreeNode
class BinaryTree[T]:
    def __init__(self):
        self.root  = None

    def insert(self, value: T):
        if self.root is None:
            self.root = TreeNode(value)
        else:
            self._insert(self.root, value)

    def __insert(self, node: TreeNode[T], value: T):
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self.__insert(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self.__insert(node.right, value)


    def search(self, value: str) -> TreeNode[T] | None:
        return self.__search(value, self.root)

    def __search(self, value: str, ref: TreeNode[T] | None) -> TreeNode[T] | None:
        if ref is None:
            return None
        elif ref.is_leaf():
            pass
        if ref.value == value:
            return ref

        left = self.__search(value, ref.left)
        if left is None:
            right = self.__search(value, ref.right)
            return right
        return left

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