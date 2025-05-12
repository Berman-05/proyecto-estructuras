import tkinter as tk
import json
from tkinter import ttk, messagebox, filedialog
from stack import Pila
from queue import Cola
from simple_list import ListaSimple
from lista_circular_gui import CircularListFrame
from lista_doble_gui import DoublyListFrame
from trees_gui import TreesGUI
def dibujar_pila(canvas: tk.Canvas, pila: Pila, highlight_index=None):
    canvas.delete("all")
    ancho, alto, sep = 100, 40, 10
    x0 = canvas.winfo_width() // 2 - ancho // 2
    y0 = 20
    for i, val in enumerate(reversed(pila.items)):
        y = y0 + i * (alto + sep)
        color = "#FF5733" if highlight_index == len(pila.items) - 1 - i else "#89CFF0"
        canvas.create_rectangle(x0, y, x0 + ancho, y + alto, fill=color, outline="#333")
        canvas.create_text(x0 + ancho // 2, y + alto // 2,
                           text=f"{val}\n0x{id(val) & 0xFFF:03X}", font=("Consolas", 10))
    info = f"Tamaño: {pila.tamaño} / {pila.max_nodos}"
    canvas.create_text(10, canvas.winfo_height() - 10,
                       text=info, anchor="w", font=("Consolas", 10, "italic"))


def dibujar_cola(canvas: tk.Canvas, cola: Cola, highlight_index=None):
    canvas.delete("all")
    ancho, alto, sep = 80, 40, 10
    x0 = 20
    y0 = canvas.winfo_height() // 2 - alto // 2
    for i, val in enumerate(cola.items):
        x = x0 + i * (ancho + sep)
        color = "#FF5733" if highlight_index == i else "#90EE90"
        canvas.create_rectangle(x, y0, x + ancho, y0 + alto, fill=color, outline="#333")
        canvas.create_text(x + ancho // 2, y0 + alto // 2,
                           text=f"{val}\n0x{id(val) & 0xFFF:03X}", font=("Consolas", 10))
    info = f"Tamaño: {cola.tamaño} / {cola.max_nodos}"
    canvas.create_text(10, 10, text=info, anchor="nw", font=("Consolas", 10, "italic"))


