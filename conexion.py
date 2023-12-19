import sqlite3
from tkinter.messagebox import showerror


def conexion():
    try:
        con = sqlite3.connect("mibase.db")
        return con
    except sqlite3.Error as e:
        mensaje_error = f"Error al conectar a la base de datos: {e}"
        showerror("Error de conexión", mensaje_error)
        return None


mi_conexion = conexion()
if mi_conexion:
    print("Conexión exitosa")
else:
    print("No se pudo establecer la conexión")
