import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.filedialog as filedialog
import json
from nodes import TreeNode

class TreesGUI(ttk.Frame):
    def __init__(self, root, frames, nombre, tree, **kwargs):
        super().__init__(root, **kwargs)
        self.root = root
        self.frames = frames
        self.nombre = nombre
        self.tree = tree
        self.frames[nombre] = self
        self.configure(style="Custom.TFrame")
        self.canvas = tk.Canvas(self, width=800, height=400, bg="white")
        self.canvas.pack(pady=20)

        self.entry = ttk.Entry(self, font=("Century Gothic", 12))
        self.entry.pack(pady=10)

        botones_frame = ttk.Frame(self, style="Custom.TFrame")
        botones_frame.pack(pady=10)

        ttk.Button(botones_frame, text="Insertar Izquierda", style="RoundedButton.TButton",
                   command=lambda: self.insertar_nodo_arbol_binario(lado="left")).pack(side="left", padx=5, ipadx=10, ipady=5)
        ttk.Button(botones_frame, text="Insertar Derecha", style="RoundedButton.TButton",
                   command=lambda: self.insertar_nodo_arbol_binario(lado="right")).pack(side="left", padx=5, ipadx=10, ipady=5)
        ttk.Button(botones_frame, text="Eliminar Nodo", style="RoundedButton.TButton",
                   command=self.eliminar_nodo_arbol_binario).pack(side="left", padx=5, ipadx=10, ipady=5)
        ttk.Button(botones_frame, text="Buscar Nodo", style="RoundedButton.TButton",
                   command=self.buscar_nodo).pack(side="left", padx=5, ipadx=10, ipady=5)

        botones_frame_2 = ttk.Frame(self, style="Custom.TFrame")
        botones_frame_2.pack(pady=10)

        ttk.Button(botones_frame_2, text="Guardar Árbol", style="RoundedButton.TButton",
                   command=self.guardar_arbol).pack(side="left", padx=5, ipadx=10, ipady=5)
        ttk.Button(botones_frame_2, text="Cargar Árbol", style="RoundedButton.TButton",
                   command=self.cargar_arbol).pack(side="left", padx=5, ipadx=10, ipady=5)

        ttk.Button(self, text="⬅ Volver al Menú", style="RoundedButton.TButton",
                   command=lambda: self.mostrar_frame("menu")).pack(pady=20, ipadx=10, ipady=5)



    def insertar_nodo_arbol_binario(self, lado):
        value = self.entry.get()
        if value:
            try:
                self.tree.insert(value, lado)
                self.canvas.delete("all")
                self.dibujar_arbol()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo insertar el nodo: {e}")

    def eliminar_nodo_arbol_binario(self):
        value = self.entry.get()
        if value:
            try:
                self.tree.delete(value)
                self.canvas.delete("all")
                self.dibujar_arbol()
            except ValueError as e:
                messagebox.showwarning("Advertencia", f"{e}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el nodo: {e}")

    def buscar_nodo(self):
        value = self.entry.get()
        if value:
            result = self.tree.search(value)
            self.canvas.delete("all")
            self.dibujar_arbol(highlight=result)
            if result:
                messagebox.showinfo("Resultado de Búsqueda", f"El nodo con valor '{value}' fue encontrado.")
            else:
                messagebox.showwarning("Resultado de Búsqueda", f"El nodo con valor '{value}' no existe.")

    def guardar_arbol(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            try:
                self.tree.save_to_file(filename)
                messagebox.showinfo("Éxito", f"Árbol guardado en {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el árbol: {e}")

    def cargar_arbol(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            try:
                with open(filename, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    self.tree.root = self.reconstruir_arbol(data)
                self.canvas.delete("all")
                self.dibujar_arbol()
                messagebox.showinfo("Éxito", f"Árbol cargado desde {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el árbol: {e}")

    def reconstruir_arbol(self, data):
        if data is None:
            return None
        node = TreeNode(data["value"])
        node.left = self.reconstruir_arbol(data["left"])
        node.right = self.reconstruir_arbol(data["right"])
        return node

    def dibujar_arbol(self, x=400, y=50, dx=100, dy=50, node=None, highlight=None):
        if node is None:
            node = self.tree.root
        if node:
            color = "lightgreen" if node == highlight else "lightblue"
            self.canvas.create_oval(x-15, y-15, x+15, y+15, fill=color)
            self.canvas.create_text(x, y, text=f"{node.value}\n@{id(node)}", font=("Arial", 10, "bold"))
            if node.left:
                self.canvas.create_line(x, y, x-dx, y+dy, arrow=tk.LAST)
                self.dibujar_arbol(x-dx, y+dy, dx//2, dy, node.left, highlight)
            if node.right:
                self.canvas.create_line(x, y, x+dx, y+dy, arrow=tk.LAST)
                self.dibujar_arbol(x+dx, y+dy, dx//2, dy, node.right, highlight)

    def mostrar_frame(self, nombre):
        for frame in self.frames.values():
            frame.pack_forget()
        if nombre in self.frames:
            self.frames[nombre].pack(expand=True, fill="both")


    @classmethod
    def crear_menu_arbol_binario(cls, root, frames, nombre, tree):
        menu_arbol = cls(root, frames, nombre, tree)
        return menu_arbol
    @classmethod
    def crear_menu_arbol_busqueda(cls, root, frames, nombre, tree):
        menu_arbol_busqueda = cls(root, frames, nombre, tree)
        return menu_arbol_busqueda