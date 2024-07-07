import pandas as pd
from modulos.gestion_clases import Actividad
from modulos.gestion_ambientes import Ambiente, GestorDeAmbientes
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
        print(f"Intentando asignar actividad '{actividad.nombre}' en el período '{periodo_inicio}'...")
        periodos_lista = list(self.periodos.keys())
        indice_inicio = periodos_lista.index(periodo_inicio)
        
        if all(self.periodos[periodos_lista[indice_inicio + i]] is None for i in range(actividad.duracion)):
            print("Todos los períodos requeridos están disponibles. Asignando actividad...")
            for i in range(actividad.duracion):
                self.periodos[periodos_lista[indice_inicio + i]] = actividad
            print(f"Actividad '{actividad.nombre}' asignada en el período '{periodo_inicio}'.")
        else:
            print(f"No se puede asignar la actividad '{actividad.nombre}' en el período '{periodo_inicio}'. Períodos no disponibles.")

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

    def consultar_horario(self, codigo_ambiente: str, gestor_ambientes: 'GestorDeAmbientes'):
        if gestor_ambientes is None:
            print("Error: El gestor de ambientes no está definido.")
            return None
        
        ambiente_data = gestor_ambientes.consultar_ambiente(codigo_ambiente)
        
        if not ambiente_data.empty:
            # Convertir ambiente_data a un objeto Ambiente
            ambiente_info = ambiente_data.iloc[0].to_dict()
            ambiente = Ambiente(**ambiente_info)
            
            if codigo_ambiente in self.horarios_df.index:
                data = self.horarios_df.loc[codigo_ambiente]
            else:
                data = {periodo: None for periodo in self.horarios_df.columns if periodo != 'ambiente'}

            horario = Horario(ambiente)
            for periodo, actividad in data.items():
                if isinstance(actividad, str) and actividad == '-':
                    horario.periodos[periodo] = None
                else:
                    actividad_obj = Actividad(nombre=actividad) if actividad else None
                    horario.periodos[periodo] = actividad_obj
            return horario
        else:
            print(f"No se encontró el ambiente con código '{codigo_ambiente}'.")
            return None

    def mostrar_horarios(self):
        df_horarios = self.horarios_df.fillna('-')
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
            print(f"Registro anterior de Ambiente '{ambiente_codigo}' no encontrado.")
  
    def exportar_a_csv(self, nombre_archivo):
        self.horarios_df.to_csv(nombre_archivo, index=False)

    def verificar_disponibilidad(self, ambiente_codigo: str, periodo_inicio: str, duracion: int, gestor_ambientes: GestorDeAmbientes) -> bool:
        horario = self.consultar_horario(ambiente_codigo, gestor_ambientes)
        if horario:
            periodos_lista = list(horario.periodos.keys())
            if periodo_inicio in periodos_lista:
                indice_inicio = periodos_lista.index(periodo_inicio)
                # Verificar disponibilidad para la duración de la actividad
                if indice_inicio + duracion <= len(periodos_lista):
                    return all(horario.periodos[periodos_lista[indice_inicio + i]] is None for i in range(duracion))
                else:
                    print("No hay suficientes periodos para la duración solicitada")
                    return False  
            else:
                print("El periodo_inicio no está en la lista de periodos del horario")
                return False  
        print("No se encontró el horario para el ambiente")
        return False   
    
    def asignar_actividad_a_ambiente(self, ambiente_codigo: str, periodo_inicio: str, actividad: Actividad, gestor_ambientes: GestorDeAmbientes):
        if self.verificar_disponibilidad(ambiente_codigo, periodo_inicio, actividad.duracion, gestor_ambientes):
            horario = self.consultar_horario(ambiente_codigo, gestor_ambientes)
            horario.asignar_actividad(periodo_inicio, actividad)
            self.eliminar_horario(ambiente_codigo)  # Eliminamos el horario antiguo
            self.agregar_horario(horario)  # Agregamos el horario actualizado
            print(f"Actividad '{actividad.nombre}' asignada al ambiente '{ambiente_codigo}' en el periodo '{periodo_inicio}'.")
        else:
            print(f"Error aca")

    def mostrar_ambientes_disponibles(self, actividad: Actividad, gestor_ambientes: GestorDeAmbientes):
        ambientes_disponibles = gestor_ambientes.filtrar_ambientes_para_actividad(actividad)
        
        if ambientes_disponibles.empty:
            print("No hay ambientes disponibles que cumplan con los requisitos de la actividad.")
        else:
            print("Ambientes disponibles para la actividad:")
            for i, ambiente in ambientes_disponibles.iterrows():
                print(f"{i}. {ambiente['codigo_ambiente']} - Tipo: {ambiente['tipo_ambiente']}, Capacidad: {ambiente['capacidad']}")
        
        return ambientes_disponibles['codigo_ambiente'].tolist()

    def seleccionar_ambiente_asignar_actividad(self, actividad: Actividad, gestor_ambientes: GestorDeAmbientes):
        ambientes_disponibles = self.mostrar_ambientes_disponibles(actividad, gestor_ambientes)
        opcion = input("Seleccione el número del ambiente donde desea asignar la actividad: ")

        try:
            print(ambientes_disponibles)
            opcion = int(opcion)
            if opcion > 0 and opcion <= len(ambientes_disponibles):
                ambiente_seleccionado = ambientes_disponibles[opcion - 1]
                print(f"Ambiente seleccionado: {ambiente_seleccionado}")
                periodo_inicio = input("Ingrese el período de inicio (por ejemplo, '8-8:50 AM'): ")
                self.asignar_actividad_a_ambiente(ambiente_seleccionado, periodo_inicio, actividad, gestor_ambientes)
            else:
                print("Opción inválida. Seleccione un número válido.")
        except ValueError:
            print("Entrada inválida. Ingrese un número válido.")


