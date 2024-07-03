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
            print(f"Actividad '{actividad.nombre}' asignada al ambiente '{ambiente_codigo}' en el periodo '{periodo_inicio}'.")
        else:
            print(f"No se puede asignar la actividad '{actividad.nombre}' al ambiente '{ambiente_codigo}' en el periodo '{periodo_inicio}'. Períodos no disponibles.")