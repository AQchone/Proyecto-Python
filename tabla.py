import sqlite3
from tkinter.messagebox import showerror
import conexion


def crear_tabla():
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
    except sqlite3.Error as e:
        showerror("Error", f"Error al crear la tabla: {e}")
