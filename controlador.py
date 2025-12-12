import re
import sqlite3
from tkinter.messagebox import showerror, showinfo
import conexion
import csv
from datetime import datetime


class AgregarProducto:
    def __init__(self):
        self.default_patron = "^[A-Za-zÀ-ÿ0-9\s]+$"

    def alta(self, producto, cantidad, precio_unitario, descuento, tree):
        """Agrega un producto con validación mejorada"""
        cadena = producto.strip()

        # Validaciones
        if not cadena:
            showerror("Error", "El nombre del producto no puede estar vacío")
            return False

        if len(cadena) < 2:
            showerror(
                "Error", "El nombre del producto debe tener al menos 2 caracteres"
            )
            return False

        patron = self.default_patron
        if not re.match(patron, cadena):
            showerror(
                "Error", "El producto solo puede contener letras, números y espacios"
            )
            return False

        # Validar números
        try:
            cantidad = float(cantidad)
            precio_unitario = float(precio_unitario)
            descuento = float(descuento)

            if cantidad <= 0:
                showerror("Error", "La cantidad debe ser mayor a 0")
                return False
            if precio_unitario <= 0:
                showerror("Error", "El precio unitario debe ser mayor a 0")
                return False
            if descuento < 0 or descuento > 100:
                showerror("Error", "El descuento debe estar entre 0 y 100")
                return False

        except ValueError:
            showerror("Error", "Por favor ingrese valores numéricos válidos")
            return False

        try:
            con = conexion.conexion()
            cursor = con.cursor()
            precio_total = cantidad * precio_unitario * (1 - descuento / 100)
            data = (cadena, cantidad, precio_unitario, precio_total)
            sql = "INSERT INTO productos(producto, cantidad, precio_unitario, precio_total) VALUES(?, ?, ?, ?)"
            cursor.execute(sql, data)
            con.commit()

            # Registrar en historial
            self.registrar_historial(
                cursor.lastrowid, "AGREGAR", f"Producto: {cadena}, Cantidad: {cantidad}"
            )
            con.commit()

            self.actualizar_treeview(tree)
            showinfo("Éxito", f"Producto '{cadena}' agregado correctamente")
            return True
        except sqlite3.Error as e:
            showerror("Error", f"Error al dar de alta el producto: {e}")
            return False

    def actualizar_treeview(self, mitreview):
        """Actualiza el treeview con los datos de la base de datos"""
        mitreview.delete(*mitreview.get_children())
        try:
            con = conexion.conexion()
            cursor = con.cursor()
            sql = "SELECT * FROM productos ORDER BY id DESC"
            datos = cursor.execute(sql)
            resultado = datos.fetchall()
            for fila in resultado:
                # Formatear valores monetarios
                precio_unit = f"${fila[3]:.2f}"
                precio_tot = f"${fila[4]:.2f}"
                mitreview.insert(
                    "",
                    0,
                    text=fila[0],
                    values=(fila[1], fila[2], precio_unit, precio_tot),
                )
        except sqlite3.Error as e:
            showerror("Error", f"Error al actualizar el treeview: {e}")

    def registrar_historial(self, producto_id, accion, detalles):
        """Registra acciones en el historial"""
        try:
            con = conexion.conexion()
            cursor = con.cursor()
            sql = "INSERT INTO historial(producto_id, accion, detalles) VALUES(?, ?, ?)"
            cursor.execute(sql, (producto_id, accion, detalles))
            con.commit()
        except sqlite3.Error:
            pass  # No es crítico si falla el historial


class EditarProducto:
    def __init__(self):
        self.patron = "^[A-Za-zÀ-ÿ0-9\s]+$"

    def editar(self, tree, producto, cantidad, precio_unitario, descuento):
        """Edita un producto existente"""
        valor = tree.selection()
        if not valor:
            showerror("Error", "Debe seleccionar un producto para editar")
            return False

        item = tree.item(valor)
        mi_id = item["text"]

        # Validaciones
        producto = producto.strip()
        if not producto or not re.match(self.patron, producto):
            showerror("Error", "Nombre de producto inválido")
            return False

        try:
            cantidad = float(cantidad)
            precio_unitario = float(precio_unitario)
            descuento = float(descuento)

            if cantidad <= 0 or precio_unitario <= 0:
                showerror("Error", "Cantidad y precio deben ser mayores a 0")
                return False
            if descuento < 0 or descuento > 100:
                showerror("Error", "El descuento debe estar entre 0 y 100")
                return False

        except ValueError:
            showerror("Error", "Valores numéricos inválidos")
            return False

        try:
            con = conexion.conexion()
            cursor = con.cursor()
            precio_total = cantidad * precio_unitario * (1 - descuento / 100)

            sql = """UPDATE productos 
                     SET producto=?, cantidad=?, precio_unitario=?, precio_total=?, 
                         fecha_modificacion=CURRENT_TIMESTAMP 
                     WHERE id=?"""
            cursor.execute(
                sql, (producto, cantidad, precio_unitario, precio_total, mi_id)
            )
            con.commit()

            showinfo("Éxito", f"Producto ID {mi_id} actualizado correctamente")
            return True
        except sqlite3.Error as e:
            showerror("Error", f"Error al editar el producto: {e}")
            return False


