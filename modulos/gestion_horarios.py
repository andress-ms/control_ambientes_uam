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
        periodos_lista = list(self.periodos.keys())
        indice_inicio = periodos_lista.index(periodo_inicio)
        
        if all(self.periodos[periodos_lista[indice_inicio + i]] is None for i in range(actividad.duracion)):
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

    def actualizar_actividad(self, periodo_inicio, actividad: Actividad):
        print(f"Intentando actualizar actividad '{actividad.nombre}' en el período '{periodo_inicio}'...")
        if periodo_inicio in self.periodos and self.periodos[periodo_inicio] is not None:
            print(f"El período '{periodo_inicio}' ya está ocupado por la actividad '{self.periodos[periodo_inicio].nombre}'.")
            return False
        else:
            self.periodos[periodo_inicio] = actividad
            print(f"Actividad '{actividad.nombre}' actualizada en el período '{periodo_inicio}'.")
            return True

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

    
    def consultar_horario(self, codigo_ambiente: str) -> pd.Series:
        if codigo_ambiente in self.horarios_df.index:
            return self.horarios_df.loc[codigo_ambiente]
        else:
            print(f"No se encontró el ambiente con código '{codigo_ambiente}' en el horario.")
            return pd.Series()
    
    """def consultar_horario(self, codigo_ambiente: str, gestor_ambientes: GestorDeAmbientes):
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
                if isinstance(actividad, str):
                    if actividad == '-':
                        horario.periodos[periodo] = None
                    else:
                        # Aquí se asume que la cadena contiene el nombre de la actividad
                        actividad_obj = Actividad(
                            codigo_clase='',
                            nombre=actividad,
                            duracion=0,
                            tamaño=0,
                            grupo='',
                            docente=None
                        )
                elif isinstance(actividad, Actividad):
                    actividad_obj = actividad
                else:
                    actividad_obj = None
                    horario.periodos[periodo] = actividad_obj
            return horario
        else:
            print(f"No se encontró el ambiente con código '{codigo_ambiente}'.")
            return None"""

    def mostrar_horarios(self):
        df_horarios = self.horarios_df.fillna('-')
        print(df_horarios.to_string())

    def agregar_actividad(self, ambiente_codigo: str, periodo_inicio: str, actividad_nombre: str):
        if ambiente_codigo in self.horarios_df.index:
            self.horarios_df.loc[ambiente_codigo, periodo_inicio] = actividad_nombre
        else:
            print(f"No se encontró el ambiente con código '{ambiente_codigo}'.")
            
    def actualizar_actividad(self, ambiente_codigo: str, periodo_inicio: str, actividad_nombre: str):
        if ambiente_codigo in self.horarios_df.index:
            if periodo_inicio in self.horarios_df.columns:
                self.horarios_df.loc[ambiente_codigo, periodo_inicio] = actividad_nombre
            else:
                print(f"El periodo '{periodo_inicio}' no existe en el DataFrame.")
        else:
            print(f"No se encontró el ambiente con código '{ambiente_codigo}'.")
            
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
                    for i in range(duracion):
                        if horario.periodos[periodos_lista[indice_inicio + i]] is not None:
                            print(f"Periodo '{periodos_lista[indice_inicio + i]}' ya está ocupado.")
                            return False
                    return True
                else:
                    print("No hay suficientes periodos para la duración solicitada.")
                    return False
            else:
                print(f"El período '{periodo_inicio}' no está en la lista de periodos del horario.")
                return False
        else:
            print(f"No se encontró el horario para el ambiente con código '{ambiente_codigo}'.")
            return False
    
    def verificar_disponibilidad_en_df(self, ambiente_codigo: str, periodo_inicio: str, duracion: int) -> bool:
        # Verificar si el ambiente está en el DataFrame
        if ambiente_codigo not in self.horarios_df.index:
            print(f"No se encontró el ambiente con el código '{ambiente_codigo}' en el DataFrame de horarios.")
            return False

        # Obtener los períodos que serán ocupados por la actividad
        periodos_ocupados = []
        index_inicio = self.horarios_df.columns.get_loc(periodo_inicio)
        for i in range(duracion):
            periodo = self.horarios_df.columns[index_inicio + i]
            periodos_ocupados.append(periodo)

        # Verificar la disponibilidad en los períodos necesarios
        for periodo in periodos_ocupados:
            if self.horarios_df.loc[ambiente_codigo, periodo] is not None:
                print(f"El período '{periodo}' está ocupado en el ambiente '{ambiente_codigo}'.")
                return False

        # Si todos los períodos están libres, retorna True
        return True
        
    def obtener_periodos_libres(self, ambiente_codigo: str, duracion: int) -> list:
        periodos_libres = []

        if ambiente_codigo not in self.horarios_df.index:
            # Inicializar todos los períodos como libres si el ambiente no existe en el DataFrame
            self.horarios_df.loc[ambiente_codigo] = [None] * len(self.horarios_df.columns)
            
        # Obtener la lista completa de períodos sin excluir la primera columna
        periodos_lista = list(self.horarios_df.columns)

        for i in range(len(periodos_lista) - duracion + 1):  # Iniciamos desde 0
            if all(self.horarios_df.loc[ambiente_codigo, periodos_lista[i + j]] is None for j in range(duracion)):
                periodos_libres.append(periodos_lista[i])
        
        return periodos_libres

    
    def asignar_actividad_a_ambiente(self, ambiente_codigo: str, periodo_inicio: str, actividad: Actividad, gestor_ambientes: 'GestorDeAmbientes'):
        duracion = actividad.duracion
        if ambiente_codigo in self.horarios_df.index:
            if periodo_inicio in self.horarios_df.columns:
                if self.verificar_disponibilidad_en_df(ambiente_codigo, periodo_inicio, duracion):
                    # Asignar la actividad a todos los períodos requeridos
                    index_inicio = self.horarios_df.columns.get_loc(periodo_inicio)
                    for i in range(duracion):
                        periodo = self.horarios_df.columns[index_inicio + i]
                        self.horarios_df.loc[ambiente_codigo, periodo] = actividad.nombre
                    print(f"Actividad '{actividad.nombre}' asignada al ambiente '{ambiente_codigo}' en el periodo '{periodo_inicio}'.")
                else:
                    print(f"No se puede asignar la actividad '{actividad.nombre}' al ambiente '{ambiente_codigo}' en el periodo '{periodo_inicio}' porque algunos períodos están ocupados.")
            else:
                print(f"El periodo '{periodo_inicio}' no existe en el DataFrame.")
        else:
            print(f"No se encontró el ambiente con código '{ambiente_codigo}'.")

    def mostrar_ambientes_disponibles(self, actividad: Actividad, gestor_ambientes: GestorDeAmbientes):
        ambientes_disponibles = gestor_ambientes.filtrar_ambientes_para_actividad(actividad)

        if ambientes_disponibles.empty:
            print("No hay ambientes disponibles que cumplan con los requisitos de la actividad.")

        return ambientes_disponibles['codigo_ambiente'].tolist()

    def seleccionar_ambiente_asignar_actividad(self, actividad: Actividad, gestor_ambientes: GestorDeAmbientes):
        ambientes_disponibles = self.mostrar_ambientes_disponibles(actividad, gestor_ambientes)
        opcion = input("Seleccione el número del ambiente donde desea asignar la actividad: ")

        try:
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


