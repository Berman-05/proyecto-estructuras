from nodes import TreeNode
import json
class BinarySearchTree[T]:
    def __init__(self):
        self.root = None

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

    def from_dict(self, data: dict | None) -> TreeNode[T] | None:
        if data is None:
            return None
        node = TreeNode(data["value"])
        node.left = self.from_dict(data["left"])
        node.right = self.from_dict(data["right"])
        return node

    def insert(self, value):
        if self.root is None:
            self.root = TreeNode(value)
        else:
            self._insert(self.root, value)

    def _insert(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert(node.left, value)
        elif value > node.value:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._insert(node.right, value)


    def save_to_file(self, filename: str):
        data = json.dumps(self.to_dict(self.root), ensure_ascii=False)
        with open(filename, "w", encoding="utf-8") as file:
            file.write(data)

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

    def to_dict(self, node: TreeNode[T] | None) -> dict | None:
        if node is None:
            return None
        else:
            return {
            "value": node.value,
            "left": self.to_dict(node.left),
            "right": self.to_dict(node.right)
            }

