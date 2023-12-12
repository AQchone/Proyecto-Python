import tkinter as tk
from tkinter.messagebox import showerror
from tkinter.messagebox import showinfo
import sqlite3
from tkinter import ttk
import re


def conexion():
    try:
        con = sqlite3.connect("mibase.db")
        return con
    except sqlite3.Error as e:
        showerror("Error", f"Error al conectar a la base de datos: {e}")


def crear_tabla():
    try:
        con = conexion()
        cursor = con.cursor()
        sql = """CREATE TABLE IF NOT EXISTS productos
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 producto varchar(20) NOT NULL,
                 cantidad real,
                 precio_unitario real,
                 precio_total real)
        """
        cursor.execute(sql)
        con.commit()
    except sqlite3.Error as e:
        showerror("Error", f"Error al crear la tabla: {e}")


crear_tabla()


def alta(producto, cantidad, precio_unitario, descuento, tree):
    cadena = producto
    patron = "^[A-Za-záéíóú]*$"
    if re.match(patron, cadena):
        try:
            con = conexion()
            cursor = con.cursor()
            precio_total = cantidad * precio_unitario * (1 - descuento / 100)
            data = (producto, cantidad, precio_unitario, precio_total)
            sql = "INSERT INTO productos(producto, cantidad, precio_unitario, precio_total) VALUES(?, ?, ?, ?)"
            cursor.execute(sql, data)
            con.commit()
            actualizar_treeview(tree)
        except sqlite3.Error as e:
            showerror("Error", f"Error al dar de alta el producto: {e}")
    else:
        showerror("Error", "El campo producto solo puede contener letras")


def consultar():
    try:
        con = conexion()
        cursor = con.cursor()
        sql = "SELECT SUM(precio_total) FROM productos"
        cursor.execute(sql)
        result = cursor.fetchone()[0]
        showinfo("Suma de Precios", f"El resultado de la suma de precios es: ${result}")
    except sqlite3.Error as e:
        showerror("Error", f"Error al consultar los precios: {e}")


def borrar(tree):
    valor = tree.selection()
    if valor:
        item = tree.item(valor)
        mi_id = item["text"]
        try:
            con = conexion()
            cursor = con.cursor()
            data = (mi_id,)
            sql = "DELETE FROM productos WHERE id = ?"
            cursor.execute(sql, data)
            con.commit()
            tree.delete(valor)
        except sqlite3.Error as e:
            showerror("Error", f"Error al borrar el producto: {e}")
    else:
        showerror("Error", "Debe seleccionar un producto para borrar")


def actualizar_treeview(mitreview):
    mitreview.delete(*mitreview.get_children())
    try:
        con = conexion()
        cursor = con.cursor()
        sql = "SELECT * FROM productos ORDER BY id ASC"
        datos = cursor.execute(sql)
        resultado = datos.fetchall()
        for fila in resultado:
            mitreview.insert(
                "", 0, text=fila[0], values=(fila[1], fila[2], fila[3], fila[4])
            )
    except sqlite3.Error as e:
        showerror("Error", f"Error al actualizar el treeview: {e}")


root = tk.Tk()

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
    command=lambda: alta(a_val.get(), b_val.get(), c_val.get(), d_val.get(), tree),
)
boton_alta.grid(row=6, column=0, sticky="w", padx=10, pady=10)
boton_consulta = tk.Button(root, text="Sumar Total", command=lambda: consultar())
boton_consulta.grid(row=7, column=0, sticky="w", padx=10, pady=10)
boton_borrar = tk.Button(root, text="Borrar", command=lambda: borrar(tree))
boton_borrar.grid(row=8, column=0, sticky="w", padx=10, pady=10)
root.mainloop()
