from pathlib import Path

NOMBRE_EMPLEADOS   = Path('empleados.txt')
NOMBRE_CONTRASENAS = Path('passwords.txt')
NOMBRE_REGISTROS   = Path('registros')
NOMBRE_ENTRADAS    = Path('entradas')
NOMBRE_SALIDAS     = Path('salidas')

DIR_ENTRADAS    = NOMBRE_REGISTROS / NOMBRE_ENTRADAS
DIR_SALIDAS     = NOMBRE_REGISTROS / NOMBRE_SALIDAS
ARC_EMPLEADOS   = NOMBRE_REGISTROS / NOMBRE_EMPLEADOS
ARC_CONTRASENAS = NOMBRE_REGISTROS / NOMBRE_CONTRASENAS