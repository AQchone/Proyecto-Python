import sqlite3
from tkinter.messagebox import showerror
import conexion


class creaTabla:
    def crear_tabla(self):
        try:
            con = conexion.conexion()
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
            con.close()
        except sqlite3.Error as e:
            showerror("Error", f"Error al crear la tabla: {e}")


tabla = creaTabla()
tabla.crear_tabla()
