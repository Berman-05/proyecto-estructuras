from nodes import TreeNode
import json
from tkinter import messagebox
class BinaryTree[T]:
    def __init__(self):
        self.root  = None

    def from_dict(self, data: dict | None) -> TreeNode[T] | None:
        if data is None:
            return None
        node = TreeNode(data["value"])
        node.left = self.from_dict(data["left"])
        node.right = self.from_dict(data["right"])
        return node

    def delete(self, value):
        if self.search(value):
            try:
                self.root = self._delete_recursive(self.root, value)
                messagebox.showinfo("Éxito", f"El nodo con valor {value} fue eliminado.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", f"El valor {value} no se encuentra en el árbol.")

    def _delete_recursive(self, node, value):
        if node is None:
            raise ValueError(f"El valor {value} no se encuentra en el árbol.")

        if node.value == value:

            if node.is_leaf():
                return None

            if node.left is None:
                return node.right
            if node.right is None:
                return node.left

            deepest_left = self._find_deepest_left(node.left)
            node.value = deepest_left.value
            node.left = self._delete_recursive(node.left, deepest_left.value)
        else:

            if node.left:
                node.left = self._delete_recursive(node.left, value)
            if node.right:
                node.right = self._delete_recursive(node.right, value)

        return node

    def _find_deepest_left(self, node):
        while node.right is not None:
            node = node.right
        return node

    def insert(self, value, lado=None):
        if self.root is None:
            self.root = TreeNode(value)
        else:
            if lado == "left":
                self._insert_left(self.root, value)
            elif lado == "right":
                self._insert_right(self.root, value)

    def _insert_left(self, node, value):
        if node.left is None:
            node.left = TreeNode(value)
        else:
            self._insert_left(node.left, value)

    def _insert_right(self, node, value):
        if node.right is None:
            node.right = TreeNode(value)
        else:
            self._insert_right(node.right, value)

    def save_to_file(self, filename: str):
        data = json.dumps(self.to_dict(self.root), ensure_ascii=False)
        with open(filename, "w", encoding="utf-8") as file:
            file.write(data)

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

    def to_dict(self, node: TreeNode[T] | None) -> dict | None:
        if node is None:
            return None
        else:
            return {
            "value": node.value,
            "left": self.to_dict(node.left),
            "right": self.to_dict(node.right)
            }