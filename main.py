from modulos import *
from datetime import datetime as date, timedelta
from os import system

FORMATO_HORA = '%H:%M:%S'
FORMATO_FECHA = '%Y_%m'

# Obtiene la hora actual del sistema
def obtener_hora_actual():
    return date.now().strftime(FORMATO_HORA)

# False = entrada
def obtener_archivo_id(id: str, entrada_salida: bool):
    return (DIR_SALIDAS if entrada_salida else DIR_ENTRADAS) / f'{date.now().strftime(FORMATO_FECHA)}_{id}_{(NOMBRE_SALIDAS if entrada_salida else NOMBRE_ENTRADAS)}'

# Registra la hora de entrada y salida
def registrar_entrada_salida(id: str, entrada_salida: bool):
    nombre_archivo = obtener_archivo_id(id, entrada_salida)
    fecha_hora = (date.now().strftime('%d'), obtener_hora_actual())
    resultado = escribir_registros(nombre_archivo, [fecha_hora])
    return fecha_hora if resultado else None

# Calcula las horas trabajas en base a la suma de las diferencias entre las salidas y las entradas
def calcular_horas_trabajadas(entradas: list[Registro], salidas: list[Registro]):
    if len(salidas) == 0:
        return None
    horas = timedelta()
    for i, salida in enumerate(salidas):
        horas += (date.strptime(salida[1], FORMATO_HORA) - date.strptime(entradas[i][1], FORMATO_HORA))
    return horas

# MENU DE INICIO DE SESION
def mostrar_menu_inicio():
    print('1. Ingresar')
    print('2. Salir')

# MENU SI YA SE INICIO SESION
def mostrar_menu():
    print('1. Entrada')
    print('2. Salida')
    print('3. Horas trabajadas')
    print('4. Dias presentes')
    print('5. Salir')

