import pandas as pd
from modulos.administracion import Usuario, exportar_dataframe_a_csv

class Actividad:
    def __init__(self, codigo_clase, nombre, duracion, tamaño, grupo, docente=None):
        self.codigo_clase = codigo_clase
        self.nombre = nombre
        self.duracion = duracion
        self.tamaño = tamaño
        self.grupo = grupo
        self.docente = docente

    def __repr__(self):
        return f"Actividad(codigo_clase='{self.codigo_clase}', nombre='{self.nombre}', duracion={self.duracion}, tamaño={self.tamaño}, grupo='{self.grupo}', docente='{self.docente}')"

class GestorDeActividades:
    def __init__(self, usuario: Usuario, actividades_df= None):
        self.usuario = usuario
        if actividades_df is None:
            self.actividades_df = pd.DataFrame(columns=['codigo_clase', 'nombre', 'duracion', 'tamaño', 'grupo', 'docente'])
        else: 
            self.actividades_df = actividades_df
            
    def _verificar_permiso(self):
        if not self.usuario.es_administrador():
            raise PermissionError("Acción no permitida. Se requiere rol de administrador.")
    
    def agregar_actividad(self, nueva_actividad: Actividad) -> None:
        self._verificar_permiso()
        nuevo_df = pd.DataFrame([vars(nueva_actividad)])
        self.actividades_df = pd.concat([self.actividades_df, nuevo_df], ignore_index=True)
    
    def eliminar_actividad(self, codigo_clase: str) -> None:
        self._verificar_permiso()
        self.actividades_df.drop(self.actividades_df[self.actividades_df['codigo_clase'] == codigo_clase].index, inplace=True)
    
    def actualizar_actividad(self, codigo_clase: str, datos_actualizados: dict) -> None:
        self._verificar_permiso()
        try:
            self.actividades_df.loc[self.actividades_df['codigo_clase'] == codigo_clase, list(datos_actualizados.keys())] = list(datos_actualizados.values())
        except Exception as e:
            print(f"Error al actualizar la actividad: {e}")
    
    def consultar_actividad(self, codigo_clase: str) -> pd.DataFrame:
        actividad = self.actividades_df[self.actividades_df['codigo_clase'] == codigo_clase]
        if actividad.empty:
            print("No se encontró la actividad con el código proporcionado.")
        return actividad

    def exportar_a_csv(self, nombre_archivo):
        exportar_dataframe_a_csv(self.actividades_df, nombre_archivo)
