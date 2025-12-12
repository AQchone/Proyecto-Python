import sqlite3
from tkinter.messagebox import showerror
import conexion


class creaTabla:
    def crear_tabla(self):
        """Crea la tabla de productos con campos mejorados"""
        try:
            con = conexion.conexion()
            cursor = con.cursor()
            sql = """CREATE TABLE IF NOT EXISTS productos
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     producto varchar(50) NOT NULL,
                     cantidad real NOT NULL CHECK(cantidad >= 0),
                     precio_unitario real NOT NULL CHECK(precio_unitario >= 0),
                     precio_total real NOT NULL,
                     fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                     fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
            """
            cursor.execute(sql)

            # Crear índice para búsquedas más rápidas
            cursor.execute(
                """CREATE INDEX IF NOT EXISTS idx_producto 
                           ON productos(producto)"""
            )

            con.commit()
        except sqlite3.Error as e:
            showerror("Error", f"Error al crear la tabla: {e}")

    def agregar_columna_usuario(self):
        """Agrega columna para asociar productos con usuarios"""
        try:
            con = conexion.conexion()
            cursor = con.cursor()

            # Verificar si la columna ya existe
            cursor.execute("PRAGMA table_info(productos)")
            columnas = [col[1] for col in cursor.fetchall()]

            if "usuario_id" not in columnas:
                cursor.execute(
                    """ALTER TABLE productos 
                               ADD COLUMN usuario_id INTEGER"""
                )
                con.commit()
        except sqlite3.Error:
            # Si la columna ya existe, no es un error crítico
            pass

    def crear_tabla_historial(self):
        """Crea tabla para historial de cambios"""
        try:
            con = conexion.conexion()
            cursor = con.cursor()
            sql = """CREATE TABLE IF NOT EXISTS historial
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     producto_id INTEGER,
                     accion varchar(20),
                     usuario varchar(50),
                     detalles TEXT,
                     fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
            """
            cursor.execute(sql)
            con.commit()
        except sqlite3.Error as e:
            showerror("Error", f"Error al crear tabla de historial: {e}")


# Inicialización automática
tabla = creaTabla()
tabla.crear_tabla()
tabla.agregar_columna_usuario()
tabla.crear_tabla_historial()
