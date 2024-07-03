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

    def asignar_actividad(self, periodo, actividad: Actividad):
        if periodo not in self.periodos:
            print(f"Periodo '{periodo}' no válido.")
            return

        periodo_idx = self.periodo_orden.index(periodo)
        duracion = actividad.duracion

        if periodo_idx + duracion > len(self.periodo_orden):
            print(f"No hay suficientes periodos disponibles para asignar la actividad '{actividad.nombre}'.")
            return

        for i in range(duracion):
            self.periodos[self.periodo_orden[periodo_idx + i]] = actividad

    def obtener_actividad(self, periodo):
        if periodo in self.periodos:
            return self.periodos[periodo]
        else:
            print(f"Periodo '{periodo}' no válido.")
            return None

        
class HorariosDataFrame:
    def __init__(self):
        self.horarios = []

    def agregar_horario(self, horario: Horario):
        self.horarios.append(horario)

    def eliminar_horario(self, ambiente_codigo: str):
        self.horarios = [h for h in self.horarios if h.ambiente.codigo_ambiente != ambiente_codigo]

    def consultar_horario(self, ambiente_codigo: str) -> Horario:
        for h in self.horarios:
            if h.ambiente.codigo_ambiente == ambiente_codigo:
                return h
        print(f"No se encontró el horario para el ambiente con código '{ambiente_codigo}'.")
        return None

    def obtener_horarios_como_dataframe(self) -> pd.DataFrame:
        horarios_data = []
        for horario in self.horarios:
            horario_data = {'Ambiente': horario.ambiente.codigo_ambiente}
            for periodo in horario.periodo_orden:
                actividad = horario.obtener_actividad(periodo)
                horario_data[periodo] = actividad.nombre if actividad else ''
            horarios_data.append(horario_data)

        horarios_df = pd.DataFrame(horarios_data)
        return horarios_df
    
    def exportar_a_csv(self, nombre_archivo):
        horarios_df = self.obtener_horarios_como_dataframe()
        exportar_dataframe_a_csv(horarios_df, nombre_archivo)
