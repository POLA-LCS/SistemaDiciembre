valor_codigo_error = 0
def codigo_error():
    global valor_codigo_error
    valor_codigo_error += 1
    return valor_codigo_error

def pedir_id():
    id = input('ID >> ')
    try:
        int(id)
        return id
    except:
        return None

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