import pandas as pd
from modulos.administracion import Usuario

class Ambiente:
    def __init__(self, codigo_ambiente, tipo_ambiente, disponibilidad, activo, capacidad):
        self.codigo_ambiente = codigo_ambiente
        self.tipo_ambiente = tipo_ambiente
        self.disponibilidad = disponibilidad
        self.activo = activo
        self.capacidad = capacidad

class GestorDeAmbientes:
    def __init__(self, usuario: Usuario, ambientes_df=None):
        self.usuario = usuario
        if ambientes_df is None:
            self.ambientes_df = pd.DataFrame(columns=['codigo_ambiente', 'tipo', 'disponibilidad', 'activo', 'capacidad'])
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
        ambiente = self.ambientes_df[self.ambientes_df['codigo_ambiente'] == codigo_ambiente]
        if ambiente.empty:
            print("No se encontró el ambiente con el código proporcionado.")
        return ambiente
