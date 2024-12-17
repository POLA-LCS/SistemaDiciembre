# Plantilla para los mensajes de ERROR, FALLO y EXITO
def plantilla_mensaje(prefijo: str, mensaje: str, presionar = False):
    print(prefijo, mensaje)
    if presionar:
        input('...')

def ERROR(mensaje: str, presionar = True):
    plantilla_mensaje('[ERROR]', mensaje, presionar)

def FALLO(mensaje: str, presionar = True):
    plantilla_mensaje('[!]', mensaje, presionar)
    
def EXITO(mensaje: str, presionar = True):
    plantilla_mensaje('[O]', mensaje, presionar)