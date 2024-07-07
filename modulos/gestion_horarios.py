import pandas as pd
from modulos.gestion_clases import Actividad
from modulos.gestion_ambientes import Ambiente
from modulos.administracion import exportar_dataframe_a_csv

class Horario:
    def __init__(self, ambiente: Ambiente):
        self.ambiente = ambiente
        self.periodos = {
            '7-7:50 AM': None,
            '8-8:50 AM': None,
            '9-9:50 AM': None,
            '10-10:50 AM': None,
            '11-11:50 AM': None,
            '12M-12:50 PM': None,
            '1-1:50 PM': None,
            '2-2:50 PM': None,
            '3-3:50 PM': None,
            '4-4:50 PM': None,
            '5-5:50 PM': None,
            '5:50-6:40 PM': None,
            '6:45-7:35 PM': None,
            '7:40-8:30 PM': None,
            '8:30-9:20 PM': None
        }
        self.periodo_orden = list(self.periodos.keys())

    def asignar_actividad(self, periodo_inicio, actividad: Actividad):
        periodos_lista = list(self.periodos.keys())
        indice_inicio = periodos_lista.index(periodo_inicio)
        if all(self.periodos[periodos_lista[indice_inicio + i]] is None for i in range(actividad.duracion)):
            for i in range(actividad.duracion):
                self.periodos[periodos_lista[indice_inicio + i]] = actividad
        else:
            print(f"No se puede asignar la actividad '{actividad.nombre}' en el periodo '{periodo_inicio}'. Períodos no disponibles.")

    def obtener_actividad(self, periodo):
        if periodo in self.periodos:
            return self.periodos[periodo]
        else:
            print(f"Periodo '{periodo}' no válido.")
            return None


class HorariosDataFrame:
    def __init__(self, horarios_df=None):
        columnas = [
            'ambiente', '7-7:50 AM', '8-8:50 AM', '9-9:50 AM', '10-10:50 AM', '11-11:50 AM', 
            '12M-12:50 PM', '1-1:50 PM', '2-2:50 PM', '3-3:50 PM', '4-4:50 PM', 
            '5-5:50 PM', '5:50-6:40 PM', '6:45-7:35 PM', '7:40-8:30 PM', '8:30-9:20 PM'
        ]
        if horarios_df is None:
            self.horarios_df = pd.DataFrame(columns=columnas)
        else:
            self.horarios_df = horarios_df.set_index('ambiente')

    def consultar_horario(self, codigo_ambiente: str):
        if codigo_ambiente in self.horarios_df.index:
            data = self.horarios_df.loc[codigo_ambiente]
            ambiente = Ambiente(codigo_ambiente)
            horario = Horario(ambiente)
            for periodo, actividad in data.items():
                horario.periodos[periodo] = actividad
            return horario
        return None

    def mostrar_horarios(self):
        df_horarios = self.horarios_df.fillna('Libre')
        print(df_horarios.to_string())

    def agregar_horario(self, horario):
        horario_data = {}
        for periodo, actividad in horario.periodos.items():
            horario_data[periodo] = actividad.nombre if actividad else None
        self.horarios_df.loc[horario.ambiente.codigo_ambiente] = horario_data

    def eliminar_horario(self, ambiente_codigo):
        if ambiente_codigo in self.horarios_df.index:
            self.horarios_df = self.horarios_df.drop(index=ambiente_codigo)
        else:
            print(f"Ambiente '{ambiente_codigo}' no encontrado.")
  
    def exportar_a_csv(self, nombre_archivo):
        self.horarios_df.to_csv(nombre_archivo, index=False)

    def verificar_disponibilidad(self, ambiente_codigo: str, periodo_inicio: str, duracion: int) -> bool:
        horario = self.consultar_horario(ambiente_codigo)
        if horario:
            periodos_lista = list(horario.periodos.keys())
            indice_inicio = periodos_lista.index(periodo_inicio)
            return all(horario.periodos[periodos_lista[indice_inicio + i]] is None for i in range(duracion))
        return False

    def asignar_actividad_a_ambiente(self, ambiente_codigo: str, periodo_inicio: str, actividad: Actividad):
        if self.verificar_disponibilidad(ambiente_codigo, periodo_inicio, actividad.duracion):
            horario = self.consultar_horario(ambiente_codigo)
            horario.asignar_actividad(periodo_inicio, actividad)
            self.eliminar_horario(ambiente_codigo)  # Eliminamos el horario antiguo
            self.agregar_horario(horario)  # Agregamos el horario actualizado
            print(f"Actividad '{actividad.nombre}' asignada al ambiente '{ambiente_codigo}' en el periodo '{periodo_inicio}'.")
        else:
            print(f"No se puede asignar la actividad '{actividad.nombre}' al ambiente '{ambiente_codigo}' en el periodo '{periodo_inicio}'. Períodos no disponibles.")
