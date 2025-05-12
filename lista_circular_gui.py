import tkinter as tk
from tkinter import ttk, filedialog
import json
from circular_list import CircularLinkedList  # tu clase de datos

class CircularListFrame(ttk.Frame):
    def __init__(self, master, mostrar_menu, **kwargs):
        super().__init__(master, style="Custom.TFrame", padding=10, **kwargs)
        self.mostrar_menu = mostrar_menu
        self.lista = CircularLinkedList()
        self.highlight_value = None  # valor a resaltar

        self.canvas = tk.Canvas(self, width=700, height=350, bg="white")
        self.canvas.pack(pady=10)

        entry_frame = ttk.Frame(self, style="Custom.TFrame")
        entry_frame.pack(fill="x", pady=(0,5))
        ttk.Label(entry_frame, text="Valor:", background="#1E1E2F", foreground="white").pack(side="left", padx=(0,5))
        self.entry = ttk.Entry(entry_frame)
        self.entry.pack(side="left", fill="x", expand=True)

        btn_frame = ttk.Frame(self, style="Custom.TFrame")
        btn_frame.pack(pady=5)

        operaciones = [
            ("Insertar inicio", self.insertar_inicio),
            ("Insertar final",  self.insertar_final),
            ("Buscar",          self.buscar_valor),
            ("Eliminar inicio", self.eliminar_inicio),
            ("Eliminar final",  self.eliminar_final),
            ("Rotar izquierda", self.rotar_izquierda),
            ("Rotar derecha",   self.rotar_derecha),
            ("Guardar",    self.guardar_json),
            ("Cargar",     self.cargar_json),
            ("Volver al menú",  self.mostrar_menu)
        ]
        for idx, (texto, cmd) in enumerate(operaciones):
            r, c = divmod(idx, 2)
            b = ttk.Button(btn_frame, text=texto,
                           style="RoundedButton.TButton", command=cmd)
            b.grid(row=r, column=c, padx=5, pady=5, ipadx=10, ipady=5, sticky="ew")
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)


        self.info_label = ttk.Label(self, text="Lista vacía",
            font=("Century Gothic", 12), background="#1E1E2F", foreground="white")
        self.info_label.pack(pady=(5,0))

    def insertar_inicio(self):
        val = self.entry.get().strip()
        if not val:
            self.info_label.config(text="Ingrese un valor.")
            return
        if self.lista.search(val):
            self.info_label.config(text=f"El valor {val} ya existe.")
        else:
            self.lista.insert_at_start(val)
            self.highlight_value = val
            self.redibujar()
            self.info_label.config(text=f"Insertado {val} al inicio.")
        self.entry.delete(0, tk.END)

    def insertar_final(self):
        val = self.entry.get().strip()
        if not val:
            self.info_label.config(text="Ingrese un valor.")
            return
        if self.lista.search(val):
            self.info_label.config(text=f"El valor {val} ya existe.")
        else:
            self.lista.insert_at_end(val)
            self.highlight_value = val
            self.redibujar()
            self.info_label.config(text=f"Insertado {val} al final.")
        self.entry.delete(0, tk.END)

    def buscar_valor(self):
        val = self.entry.get().strip()
        if not val:
            self.info_label.config(text="Ingrese un valor.")
        else:
            found = self.lista.search(val)
            self.highlight_value = val if found else None
            self.redibujar()
            self.info_label.config(text=f"Valor {'encontrado' if found else 'no encontrado'}: {val}.")
        self.entry.delete(0, tk.END)

    def eliminar_inicio(self):
        if self.lista.is_empty():
            self.info_label.config(text="Lista vacía.")
        else:
            val = self.lista.tail.next.value
            self.lista.delete_from_start()
            self.highlight_value = val
            self.redibujar()
            self.info_label.config(text=f"Eliminado inicio: {val}.")

    def eliminar_final(self):
        if self.lista.is_empty():
            self.info_label.config(text="Lista vacía.")
        else:
            curr = self.lista.tail.next
            while curr.next != self.lista.tail:
                curr = curr.next
            val = self.lista.tail.value
            self.lista.delete_from_end()
            self.highlight_value = val
            self.redibujar()
            self.info_label.config(text=f"Eliminado final: {val}.")

    def rotar_izquierda(self):
        if not self.lista.is_empty():
            self.lista.rotate_left()
            self.redibujar()
            self.info_label.config(text="Rotado izquierda.")

    def rotar_derecha(self):
        if not self.lista.is_empty():
            self.lista.rotate_right()
            self.redibujar()
            self.info_label.config(text="Rotado derecha.")

    def guardar_json(self):
        path = filedialog.asksaveasfilename(defaultextension='.json',
                                            filetypes=[('JSON files','*.json')])
        if not path:
            return
        data = []
        curr = self.lista.tail.next if not self.lista.is_empty() else None
        if curr:
            start = curr
            while True:
                data.append(curr.value)
                curr = curr.next
                if curr == start:
                    break
        with open(path, 'w') as f:
            json.dump(data, f)
        self.info_label.config(text=f"Guardado en {path}")

    def cargar_json(self):
        path = filedialog.askopenfilename(filetypes=[('JSON files','*.json')])
        if not path:
            return
        with open(path) as f:
            data = json.load(f)

        self.lista = CircularLinkedList()
        for val in data:
            if not self.lista.search(val):
                self.lista.insert_at_end(val)
        self.highlight_value = None
        self.redibujar()
        self.info_label.config(text=f"Cargado desde {path}")

    def redibujar(self):
        self.canvas.delete("all")
        if self.lista.is_empty():
            self.info_label.config(text="Lista vacía")
            return
        nodes = []
        start = self.lista.tail.next
        curr = start
        while True:
            nodes.append(curr.value)
            curr = curr.next
            if curr == start: break

        n = len(nodes)
        spacing = 700 // n
        y = 175
        w, h = 80, 40
        coords = []

        for i, v in enumerate(nodes):
            x = spacing//2 + i*spacing
            coords.append((x,y))
            fill = "#219EBC" if v == self.highlight_value else "#7DC3C1"
            self.canvas.create_rectangle(x-w//2, y-h//2, x+w//2, y+h//2,
                                         fill=fill, outline="black")
            self.canvas.create_text(x, y, text=str(v), font=("Arial", 12, "bold"))

        for i in range(n-1):
            x1, y1 = coords[i]
            x2, y2 = coords[i+1]
            self.canvas.create_line(x1 + w//2, y1, x2 - w//2, y2,
                                    arrow=tk.LAST)

        x_last, y_last = coords[-1]
        x_first, y_first = coords[0]
        ctrl1 = (x_last + 50, y_last - 80)
        ctrl2 = (x_first - 50, y_first - 80)
        self.canvas.create_line(
            x_last + w//2, y_last,
            ctrl1[0], ctrl1[1],
            ctrl2[0], ctrl2[1],
            x_first - w//2, y_first,
            arrow=tk.LAST,
            smooth=True
        )

        self.info_label.config(text=f"Nodos: {n}")
