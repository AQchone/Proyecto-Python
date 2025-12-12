import sqlite3
from tkinter.messagebox import showerror


class ConexionDB:
    """Singleton para manejar la conexión a la base de datos"""

    _instancia = None
    _conexion = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(ConexionDB, cls).__new__(cls)
        return cls._instancia

    def obtener_conexion(self, nombre_db="mibase.db"):
        """Obtiene o crea una conexión a la base de datos"""
        try:
            if self._conexion is None:
                self._conexion = sqlite3.connect(nombre_db)
            return self._conexion
        except sqlite3.Error as e:
            mensaje_error = f"Error al conectar a la base de datos: {e}"
            showerror("Error de conexión", mensaje_error)
            return None

    def cerrar_conexion(self):
        """Cierra la conexión actual"""
        if self._conexion:
            self._conexion.close()
            self._conexion = None


def conexion():
    """Función de compatibilidad con código anterior"""
    db = ConexionDB()
    return db.obtener_conexion()


# Inicialización
if __name__ == "__main__":
    mi_conexion = conexion()
    if mi_conexion:
        print("Conexión exitosa")
    else:
        print("No se pudo establecer la conexión")
