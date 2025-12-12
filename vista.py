import tkinter as tk
from tkinter import ttk, messagebox
from tabla import creaTabla
from controlador import (
    AgregarProducto,
    DarResultado,
    EliminarProducto,
    EditarProducto,
    BuscarProducto,
    ExportarDatos,
)


class Vista:
    def __init__(self):
        self.root = None
        self.style = None
        self.tree = None
        self.tema_oscuro = False

        # Variables de entrada
        self.a_val = None
        self.b_val = None
        self.c_val = None
        self.d_val = None

        # Controladores
        self.agregar_producto = AgregarProducto()
        self.eliminar_producto = EliminarProducto()
        self.editar_producto = EditarProducto()
        self.dar_resultado = DarResultado()
        self.buscar_producto = BuscarProducto()
        self.exportar_datos = ExportarDatos()

    def actualizar_treeview(self):
        self.agregar_producto.actualizar_treeview(self.tree)

    def cambiar_tema(self):
        """Alterna entre tema claro y oscuro"""
        self.tema_oscuro = not self.tema_oscuro

        if self.tema_oscuro:
            bg_root = "#2c3e50"
            tree_bg = "#2c3e50"
            tree_fg = "#ecf0f1"

        else:
            bg_root = "#ecf0f1"
            tree_bg = "#ffffff"
            tree_fg = "#2c3e50"

        self.root.configure(background=bg_root)

        # Actualizar estilo del treeview
        self.style.configure(
            "Treeview",
            background=tree_bg,
            fieldbackground=tree_bg,
            foreground=tree_fg,
            rowheight=25,
        )
        self.style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))

    def limpiar_campos(self):
        """Limpia todos los campos de entrada"""
        self.a_val.set("")
        self.b_val.set(0.0)
        self.c_val.set(0.0)
        self.d_val.set(0.0)

    def cargar_producto_seleccionado(self):
        """Carga los datos del producto seleccionado en los campos"""
        valor = self.tree.selection()
        if not valor:
            messagebox.showwarning("Advertencia", "Debe seleccionar un producto")
            return

        item = self.tree.item(valor)
        valores = item["values"]

        if valores:
            self.a_val.set(valores[0])
            self.b_val.set(valores[1])
            # Limpiar el símbolo $ del precio
            precio_str = str(valores[2]).replace("$", "")
            self.c_val.set(float(precio_str))
            self.d_val.set(0.0)  # Descuento no se guarda

    def agregar_con_limpieza(self):
        """Agrega producto y limpia campos si fue exitoso"""
        if self.agregar_producto.alta(
            self.a_val.get(),
            self.b_val.get(),
            self.c_val.get(),
            self.d_val.get(),
            self.tree,
        ):
            self.limpiar_campos()

    def editar_producto_seleccionado(self):
        """Edita el producto seleccionado"""
        if self.editar_producto.editar(
            self.tree,
            self.a_val.get(),
            self.b_val.get(),
            self.c_val.get(),
            self.d_val.get(),
        ):
            self.actualizar_treeview()
            self.limpiar_campos()

    def buscar(self):
        """Abre ventana de búsqueda"""
        ventana_busqueda = tk.Toplevel(self.root)
        ventana_busqueda.title("Buscar Producto")
        ventana_busqueda.geometry("300x100")
        ventana_busqueda.configure(bg="#ecf0f1")

        tk.Label(ventana_busqueda, text="Buscar:", bg="#ecf0f1").pack(pady=10)
        entrada_busqueda = tk.Entry(ventana_busqueda, width=30)
        entrada_busqueda.pack(pady=5)
        entrada_busqueda.focus()

        def realizar_busqueda():
            self.buscar_producto.buscar(entrada_busqueda.get(), self.tree)
            ventana_busqueda.destroy()

        entrada_busqueda.bind("<Return>", lambda e: realizar_busqueda())

        tk.Button(
            ventana_busqueda,
            text="Buscar",
            command=realizar_busqueda,
            bg="#3498db",
            fg="white",
        ).pack(pady=5)

    def cerrar_ventana(self):
        if messagebox.askyesno("Salir", "¿Estás seguro que quieres salir?"):
            self.root.destroy()

    def crear_interfaz(self):
        self.root = tk.Tk()
        self.root.configure(background="#ecf0f1")
        self.root.title("Sistema de Gestión de Productos")
        self.root.geometry("1000x650")

        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

        self.style = ttk.Style(self.root)
        self.style.theme_use("clam")
        self.style.configure("Treeview", rowheight=25)
        self.style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))

        # Frame principal con dos columnas
        main_frame = tk.Frame(self.root, bg="#ecf0f1")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Columna izquierda - Formulario
        left_frame = tk.Frame(main_frame, bg="#ecf0f1")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # Título
        titulo = tk.Label(
            left_frame,
            text="📦 Gestión de Productos",
            bg="#3498db",
            fg="white",
            font=("Helvetica", 16, "bold"),
            height=2,
        )
        titulo.pack(fill="x", pady=(0, 20))

        # Frame de entrada de datos
        form_frame = tk.LabelFrame(
            left_frame,
            text="Datos del Producto",
            bg="#ecf0f1",
            font=("Helvetica", 10, "bold"),
            padx=15,
            pady=15,
        )
        form_frame.pack(fill="x", pady=(0, 10))

        # Variables
        self.a_val = tk.StringVar()
        self.b_val = tk.DoubleVar()
        self.c_val = tk.DoubleVar()
        self.d_val = tk.DoubleVar()

        # Campos de entrada
        campos = [
            ("Producto:", self.a_val, "text"),
            ("Cantidad:", self.b_val, "number"),
            ("Precio Unitario ($):", self.c_val, "number"),
            ("Descuento (%):", self.d_val, "number"),
        ]

        for i, (label_text, variable, tipo) in enumerate(campos):
            tk.Label(
                form_frame, text=label_text, bg="#ecf0f1", font=("Helvetica", 9)
            ).grid(row=i, column=0, sticky="w", pady=5)

            entrada = tk.Entry(
                form_frame, textvariable=variable, width=25, font=("Helvetica", 9)
            )
            entrada.grid(row=i, column=1, sticky="ew", pady=5)

        form_frame.columnconfigure(1, weight=1)

        # Frame de botones de acción
        button_frame = tk.LabelFrame(
            left_frame,
            text="Acciones",
            bg="#ecf0f1",
            font=("Helvetica", 10, "bold"),
            padx=15,
            pady=15,
        )
        button_frame.pack(fill="x", pady=(0, 10))

        botones = [
            ("➕ Agregar", self.agregar_con_limpieza, "#27ae60"),
            ("✏️ Editar", self.editar_producto_seleccionado, "#f39c12"),
            ("🗑️ Borrar", lambda: self.eliminar_producto.borrar(self.tree), "#e74c3c"),
            ("🔍 Buscar", self.buscar, "#3498db"),
            ("📋 Cargar Datos", self.cargar_producto_seleccionado, "#9b59b6"),
            ("🧹 Limpiar", self.limpiar_campos, "#95a5a6"),
        ]

        for i, (texto, comando, color) in enumerate(botones):
            btn = tk.Button(
                button_frame,
                text=texto,
                command=comando,
                bg=color,
                fg="white",
                font=("Helvetica", 9, "bold"),
                cursor="hand2",
                relief="flat",
                padx=10,
                pady=5,
            )
            btn.grid(row=i // 2, column=i % 2, sticky="ew", padx=5, pady=5)

        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        # Frame de operaciones
        ops_frame = tk.LabelFrame(
            left_frame,
            text="Operaciones",
            bg="#ecf0f1",
            font=("Helvetica", 10, "bold"),
            padx=15,
            pady=15,
        )
        ops_frame.pack(fill="x")

        operaciones = [
            ("💰 Total Inventario", self.dar_resultado.consultar, "#16a085"),
            ("📊 Estadísticas", self.dar_resultado.calcular_estadisticas, "#2980b9"),
            ("💾 Exportar CSV", self.exportar_datos.exportar_csv, "#8e44ad"),
            ("🎨 Cambiar Tema", self.cambiar_tema, "#34495e"),
        ]

        for i, (texto, comando, color) in enumerate(operaciones):
            btn = tk.Button(
                ops_frame,
                text=texto,
                command=comando,
                bg=color,
                fg="white",
                font=("Helvetica", 9, "bold"),
                cursor="hand2",
                relief="flat",
                padx=10,
                pady=5,
            )
            btn.grid(row=i // 2, column=i % 2, sticky="ew", padx=5, pady=5)

        ops_frame.columnconfigure(0, weight=1)
        ops_frame.columnconfigure(1, weight=1)

        # Columna derecha - Tabla
        right_frame = tk.Frame(main_frame, bg="#ecf0f1")
        right_frame.grid(row=0, column=1, sticky="nsew")

        # Título de la tabla
        titulo_tabla = tk.Label(
            right_frame,
            text="📋 Lista de Productos",
            bg="#2c3e50",
            fg="white",
            font=("Helvetica", 12, "bold"),
            height=2,
        )
        titulo_tabla.pack(fill="x")

        # Frame para el treeview y scrollbar
        tree_frame = tk.Frame(right_frame, bg="#ecf0f1")
        tree_frame.pack(fill="both", expand=True, pady=10)

        # Scrollbar
        scrollbar = tk.Scrollbar(tree_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        # Treeview
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("col1", "col2", "col3", "col4"),
            yscrollcommand=scrollbar.set,
        )
        self.tree.pack(fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)

        # Configurar columnas
        self.tree.column("#0", width=50, minwidth=50, anchor="center")
        self.tree.column("col1", width=150, minwidth=100)
        self.tree.column("col2", width=100, minwidth=80, anchor="center")
        self.tree.column("col3", width=120, minwidth=100, anchor="center")
        self.tree.column("col4", width=120, minwidth=100, anchor="center")

        self.tree.heading("#0", text="ID")
        self.tree.heading("col1", text="Producto")
        self.tree.heading("col2", text="Cantidad")
        self.tree.heading("col3", text="Precio Unit.")
        self.tree.heading("col4", text="Precio Total")

        # Configurar grid weights
        main_frame.columnconfigure(0, weight=2, minsize=350)
        main_frame.columnconfigure(1, weight=3)
        main_frame.rowconfigure(0, weight=1)

        # Cargar datos iniciales
        creaTabla()
        self.actualizar_treeview()

        self.root.mainloop()


def inicializar_vista():
    """Función de compatibilidad con el código anterior"""
    vista = Vista()
    vista.crear_interfaz()


if __name__ == "__main__":
    inicializar_vista()
