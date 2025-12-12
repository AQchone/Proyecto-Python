from tabla import creaTabla
import vista


def iniciar_aplicacion():
    """Inicializa la aplicación principal"""
    # Crear tablas si no existen
    tabla = creaTabla()
    tabla.crear_tabla()
    tabla.agregar_columna_usuario()
    tabla.crear_tabla_historial()

    # Iniciar la interfaz gráfica
    vista.inicializar_vista()


if __name__ == "__main__":
    iniciar_aplicacion()
