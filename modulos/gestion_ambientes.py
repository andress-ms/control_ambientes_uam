import pandas as pd
from modulos.administracion import Usuario, exportar_dataframe_a_csv
from modulos.gestion_clases import Actividad

class Ambiente:
    def __init__(self, codigo_ambiente, tipo_ambiente, disponibilidad, activo, capacidad):
        self.codigo_ambiente = codigo_ambiente
        self.tipo_ambiente = tipo_ambiente
        self.disponibilidad = "Disponible" if disponibilidad else "No disponible"
        self.activo = "Activo" if activo else "Inactivo"
        self.capacidad = capacidad

class GestorDeAmbientes:
    def __init__(self, usuario: Usuario, ambientes_df=None):
        self.usuario = usuario
        if ambientes_df is None:
            self.ambientes_df = pd.DataFrame(columns=['codigo_ambiente', 'tipo_ambiente', 'disponibilidad', 'activo', 'capacidad'])
        else:
            self.ambientes_df = ambientes_df
            
    def _verificar_permiso(self):
        if not self.usuario.es_administrador():
            raise PermissionError("Acción no permitida. Se requiere rol de administrador.")
    
    def agregar_ambiente(self, nuevo_ambiente: Ambiente) -> None:
        self._verificar_permiso()
        nuevo_df = pd.DataFrame([vars(nuevo_ambiente)])
        self.ambientes_df = pd.concat([self.ambientes_df, nuevo_df], ignore_index=True)
    
    def eliminar_ambiente(self, codigo_ambiente: str) -> None:
        self._verificar_permiso()
        self.ambientes_df.drop(self.ambientes_df[self.ambientes_df['codigo_ambiente'] == codigo_ambiente].index, inplace=True)
    
    def actualizar_ambiente(self, codigo_ambiente: str, datos_actualizados: dict) -> None:
        self._verificar_permiso()
        try:
            self.ambientes_df.loc[self.ambientes_df['codigo_ambiente'] == codigo_ambiente, list(datos_actualizados.keys())] = list(datos_actualizados.values())
        except Exception as e:
            print(f"Error al actualizar el ambiente: {e}")
    
    def consultar_ambiente(self, codigo_ambiente: str) -> pd.DataFrame:
        # Asegurarse de que el código de ambiente esté en mayúsculas para una comparación insensible a mayúsculas y minúsculas
        ambiente = self.ambientes_df[self.ambientes_df['codigo_ambiente'].str.upper() == codigo_ambiente.upper()]
        if ambiente.empty:
            print(f"No se encontró el ambiente con el código proporcionado: {codigo_ambiente}")
        return ambiente
    
    def exportar_a_csv(self, nombre_archivo):
        exportar_dataframe_a_csv(self.ambientes_df, nombre_archivo)
        
    def filtrar_ambientes_para_actividad(self, actividad: Actividad) -> pd.DataFrame:
        try:
            # Convertir tamaño de la actividad a tipo numérico
            actividad_tamano = int(actividad.tamaño)

            ambientes_filtrados = self.ambientes_df[
                (self.ambientes_df['disponibilidad'] == "Disponible") &
                (self.ambientes_df['activo'] == "Activo") &
                (self.ambientes_df['capacidad'].astype(int) >= actividad_tamano)
            ]
            return ambientes_filtrados
        except ValueError as e:
            print(f"Error al filtrar ambientes: {e}")
            return pd.DataFrame()  # Devolver un DataFrame vacío en caso de error