class DarResultado:
    def __init__(self):
        self.resultado = 0

    def consultar(self):
        """Muestra el total de todos los productos"""
        try:
            con = conexion.conexion()
            cursor = con.cursor()

            # Obtener suma total
            sql = "SELECT SUM(precio_total) FROM productos"
            cursor.execute(sql)
            resultado = cursor.fetchone()[0]

            # Obtener cantidad de productos
            sql_count = "SELECT COUNT(*) FROM productos"
            cursor.execute(sql_count)
            cantidad_productos = cursor.fetchone()[0]

            if resultado is None or resultado == 0:
                showinfo("Total de Inventario", "No hay productos en el inventario")
            else:
                mensaje = f"Total de productos: {cantidad_productos}\n"
                mensaje += f"Suma total del inventario: ${resultado:.2f}"
                showinfo("Total de Inventario", mensaje)

            self.resultado = resultado if resultado else 0
        except sqlite3.Error as e:
            showerror("Error", f"Error al consultar los precios: {e}")

    def calcular_estadisticas(self):
        """Calcula estadísticas del inventario"""
        try:
            con = conexion.conexion()
            cursor = con.cursor()

            sql = """SELECT 
                        COUNT(*) as total_productos,
                        SUM(cantidad) as total_unidades,
                        SUM(precio_total) as valor_total,
                        AVG(precio_total) as promedio,
                        MAX(precio_total) as maximo,
                        MIN(precio_total) as minimo
                     FROM productos"""
            cursor.execute(sql)
            stats = cursor.fetchone()

            if stats[0] == 0:
                showinfo("Estadísticas", "No hay productos en el inventario")
                return

            mensaje = f"""═══════════════════════════════════
ESTADÍSTICAS DEL INVENTARIO
═══════════════════════════════════
Total de productos: {stats[0]}
Total de unidades: {stats[1]:.0f}
Valor total: ${stats[2]:.2f}
Promedio por producto: ${stats[3]:.2f}
Producto más caro: ${stats[4]:.2f}
Producto más barato: ${stats[5]:.2f}
═══════════════════════════════════"""

            showinfo("Estadísticas del Inventario", mensaje)
        except sqlite3.Error as e:
            showerror("Error", f"Error al calcular estadísticas: {e}")


class EliminarProducto:
    def borrar(self, tree):
        """Elimina un producto con confirmación"""
        valor = tree.selection()
        if valor:
            item = tree.item(valor)
            mi_id = item["text"]
            nombre_producto = item["values"][0] if item["values"] else "producto"

            from tkinter import messagebox

            if not messagebox.askyesno(
                "Confirmar", f"¿Está seguro de eliminar '{nombre_producto}'?"
            ):
                return False

            try:
                con = conexion.conexion()
                cursor = con.cursor()
                data = (mi_id,)
                sql = "DELETE FROM productos WHERE id = ?"
                cursor.execute(sql, data)
                con.commit()
                tree.delete(valor)
                showinfo("Éxito", "Producto eliminado correctamente")
                return True
            except sqlite3.Error as e:
                showerror("Error", f"Error al borrar el producto: {e}")
                return False
        else:
            showerror("Error", "Debe seleccionar un producto para borrar")
            return False


class BuscarProducto:
    def buscar(self, termino, tree):
        """Busca productos por nombre"""
        tree.delete(*tree.get_children())

        if not termino.strip():
            # Si no hay término, mostrar todos
            agregar = AgregarProducto()
            agregar.actualizar_treeview(tree)
            return

        try:
            con = conexion.conexion()
            cursor = con.cursor()
            sql = "SELECT * FROM productos WHERE producto LIKE ? ORDER BY id DESC"
            cursor.execute(sql, (f"%{termino}%",))
            resultado = cursor.fetchall()

            if not resultado:
                showinfo("Búsqueda", f"No se encontraron productos con '{termino}'")
                return

            for fila in resultado:
                precio_unit = f"${fila[3]:.2f}"
                precio_tot = f"${fila[4]:.2f}"
                tree.insert(
                    "",
                    0,
                    text=fila[0],
                    values=(fila[1], fila[2], precio_unit, precio_tot),
                )

            showinfo("Búsqueda", f"Se encontraron {len(resultado)} producto(s)")
        except sqlite3.Error as e:
            showerror("Error", f"Error al buscar productos: {e}")


class ExportarDatos:
    def exportar_csv(self):
        """Exporta los productos a un archivo CSV"""
        try:
            con = conexion.conexion()
            cursor = con.cursor()
            cursor.execute("SELECT * FROM productos ORDER BY id ASC")
            productos = cursor.fetchall()

            if not productos:
                showinfo("Exportar", "No hay productos para exportar")
                return False

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"productos_export_{timestamp}.csv"

            with open(nombre_archivo, "w", newline="", encoding="utf-8") as archivo:
                writer = csv.writer(archivo)
                writer.writerow(
                    ["ID", "Producto", "Cantidad", "Precio Unitario", "Precio Total"]
                )
                writer.writerows(productos)

            showinfo("Éxito", f"Datos exportados correctamente a:\n{nombre_archivo}")
            return True
        except Exception as e:
            showerror("Error", f"Error al exportar datos: {e}")
            return False
