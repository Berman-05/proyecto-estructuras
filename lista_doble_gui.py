import tkinter as tk
from tkinter import ttk, filedialog
import json
from doubly_list import DoublyLinkedList  # tu clase de datos

class DoublyListFrame(ttk.Frame):
    def __init__(self, master, mostrar_menu, **kwargs):
        super().__init__(master, style="Custom.TFrame", padding=10, **kwargs)
        self.mostrar_menu = mostrar_menu
        self.lista = DoublyLinkedList()
        self.highlight_value = None

        self.canvas = tk.Canvas(self, width=700, height=350, bg="white")
        self.canvas.pack(pady=10)

        entry_frame = ttk.Frame(self, style="Custom.TFrame")
        entry_frame.pack(fill="x", pady=(0,5))
        ttk.Label(entry_frame, text="Valor:", background="#1E1E2F", foreground="white").pack(side="left", padx=(0,5))
        self.entry_val = ttk.Entry(entry_frame, width=15)
        self.entry_val.pack(side="left", padx=(0,10))
        ttk.Label(entry_frame, text="Posición:", background="#1E1E2F", foreground="white").pack(side="left", padx=(0,5))
        self.entry_pos = ttk.Entry(entry_frame, width=5)
        self.entry_pos.pack(side="left")

        btn_frame = ttk.Frame(self, style="Custom.TFrame")
        btn_frame.pack(pady=5, fill="x")
        ops = [
            ("Insertar inicio", self.insertar_inicio),
            ("Insertar final", self.insertar_final),
            ("Insertar pos.", self.insertar_posicion),
            ("Eliminar inicio", self.eliminar_inicio),
            ("Eliminar final", self.eliminar_final),
            ("Eliminar pos.", self.eliminar_posicion),
            ("Buscar", self.buscar_valor),
            ("Guardar", self.guardar_json),
            ("Cargar", self.cargar_json),
            ("Volver al menú", self.volver_menu)
        ]
        for idx, (txt, cmd) in enumerate(ops):
            r, c = divmod(idx, 2)
            b = ttk.Button(btn_frame, text=txt, style="RoundedButton.TButton", command=cmd)
            b.grid(row=r, column=c, padx=5, pady=5, ipadx=10, ipady=5, sticky="ew")
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)

        self.info_label = ttk.Label(self, text="Lista vacía", font=("Century Gothic", 12), background="#1E1E2F", foreground="white")
        self.info_label.pack(pady=(5,0))

    def volver_menu(self):
        self.lista = DoublyLinkedList()
        self.highlight_value = None
        self.redibujar()
        self.mostrar_menu()

    def insertar_inicio(self):
        val = self.entry_val.get().strip()
        if not val:
            self.info_label.config(text="Ingrese un valor.")
        elif self.lista.search(val):
            self.info_label.config(text=f"El valor {val} ya existe.")
        else:
            self.lista.insert_at_start(val)
            self.highlight_value = val
            self.info_label.config(text=f"Insertado {val} al inicio.")
        self.entry_val.delete(0, tk.END)
        self.redibujar()

    def insertar_final(self):
        val = self.entry_val.get().strip()
        if not val:
            self.info_label.config(text="Ingrese un valor.")
        elif self.lista.search(val):
            self.info_label.config(text=f"El valor {val} ya existe.")
        else:
            self.lista.insert_at_end(val)
            self.highlight_value = val
            self.info_label.config(text=f"Insertado {val} al final.")
        self.entry_val.delete(0, tk.END)
        self.redibujar()

    def insertar_posicion(self):
        val = self.entry_val.get().strip()
        pos = self.entry_pos.get().strip()
        if not val or not pos.isdigit():
            self.info_label.config(text="Ingrese valor y posición válidos.")
        else:
            idx = int(pos)
            if idx < 0:
                self.info_label.config(text="Posición no puede ser negativa.")
            elif self.lista.search(val):
                self.info_label.config(text=f"El valor {val} ya existe.")
            else:
                self.lista.insert_at_position(val, idx)
                self.highlight_value = val
                self.info_label.config(text=f"Insertado {val} en pos {idx}.")
        self.entry_val.delete(0, tk.END)
        self.entry_pos.delete(0, tk.END)
        self.redibujar()

    def eliminar_inicio(self):
        if self.lista.is_empty():
            self.info_label.config(text="Lista vacía.")
        else:
            val = self.lista.head.value
            self.lista.delete_from_start()
            self.highlight_value = val
            self.info_label.config(text=f"Eliminado inicio: {val}.")
        self.redibujar()

    def eliminar_final(self):
        if self.lista.is_empty():
            self.info_label.config(text="Lista vacía.")
        else:
            val = self.lista.tail.value
            self.lista.delete_from_end()
            self.highlight_value = val
            self.info_label.config(text=f"Eliminado final: {val}.")
        self.redibujar()

    def eliminar_posicion(self):
        pos = self.entry_pos.get().strip()
        if not pos.isdigit():
            self.info_label.config(text="Posición inválida.")
        elif self.lista.is_empty():
            self.info_label.config(text="Lista vacía.")
        else:
            idx = int(pos)
            if idx < 0:
                self.info_label.config(text="Posición negativa no válida.")
            else:
                curr = self.lista.head
                count = 0
                while curr and count < idx:
                    curr = curr.next
                    count += 1
                if curr is None:
                    self.info_label.config(text="Posición fuera de rango.")
                else:
                    val = curr.value
                    self.lista.delete_from_position(idx)
                    self.highlight_value = val
                    self.info_label.config(text=f"Eliminado pos {idx}: {val}.")
        self.entry_pos.delete(0, tk.END)
        self.redibujar()

    def buscar_valor(self):
        val = self.entry_val.get().strip()
        if not val:
            self.info_label.config(text="Ingrese un valor.")
        else:
            found = self.lista.search(val)
            self.highlight_value = val if found else None
            self.info_label.config(text=f"Valor {'encontrado' if found else 'no encontrado'}: {val}.")
        self.entry_val.delete(0, tk.END)
        self.redibujar()

    def guardar_json(self):
        path = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[('JSON files','*.json')])
        if not path:
            return
        data = []
        curr = self.lista.head
        while curr:
            data.append(curr.value)
            curr = curr.next
        with open(path, 'w') as f:
            json.dump(data, f)
        self.info_label.config(text=f"Guardado en {path}")

    def cargar_json(self):
        path = filedialog.askopenfilename(filetypes=[('JSON files','*.json')])
        if not path:
            return
        with open(path) as f:
            data = json.load(f)
        self.lista = DoublyLinkedList()
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
            self.canvas.create_text(350, 175, text="NULL", font=("Arial", 14, "bold"), fill="gray")
            return

        values = []
        curr = self.lista.head
        while curr:
            values.append(curr.value)
            curr = curr.next

        n = len(values)
        spacing = 700 // (n + 1)
        y = 175
        w, h = 80, 40
        coords = []

        for i, v in enumerate(values):
            x = spacing + i * spacing
            coords.append((x, y))
            fill = "#219EBC" if v == self.highlight_value else "#7DC3C1"
            self.canvas.create_rectangle(x - w // 2, y - h // 2, x + w // 2, y + h // 2,
                                         fill=fill, outline="black")
            self.canvas.create_text(x, y, text=str(v), font=("Arial", 12, "bold"))

        for i in range(n - 1):
            x1, y1 = coords[i]
            x2, y2 = coords[i + 1]
            self.canvas.create_line(x1 + w // 2, y1, x2 - w // 2, y2, arrow=tk.LAST)

        for i in range(1, n):
            x1, y1 = coords[i]
            x2, y2 = coords[i - 1]
            self.canvas.create_line(x1 - w // 2, y1 + 10, x2 + w // 2, y2 + 10, arrow=tk.LAST)


        x_null_left = coords[0][0] - spacing
        x_null_right = coords[-1][0] + spacing
        self.canvas.create_line(coords[0][0] - w // 2, y, x_null_left + 30, y, arrow=tk.LAST)
        self.canvas.create_line(coords[-1][0] + w // 2, y + 10, x_null_right - 30, y + 10, arrow=tk.LAST)

        self.info_label.config(text=f"Nodos: {n}")
