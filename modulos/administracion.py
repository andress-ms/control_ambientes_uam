class Usuario:
    def __init__(self, nombre, rol):
        self.nombre = nombre
        self.rol = rol

    def es_administrador(self):
        return self.rol == 'administrador'