def dibujar_lista_simple(canvas: tk.Canvas, lista: ListaSimple, highlight_index=None):
    canvas.delete("all")
    ancho, alto, sep = 80, 40, 30
    x0 = 20
    y0 = 20
    aux = lista.cabeza
    i = 0
    while aux:
        x = x0 + i * (ancho + sep)
        color = "#FF5733" if highlight_index == i else "#FFD580"
        canvas.create_rectangle(x, y0, x + ancho, y0 + alto, fill=color, outline="#333")
        canvas.create_text(x + ancho // 2, y0 + alto // 2,
                           text=f"{aux.valor}", font=("Consolas", 10))
        # flecha
        canvas.create_line(x + ancho, y0 + alto // 2, x + ancho + sep, y0 + alto // 2, arrow=tk.LAST)
        aux = aux.siguiente
        i += 1
    info = f"Tamaño: {lista.tamaño} / {lista.max_nodos}"
    canvas.create_text(10, canvas.winfo_height() - 10,
                       text=info, anchor="w", font=("Consolas", 10, "italic"))


def guardar_datos(estructura):
    try:
        archivo = filedialog.asksaveasfilename(defaultextension=".json",
                                                filetypes=[("Archivos JSON", "*.json")])
        if not archivo:
            return
        with open(archivo, 'w') as file:
            json.dump(estructura.items, file)
        messagebox.showinfo("Guardado", "Datos guardados correctamente")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar: {e}")


def cargar_datos(estructura, callback_actualizar):
    try:
        archivo = filedialog.askopenfilename(filetypes=[("Archivos JSON", "*.json")])
        if not archivo:
            return
        with open(archivo, 'r') as file:
            datos = json.load(file)
            estructura.items = datos
            estructura.tamaño = len(datos)
        messagebox.showinfo("Cargado", "Datos cargados correctamente")
        callback_actualizar()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar: {e}")


def setup_pila_frame(frame):
    for w in frame.winfo_children(): w.destroy()
    pila = Pila(max_nodos=7)
    canvas = tk.Canvas(frame, bg="white", height=400)
    canvas.pack(fill="both", expand=True, padx=10, pady=10)
    ctrl = ttk.Frame(frame, style="Custom.TFrame");
    ctrl.pack(fill="x", padx=10, pady=5)
    ttk.Label(ctrl, text="Valor:", background="#1E1E2F", foreground="white").grid(row=0, column=0)
    entrada = ttk.Entry(ctrl, width=10);
    entrada.grid(row=0, column=1)

    def ac():
        dibujar_pila(canvas, pila)

    def ins():
        try:
            pila.insertar(entrada.get()); ac()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eli():
        try:
            pila.eliminar(); ac()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def bus():
        idx = pila.buscar(entrada.get())
        dibujar_pila(canvas, pila, highlight_index=idx if idx >= 0 else None)

    def lim():
        pila.limpiar(); ac()

    def guardar():
        guardar_datos(pila)

    def cargar():
        cargar_datos(pila, ac)

    for i, (t, f) in enumerate(
            [("Insertar", ins), ("Eliminar", eli), ("Buscar", bus), ("Limpiar", lim), ("Guardar", guardar),
             ("Cargar", cargar)]):
        ttk.Button(ctrl, text=t, style="RoundedButton.TButton", command=f).grid(row=0, column=2 + i)
    canvas.bind("<Configure>", lambda e: ac())
    ttk.Button(frame, text="⬅ Volver al Menú", style="RoundedButton.TButton",
               command=lambda: mostrar_frame("menu")).pack(pady=10)
    ac()


def setup_cola_frame(frame):
    for w in frame.winfo_children(): w.destroy()
    cola = Cola(max_nodos=7)
    canvas = tk.Canvas(frame, bg="white", height=300)
    canvas.pack(fill="both", expand=True, padx=10, pady=10)
    ctrl = ttk.Frame(frame, style="Custom.TFrame");
    ctrl.pack(fill="x", padx=10, pady=5)
    ttk.Label(ctrl, text="Valor:", background="#1E1E2F", foreground="white").grid(row=0, column=0)
    entrada = ttk.Entry(ctrl, width=10);
    entrada.grid(row=0, column=1)

    def ac():
        dibujar_cola(canvas, cola)

    def ins():
        try:
            cola.insertar(entrada.get()); ac()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eli():
        try:
            cola.eliminar(); ac()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def bus():
        idx = cola.buscar(entrada.get())
        dibujar_cola(canvas, cola, highlight_index=idx if idx >= 0 else None)

    def lim():
        cola.limpiar(); ac()

    def guardar():
        guardar_datos(cola)

    def cargar():
        cargar_datos(cola, ac)

    for i, (t, f) in enumerate(
            [("Insertar", ins), ("Eliminar", eli), ("Buscar", bus), ("Limpiar", lim), ("Guardar", guardar),
             ("Cargar", cargar)]):
        ttk.Button(ctrl, text=t, style="RoundedButton.TButton", command=f).grid(row=0, column=2 + i)
    canvas.bind("<Configure>", lambda e: ac())
    ttk.Button(frame, text="⬅ Volver al Menú", style="RoundedButton.TButton",
               command=lambda: mostrar_frame("menu")).pack(pady=10)
    ac()


def setup_lista_simple_frame(frame):
    for w in frame.winfo_children(): w.destroy()
    lista = ListaSimple(max_nodos=7)
    canvas = tk.Canvas(frame, bg="white", height=300)
    canvas.pack(fill="both", expand=True, padx=10, pady=10)
    ctrl = ttk.Frame(frame, style="Custom.TFrame");
    ctrl.pack(fill="x", padx=10, pady=5)
    ttk.Label(ctrl, text="Valor:", background="#1E1E2F", foreground="white").grid(row=0, column=0)
    entrada = ttk.Entry(ctrl, width=10);
    entrada.grid(row=0, column=1)

    def ac():
        dibujar_lista_simple(canvas, lista)

    def ins_i():
        try:
            lista.insertar_inicio(entrada.get()); ac()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def ins_f():
        try:
            lista.insertar_final(entrada.get()); ac()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eli_i():
        try:
            lista.eliminar_inicio(); ac()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eli_f():
        try:
            lista.eliminar_final(); ac()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def bus():
        idx = lista.buscar(entrada.get())
        dibujar_lista_simple(canvas, lista, highlight_index=idx if idx >= 0 else None)

    def lim():
        lista.limpiar(); ac()

    def guardar():
        guardar_datos(lista)

    def cargar():
        cargar_datos(lista, ac)

    acciones = [("Ins.Ini", ins_i), ("Ins.Fin", ins_f), ("Eli.Ini", eli_i), ("Eli.Fin", eli_f), ("Buscar", bus),
                ("Limpiar", lim), ("Guardar", guardar), ("Cargar", cargar)]
    for i, (t, f) in enumerate(acciones):
        ttk.Button(ctrl, text=t, style="RoundedButton.TButton", command=f).grid(row=0, column=2 + i)
    canvas.bind("<Configure>", lambda e: ac())
    ttk.Button(frame, text="⬅ Volver al Menú", style="RoundedButton.TButton",
               command=lambda: mostrar_frame("menu")).pack(pady=10)
    ac()


root = tk.Tk()
root.title("Visualizador de Estructuras")
root.configure(bg="#1E1E2F")
root.geometry("900x900")
root.resizable(False, False)
root.overrideredirect(True)

ancho_ventana, alto_ventana = 900, 900
ancho_pantalla = root.winfo_screenwidth()
alto_pantalla = root.winfo_screenheight()
x = (ancho_pantalla // 2) - (ancho_ventana // 2)
y = (alto_pantalla // 2) - (alto_ventana // 2)
root.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

style = ttk.Style()
style.theme_use("clam")
style.configure("Custom.TFrame", background="#1E1E2F")
style.configure("RoundedButton.TButton",
                font=("Century Gothic", 12), background="#2980b9",
                foreground="white", padding=(10, 5), relief="flat")
style.map("RoundedButton.TButton", background=[("active", "#4E80EE")])

frames = {}


def mostrar_frame(nombre):
    for f in frames.values():
        f.pack_forget()
    frame = frames[nombre]
    if nombre == "pila":
        setup_pila_frame(frame)
    elif nombre == "cola":
        setup_cola_frame(frame)
    elif nombre == "lista_simple":
        setup_lista_simple_frame(frame)
    frame.pack(expand=True)


menu_frame = ttk.Frame(root, style="Custom.TFrame", padding=30)
frames["menu"] = menu_frame

title = ttk.Label(menu_frame, text="VISUALIZADOR DE ESTRUCTURAS",
                  font=("Century Gothic", 20, "bold"),
                  foreground="white", background="#1E1E2F")
title.pack(pady=(0, 10))

subtitle = ttk.Label(menu_frame, text="Seleccione qué estructura desea visualizar",
                     font=("Century Gothic", 12),
                     foreground="white", background="#1E1E2F")
subtitle.pack(pady=(0, 30))


def crear_boton(texto, nombre_frame):
    return ttk.Button(menu_frame, text=texto,
                      style="RoundedButton.TButton",
                      command=lambda: mostrar_frame(nombre_frame))


botones = [
    crear_boton("📚 Pila", "pila"),
    crear_boton("📥 Cola", "cola"),
    crear_boton("🔗 Lista Simple", "lista_simple"),
    crear_boton("⚪ Lista Circular", "lista_circular"),
    crear_boton("🔗🔗 Lista Doble", "lista_doble"),
    crear_boton("🌳 Árbol Binario", "arbol_binario"),
    crear_boton("🔀 Árbol de Búsqueda", "arbol_busqueda"),
    ttk.Button(menu_frame, text="❌ Salir", style="RoundedButton.TButton", command=root.quit)
]
for boton in botones:
    boton.pack(pady=10, ipadx=40, ipady=10, fill="x")

for nombre in ["pila", "cola", "lista_simple", "lista_circular", "lista_doble", "arbol_binario", "arbol_busqueda"]:
    frame = ttk.Frame(root, style="Custom.TFrame", padding=30)
    frames[nombre] = frame
    if nombre not in ("pila", "cola", "lista_simple"):
        label = ttk.Label(frame, text=f"Vista de {nombre.replace('_', ' ').title()}",
                          font=("Century Gothic", 18, "bold"),
                          foreground="white", background="#1E1E2F")
        label.pack(pady=20)
        ttk.Button(frame, text="⬅ Volver al Menú",
                   style="RoundedButton.TButton",
                   command=lambda: mostrar_frame("menu")).pack(pady=20)

mostrar_frame("menu")
frames["lista_circular"] = CircularListFrame(root, mostrar_menu=lambda: mostrar_frame("menu"))
frames["lista_doble"] = DoublyListFrame(root, mostrar_menu=lambda: mostrar_frame("menu"))
frames["trees_gui"] = TreesGUI.crear_menu_arbol_binario(root, frames, "arbol_binario", None)
frames["arbol_busqueda"] = TreesGUI.crear_menu_arbol_busqueda(root, frames, "arbol_busqueda", None)
root.mainloop()