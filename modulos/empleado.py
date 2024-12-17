DIRECTOR = 3
GERENTE  = 2
JEFE     = 1
EMPLEADO = 0

class Empleado:
    def __init__(self, ID: str = None, DNI: str = None, nombres: str = None, apellidos: str = None, fecha_nacimiento: str = None):
        self.ID = ID
        self.DNI = DNI
        self.nombres = nombres
        self.apellidos = apellidos
        self.fecha_nacimiento = fecha_nacimiento
    
    @property
    def rango(self):
        if self.ID[0] == 'D':
            return DIRECTOR
        elif self.ID[0] == 'G':
            return GERENTE
        elif self.ID[0] == 'J':
            return JEFE
        elif self.ID[0] == 'E':
            return EMPLEADO
        else:
            return None
    
    def __repr__(self):
        return f'({self.DNI} : {self.nombres} {self.apellidos} | {self.fecha_nacimiento})'

    def __eq__(self, other: 'Empleado'):
        return other.DNI == self.DNI