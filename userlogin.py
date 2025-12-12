import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
import re
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
        self.root.geometry("350x280")
        self.root.configure(bg="#2c3e50")
        self._usuario = None
        self._contrasena = None
        self.usuario_actual = None

        # Centrar ventana
        self.centrar_ventana()

        # Frame principal con padding
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Título
        titulo = tk.Label(
            main_frame,
            text="Sistema de Gestión",
            font=("Helvetica", 16, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1",
        )
        titulo.pack(pady=(0, 20))

        # Usuario
        self.label_usuario = tk.Label(
            main_frame,
            text="Usuario:",
            bg="#2c3e50",
            fg="#ecf0f1",
            font=("Helvetica", 10),
        )
        self.label_usuario.pack(anchor="w")
        self.entry_usuario = tk.Entry(main_frame, font=("Helvetica", 10), width=30)
        self.entry_usuario.pack(pady=(0, 10))
        self.entry_usuario.bind("<Return>", lambda e: self.entry_contrasena.focus())

        # Contraseña
        self.label_contrasena = tk.Label(
            main_frame,
            text="Contraseña:",
            bg="#2c3e50",
            fg="#ecf0f1",
            font=("Helvetica", 10),
        )
        self.label_contrasena.pack(anchor="w")
        self.entry_contrasena = tk.Entry(
            main_frame, show="●", font=("Helvetica", 10), width=30
        )
        self.entry_contrasena.pack(pady=(0, 20))
        self.entry_contrasena.bind("<Return>", lambda e: self.iniciar_sesion())

        # Frame para botones
        button_frame = tk.Frame(main_frame, bg="#2c3e50")
        button_frame.pack()

        # Botones con estilo
        self.boton_login = tk.Button(
            button_frame,
            text="Iniciar Sesión",
            command=self.iniciar_sesion,
            bg="#27ae60",
            fg="white",
            font=("Helvetica", 10, "bold"),
            width=15,
            cursor="hand2",
            relief="flat",
        )
        self.boton_login.pack(side="left", padx=5)

        self.boton_registro = tk.Button(
            button_frame,
            text="Registrarse",
            command=self.registrarse,
            bg="#3498db",
            fg="white",
            font=("Helvetica", 10, "bold"),
            width=15,
            cursor="hand2",
            relief="flat",
        )
        self.boton_registro.pack(side="left", padx=5)

        # Mensaje de requisitos
        self.label_info = tk.Label(
            main_frame,
            text="La contraseña debe tener al menos 6 caracteres",
            bg="#2c3e50",
            fg="#95a5a6",
            font=("Helvetica", 8),
        )
        self.label_info.pack(pady=(10, 0))

        self.conexion_usuarios = sqlite3.connect("usuarios.db")
        self.crear_tabla_usuarios()
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

        self.registrar_observador(InicioSesionObservador())
        self.registrar_observador(RegistroObservador())

    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    @staticmethod
    def hashear_contrasena(contrasena):
        """Hashea la contraseña usando SHA-256"""
        return hashlib.sha256(contrasena.encode()).hexdigest()

    @staticmethod
    def validar_usuario(usuario):
        """Valida el formato del usuario"""
        if len(usuario) < 3:
            return False, "El usuario debe tener al menos 3 caracteres"
        if not re.match("^[A-Za-z0-9_]+$", usuario):
            return (
                False,
                "El usuario solo puede contener letras, números y guiones bajos",
            )
        return True, ""

    @staticmethod
    def validar_contrasena(contrasena):
        """Valida la fortaleza de la contraseña"""
        if len(contrasena) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres"
        return True, ""

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
        self.usuario = self.entry_usuario.get().strip()
        self.contrasena = self.entry_contrasena.get()

        if not self.usuario or not self.contrasena:
            messagebox.showerror("Error", "Por favor, complete todos los campos")
            return

        contrasena_hash = self.hashear_contrasena(self.contrasena)

        if self.verificar_credenciales(self.usuario, contrasena_hash):
            self.usuario_actual = self.usuario
            self.notificar_observadores("inicio_sesion", self.usuario)
            self.abrir_ventana_principal()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")
            self.entry_contrasena.delete(0, tk.END)

    def registrarse(self):
        self.usuario = self.entry_usuario.get().strip()
        self.contrasena = self.entry_contrasena.get()

        # Validar usuario
        valido, mensaje = self.validar_usuario(self.usuario)
        if not valido:
            messagebox.showerror("Error", mensaje)
            return

        # Validar contraseña
        valido, mensaje = self.validar_contrasena(self.contrasena)
        if not valido:
            messagebox.showerror("Error", mensaje)
            return

        try:
            cursor = self.conexion_usuarios.cursor()

            # Verificar si el usuario ya existe
            cursor.execute(
                "SELECT usuario FROM usuarios WHERE usuario=?", (self.usuario,)
            )
            if cursor.fetchone():
                messagebox.showerror(
                    "Error", "El usuario ya existe. Por favor, elija otro nombre"
                )
                return

            contrasena_hash = self.hashear_contrasena(self.contrasena)

            cursor.execute(
                "INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)",
                (self.usuario, contrasena_hash),
            )
            self.conexion_usuarios.commit()
            messagebox.showinfo(
                "Registro Exitoso",
                f"¡Bienvenido {self.usuario}!\nUsuario registrado correctamente",
            )
            self.usuario_actual = self.usuario
            self.notificar_observadores("registro", self.usuario)
            self.iniciar_aplicacion_principal()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar el usuario: {e}")

    def verificar_credenciales(self, usuario, contrasena_hash):
        try:
            cursor = self.conexion_usuarios.cursor()
            cursor.execute(
                "SELECT * FROM usuarios WHERE usuario=? AND contrasena=?",
                (usuario, contrasena_hash),
            )
            result = cursor.fetchone()
            return result is not None
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo verificar las credenciales: {e}")
            return False

    def abrir_ventana_principal(self):
        self.conexion_usuarios.close()
        self.root.destroy()
        base.iniciar_aplicacion()

    def iniciar_aplicacion_principal(self):
        self.conexion_usuarios.close()
        self.root.destroy()
        base.iniciar_aplicacion()

    def crear_tabla_usuarios(self):
        try:
            cursor = self.conexion_usuarios.cursor()
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS usuarios
                              (id INTEGER PRIMARY KEY AUTOINCREMENT,
                              usuario VARCHAR(50) NOT NULL UNIQUE,
                              contrasena VARCHAR(64) NOT NULL,
                              fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"""
            )
            self.conexion_usuarios.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo crear la tabla de usuarios: {e}")

    def cerrar_ventana(self):
        if messagebox.askyesno("Salir", "¿Estás seguro que quieres salir?"):
            self.conexion_usuarios.close()
            self.root.destroy()


if __name__ == "__main__":
    iniciar_logueo()
