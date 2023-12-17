import sqlite3
from tkinter.messagebox import showerror


def conexion():
    try:
        con = sqlite3.connect("mibase.db")
        return con
    except sqlite3.Error as e:
        showerror("Error", f"Error al conectar a la base de datos: {e}")
