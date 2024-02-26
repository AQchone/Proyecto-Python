import tkinter as tk
from tkinter import messagebox
import sqlite3
import base


class Observador:
    def actualizar(self, evento, datos):
        pass


class InicioSesionObservador(Observador):
    def actualizar(self, evento, datos):
        print(f"Se ha iniciado sesión con el usuario: {datos}")


class RegistroObservador(Observador):
    def actualizar(self, evento, datos):
        print(f"Bienvenido {datos}")


class Sujeto:
    def __init__(self):
        self.observadores = []

    def registrar_observador(self, observador):
        self.observadores.append(observador)

    def eliminar_observador(self, observador):
        self.observadores.remove(observador)

    def notificar_observadores(self, evento, datos):
        for observador in self.observadores:
            observador.actualizar(evento, datos)


def iniciar_logueo():
    root = tk.Tk()
    LoginRegistroVentana(root)
    root.mainloop()


class LoginRegistroVentana(Sujeto):
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.root.title("Inicio de Sesión / Registro")
        self.root.geometry("200x160")
        self._usuario = None
        self._contrasena = None

        self.label_usuario = tk.Label(self.root, text="Usuario:")
        self.label_usuario.pack()
        self.entry_usuario = tk.Entry(self.root)
        self.entry_usuario.pack()

        self.label_contrasena = tk.Label(self.root, text="Contraseña:")
        self.label_contrasena.pack()
        self.entry_contrasena = tk.Entry(self.root, show="*")
        self.entry_contrasena.pack()

        self.boton_login = tk.Button(
            self.root, text="Iniciar Sesión", command=self.iniciar_sesion
        )
        self.boton_login.pack()

        self.boton_registro = tk.Button(
            self.root, text="Registrarse", command=self.registrarse
        )
        self.boton_registro.pack()

        self.conexion_usuarios = sqlite3.connect("usuarios.db")

        self.crear_tabla_usuarios()

        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

        self.registrar_observador(InicioSesionObservador())
        self.registrar_observador(RegistroObservador())

    @property
    def usuario(self):
        return self._usuario

    @usuario.setter
    def usuario(self, value):
        self._usuario = value

    @property
    def contrasena(self):
        return self._contrasena

    @contrasena.setter
    def contrasena(self, value):
        self._contrasena = value

    def iniciar_sesion(self):
        self.usuario = self.entry_usuario.get()
        self.contrasena = self.entry_contrasena.get()

        if self.verificar_credenciales(self.usuario, self.contrasena):
            self.notificar_observadores("inicio_sesion", self.usuario)
            self.abrir_ventana_principal()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    def registrarse(self):
        self.usuario = self.entry_usuario.get()
        self.contrasena = self.entry_contrasena.get()

        if self.usuario and self.contrasena:
            try:
                cursor = self.conexion_usuarios.cursor()
                cursor.execute(
                    "INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)",
                    (self.usuario, self.contrasena),
                )
                self.conexion_usuarios.commit()
                messagebox.showinfo("Registro", "Usuario registrado exitosamente")
                self.notificar_observadores("registro", self.usuario)
                self.iniciar_aplicacion_principal()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"No se pudo registrar el usuario: {e}")
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos")

    def verificar_credenciales(self, usuario, contrasena):
        try:
            cursor = self.conexion_usuarios.cursor()
            cursor.execute(
                "SELECT * FROM usuarios WHERE usuario=? AND contrasena=?",
                (usuario, contrasena),
            )
            result = cursor.fetchone()
            return result is not None
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo verificar las credenciales: {e}")
            return False

    def abrir_ventana_principal(self):
        self.root.destroy()
        base.iniciar_aplicacion()

    def iniciar_aplicacion_principal(self):
        self.root.destroy()
        base.iniciar_aplicacion()

    def crear_tabla_usuarios(self):
        try:
            cursor = self.conexion_usuarios.cursor()
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS usuarios
                              (id INTEGER PRIMARY KEY AUTOINCREMENT,
                              usuario VARCHAR(50) NOT NULL,
                              contrasena VARCHAR(50) NOT NULL)"""
            )
            self.conexion_usuarios.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo crear la tabla de usuarios: {e}")

    def cerrar_ventana(self):
        if messagebox.askyesno("Salir", "¿Estás seguro que quieres salir?"):
            self.root.destroy()
        else:
            return


if __name__ == "__main__":
    iniciar_logueo()
