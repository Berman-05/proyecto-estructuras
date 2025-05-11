import json
class Pila:
    def __init__(self, max_nodos=10):
        self.items = []
        self.max_nodos = max_nodos

    def insertar(self, x):
        if len(self.items) < self.max_nodos:
            self.items.append(x)
        else:
            raise OverflowError("Pila llena")

    def eliminar(self):
        if self.items:
            return self.items.pop()
        else:
            raise IndexError("Pila vacía")

    def buscar(self, x):
        try:
            idx = len(self.items) - self.items[::-1].index(x) - 1
            return idx
        except ValueError:
            return -1

    def limpiar(self):
        self.items.clear()

    @property
    def tamaño(self):
        return len(self.items)
