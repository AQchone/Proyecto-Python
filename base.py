from tabla import creaTabla
import controlador
import vista


def iniciar_aplicacion():
    creaTabla()
    vista.inicializar_vista()
    controlador()


if __name__ == "__main__":
    iniciar_aplicacion()
