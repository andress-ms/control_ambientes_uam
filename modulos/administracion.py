class Usuario:
    def __init__(self, nombre, rol):
        self.nombre = nombre
        self.rol = rol

    def es_administrador(self):
        return self.rol == 'administrador'
    
def exportar_dataframe_a_csv(dataframe, nombre_archivo):
    dataframe.to_csv(nombre_archivo, index=False)

