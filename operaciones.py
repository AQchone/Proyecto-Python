import re
import sqlite3
from tkinter.messagebox import showerror, showinfo
import conexion


class AgregarProducto:
    def alta(self, producto, cantidad, precio_unitario, descuento, tree):
        cadena = producto
        patron = "^[A-Za-záéíóú]*$"
        if re.match(patron, cadena):
            try:
                con = conexion.conexion()
                cursor = con.cursor()
                precio_total = cantidad * precio_unitario * (1 - descuento / 100)
                data = (producto, cantidad, precio_unitario, precio_total)
                sql = "INSERT INTO productos(producto, cantidad, precio_unitario, precio_total) VALUES(?, ?, ?, ?)"
                cursor.execute(sql, data)
                con.commit()
                self.actualizar_treeview(tree)
            except sqlite3.Error as e:
                showerror("Error", f"Error al dar de alta el producto: {e}")
        else:
            showerror("Error", "El campo producto solo puede contener letras")

    def actualizar_treeview(self, mitreview):
        mitreview.delete(*mitreview.get_children())
        try:
            con = conexion.conexion()
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


class DarResultado:
    def consultar(self):
        try:
            con = conexion.conexion()
            cursor = con.cursor()
            sql = "SELECT SUM(precio_total) FROM productos"
            cursor.execute(sql)
            result = cursor.fetchone()[0]
            showinfo(
                "Suma de Precios", f"El resultado de la suma de precios es: ${result}"
            )
        except sqlite3.Error as e:
            showerror("Error", f"Error al consultar los precios: {e}")


class EliminarProducto:
    def borrar(self, tree):
        valor = tree.selection()
        if valor:
            item = tree.item(valor)
            mi_id = item["text"]
            try:
                con = conexion.conexion()
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
