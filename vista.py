import tkinter as tk
from tkinter import ttk
from tabla import creaTabla
from operaciones import (
    AgregarProducto,
    DarResultado,
    EliminarProducto,
)

root = tk.Tk()
agregar_producto = AgregarProducto()
dar_resultado = DarResultado()
eliminar_producto = EliminarProducto()
tabla = creaTabla()


def actualizar_treeview():
    agregar_producto.actualizar_treeview(tree)


root.configure(background="grey")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
style = ttk.Style(root)
style.theme_use("clam")
style.configure(
    "Treeview", background="black", fieldbackground="black", foreground="white"
)
root.title("Proyecto PYTHON")
titulo = tk.Label(
    root,
    text="Ingrese sus datos",
    bg="blue",
    fg="thistle1",
    height=1,
    width=60,
)
titulo.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
producto = tk.Label(root, text="Producto")
producto.grid(row=1, column=0, sticky="w")
cantidad = tk.Label(root, text="Cantidad")
cantidad.grid(row=2, column=0, sticky="w")
precio_unitario = tk.Label(root, text="Precio Unitario")
precio_unitario.grid(row=3, column=0, sticky="w")
descuento = tk.Label(root, text="Descuento (%)")
descuento.grid(row=4, column=0, sticky="w")
a_val = tk.StringVar()
b_val = tk.DoubleVar()
c_val = tk.DoubleVar()
d_val = tk.DoubleVar()
w_ancho = 20
entrada1 = tk.Entry(root, textvariable=a_val, width=w_ancho)
entrada1.grid(row=1, column=1, sticky="ew")
entrada2 = tk.Entry(root, textvariable=b_val, width=w_ancho)
entrada2.grid(row=2, column=1, sticky="ew")
entrada3 = tk.Entry(root, textvariable=c_val, width=w_ancho)
entrada3.grid(row=3, column=1, sticky="ew")
entrada4 = tk.Entry(root, textvariable=d_val, width=w_ancho)
entrada4.grid(row=4, column=1, sticky="ew")
tree = ttk.Treeview(root)
tree["columns"] = ("col1", "col2", "col3", "col4")
tree.column("#0", width=90, minwidth=50, anchor="w")
tree.column("col1", width=200, minwidth=80)
tree.column("col2", width=200, minwidth=80)
tree.column("col3", width=200, minwidth=80)
tree.column("col4", width=200, minwidth=80)
tree.heading("#0", text="ID")
tree.heading("col1", text="Producto")
tree.heading("col2", text="Cantidad")
tree.heading("col3", text="Precio Unitario")
tree.heading("col4", text="Precio Total")
scrollbar = tk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
tree.grid(row=0, column=2, columnspan=2, rowspan=9, padx=10, pady=10, sticky="nsew")
scrollbar.grid(row=0, column=4, rowspan=9, sticky="ns")
scrollbar.config(width=20)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_columnconfigure(4, weight=1)
boton_alta = tk.Button(
    root,
    text="Agregar",
    command=lambda: agregar_producto.alta(
        a_val.get(), b_val.get(), c_val.get(), d_val.get(), tree
    ),
)
boton_alta.grid(row=6, column=0, sticky="w", padx=10, pady=10)

boton_consulta = tk.Button(root, text="Sumar Total", command=dar_resultado.consultar)
boton_consulta.grid(row=7, column=0, sticky="w", padx=10, pady=10)

boton_borrar = tk.Button(
    root, text="Borrar", command=lambda: eliminar_producto.borrar(tree)
)
boton_borrar.grid(row=8, column=0, sticky="w", padx=10, pady=10)

actualizar_treeview()

tabla = creaTabla()

root.mainloop()