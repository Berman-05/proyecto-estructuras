from simple_node import NodoSimple
import json

class ListaSimple:
    def __init__(self, max_nodos=10):
        self.cabeza = None
        self.max_nodos = max_nodos
        self._tamaño = 0

    def insertar_inicio(self, x):
        if self._tamaño < self.max_nodos:
            nodo = NodoSimple(x)
            nodo.siguiente = self.cabeza
            self.cabeza = nodo
            self._tamaño += 1
        else:
            raise OverflowError("Lista llena")

    def insertar_final(self, x):
        if self._tamaño < self.max_nodos:
            nodo = NodoSimple(x)
            if not self.cabeza:
                self.cabeza = nodo
            else:
                aux = self.cabeza
                while aux.siguiente:
                    aux = aux.siguiente
                aux.siguiente = nodo
            self._tamaño += 1
        else:
            raise OverflowError("Lista llena")

    def eliminar_inicio(self):
        if self.cabeza:
            valor = self.cabeza.valor
            self.cabeza = self.cabeza.siguiente
            self._tamaño -= 1
            return valor
        else:
            raise IndexError("Lista vacía")

    def eliminar_final(self):
        if not self.cabeza:
            raise IndexError("Lista vacía")
        if not self.cabeza.siguiente:
            valor = self.cabeza.valor
            self.cabeza = None
        else:
            aux = self.cabeza
            while aux.siguiente.siguiente:
                aux = aux.siguiente
            valor = aux.siguiente.valor
            aux.siguiente = None
        self._tamaño -= 1
        return valor

    def buscar(self, x):
        aux = self.cabeza
        idx = 0
        while aux:
            if aux.valor == x:
                return idx
            aux = aux.siguiente
            idx += 1
        return -1

    def limpiar(self):
        self.cabeza = None
        self._tamaño = 0

    @property
    def tamaño(self):
        return self._tamaño

    def guardar_en_json(self, archivo):
        datos = []
        aux = self.cabeza
        while aux:
            datos.append(aux.valor)
            aux = aux.siguiente
        with open(archivo, 'w') as f:
            json.dump({'valores': datos, 'max_nodos': self.max_nodos}, f)

    def cargar_de_json(self, archivo):
        with open(archivo, 'r') as f:
            datos = json.load(f)
            self.limpiar()
            self.max_nodos = datos['max_nodos']
            for valor in datos['valores']:
                self.insertar_final(valor)