def main():
    # Cargar archivo de empleados
    if not ARC_EMPLEADOS.exists():
        ERROR(f'Obteniendo los empleados | El archivo "{ARC_EMPLEADOS}" no existe.\n')
        return codigo_error()
    
    if (registros_empleados := obtener_registros(ARC_EMPLEADOS)) is None:
        ERROR(f'No se pudo leer el archivo "{ARC_EMPLEADOS}"')
        return codigo_error()
        
    # Cargar archivo de sus contraseñas
    if not ARC_CONTRASENAS.exists():
        ERROR(f'Obteniendo las contraseñas | El archivo "{ARC_CONTRASENAS}"')
        return codigo_error()
    
    if (registros_contrasenas := obtener_registros(ARC_CONTRASENAS)) is None:
        ERROR(f'No se pudo leer el archivo {ARC_CONTRASENAS}')
        return codigo_error()
    
    empleados:    dict[str, Empleado] = {}
    empleados_id: dict[str, str]      = {} # Mapa inverso
    contrasenas:  dict[str, str]      = {}
    
    # Carga de los empleados y sus ids con un mapa inverso
    for i, registro in enumerate(registros_empleados):
        if len(registro) != 5:
            ERROR(f'En "{ARC_EMPLEADOS}" | El registro {i + 1} -> "{', '.join(registro)}" no tiene el formato correcto.')
            print('    Formato: ID, DNI, NOMBRES, APELLIDOS, FECHA DE NACIMIENTO')
            return codigo_error()

        id, dni, datos = registro[0], registro[1], registro[2:]
        empleados[id]     = Empleado(id, dni, *datos)
        empleados_id[dni] = id
        
        if empleados[id].rango is None:
            ERROR(f'En "{ARC_EMPLEADOS}" | El registro {i + 1} no tiene un ID valido')
            return codigo_error()
        
    # Carga de las contraseñas
    for i, registro in enumerate(registros_contrasenas):
        if len(registro) != 2:
            ERROR(f'En "{ARC_CONTRASENAS}" | El registro {i + 1} no tiene el formato correcto.')
            print('    Formato: DNI, CONTRASEÑA')
            return codigo_error()
        
        dni, contrasena = registro
        if dni not in empleados_id:
            ERROR(f'En "{ARC_CONTRASENAS}" |"{dni}" no cohincide con ningun empleado en el sistema.\n')
            return codigo_error()
        contrasenas[dni] = contrasena
        
    # LOOP PRINCIPAL
    usuario = None
    while True:
        if usuario is None:
            system('cls')
            print('[INICIO DE SESION]\n')
            mostrar_menu_inicio()
            opcion = input('>> ')
            
            # INICIAR SESION
            if opcion == '1':
                dni = input('Ingrese su DNI: ')
                if dni not in empleados_id:
                    FALLO(f'El DNI "{dni}" no esta registrado en el sistema.\n')
                    continue
                
                contrasena = input('Ingrese su contraseña: ')
                if contrasena != contrasenas[dni]:
                    FALLO(f'La contraseña "{contrasena}" no coincide con el DNI "{dni}".\n')
                    continue
                
                # Hace que el usuario sea un empleado
                usuario = empleados[empleados_id[dni]]
                EXITO(f'Bienvenida/o {usuario} tu ID es {usuario.ID}.\n')
                
                # Crea el archivo de entradas y salidas
                if not (archivo_entradas := obtener_archivo_id(usuario.ID, False)).exists():
                    archivo_entradas.write_text('')
                    
                if not (archivo_salidas := obtener_archivo_id(usuario.ID, True)).exists():
                    archivo_salidas.write_text('')
                
                # Obtiene los registros de entradas y salidas
                if (entradas := obtener_registros(archivo_entradas)) is None:
                    ERROR('No se pudo obtener el archivo de entradas.\n')
                    continue
                
                if (salidas := obtener_registros(archivo_salidas) ) is None:
                    ERROR('No se pudo obtener el archivo de salidas.\n')
            # SALIR
            elif opcion == '2':
                break
            else:
                FALLO('Opcion invalida.\n')
        else:
            system('cls')
            print(f'[USUARIO {usuario.ID} | {usuario.DNI}]\n')
            mostrar_menu()
            opcion = input('>> ')
            
            # REGISTRAR ENTRADA
            if opcion == '1':
                # Entró mas veces de las que salió
                if len(entradas) > len(salidas):
                    FALLO('No saliste aun.\n')
                    continue
                
                resultado = registrar_entrada_salida(usuario.ID, False)
                print(resultado)
                if resultado is None:
                    FALLO('No se pudo registrar la entrada.\n')
                else:
                    EXITO(f'Entrada registrada: "{resultado}"\n')
                    entradas.append(tuple([dato.strip() for dato in resultado.split(',')]))

            # REGISTRAR SALIDA
            elif opcion == '2':
                if len(salidas) >= len(entradas):
                    FALLO('No entraste aun.\n')
                    continue
                
                resultado = registrar_entrada_salida(usuario.ID, True)
                print(resultado)
                if resultado is None:
                    FALLO('No se pudo registrar la salida.\n')
                else:
                    EXITO(f'Salida registrada: "{resultado}"\n')
                    salidas.append(tuple([dato.strip() for dato in resultado.split(',')]))

            # HORAS TRABAJADAS
            elif opcion == '3':
                if (empleado := empleados.get(input('ID >> '))) is None:
                    FALLO('El ID ingresado no existe.\n')
                    continue

                if empleado.ID != usuario.ID and empleado.rango >= usuario.rango:
                    FALLO('No podes consultar las horas trabajadas de un empleado no subordinado.\n')     
                    continue
                
                horas = calcular_horas_trabajadas(entradas, salidas)
                
                if horas is None:
                    EXITO(f'El empleado con ID {empleado.ID} no ha trabajado este mes.\n')
                    continue
                
                EXITO(f'Horas trabajadas por {empleado.apellidos}: {horas}')
            
            elif opcion == '4':
                if len(salidas) == 0:
                    EXITO('No hay dias registrados.\n')
                    continue

                EXITO('Dias presentes:', False)
                dias_trabajados = set()
                for i, salida in enumerate(salidas):
                    try:
                        dia, hora = salida
                    except:
                        ERROR(f'La salida {i + 1} no tiene el formato correcto.\n    (DIA, HORA)')
                        break
                    
                    if dia not in dias_trabajados:
                        print('-', dia)
                        dias_trabajados.add(dia)
                                        
            elif opcion == '5':
                usuario = None
                EXITO('Saliste con exito.\n')
            else:
                FALLO('Opcion invalida.\n')
            
        
if __name__ == '__main__':
    salida = main()
    exit(salida)