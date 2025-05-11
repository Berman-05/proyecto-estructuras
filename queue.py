import json

class Cola:
    def __init__(self, max_nodos=10):
        self.items = []
        self.max_nodos = max_nodos

    def insertar(self, x):
        if len(self.items) < self.max_nodos:
            self.items.append(x)
        else:
            raise OverflowError("Cola llena")

    def eliminar(self):
        if self.items:
            return self.items.pop(0)
        else:
            raise IndexError("Cola vacía")

    def buscar(self, x):
        try:
            return self.items.index(x)
        except ValueError:
            return -1

    def limpiar(self):
        self.items.clear()

    @property
    def tamaño(self):
        return len(self.items)

    def guardar_en_json(self, archivo):
        with open(archivo, 'w') as f:
            json.dump({'items': self.items, 'max_nodos': self.max_nodos}, f)

    def cargar_de_json(self, archivo):
        with open(archivo, 'r') as f:
            datos = json.load(f)
            self.items = datos['items']
            self.max_nodos = datos['max_nodos']
