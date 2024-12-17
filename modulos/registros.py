Registro = tuple[str, ...]

# Devuelve los datos en una lista de registros limpios de espacios en blanco
def obtener_registros(dir: str) -> (list[Registro] | None):
    try:
        with open(dir, 'r') as file:
            return [tuple([dato.strip() for dato in registro.split(',')]) for registro in file.readlines()]
    except:
        return None
    
# Escribe un registro (str, ...) separado por coma "dato1, dato2, dato3"
def escribir_registros(dir: str, registros: list[Registro]):
    try:
        with open(dir, 'a') as file:
            for registro in registros:
                file.write(', '.join(registro) + '\n')
        return True
    except:
        return False