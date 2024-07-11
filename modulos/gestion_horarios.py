import pandas as pd
from modulos.gestion_clases import Actividad
from modulos.gestion_ambientes import Ambiente, GestorDeAmbientes
from modulos.administracion import exportar_dataframe_a_csv

class HorariosDataFrame:
    def __init__(self, horarios_df=None):
        columnas = [
            'ambiente', '7-7:50 AM', '8-8:50 AM', '9-9:50 AM', '10-10:50 AM', '11-11:50 AM', 
            '12M-12:50 PM', '1-1:50 PM', '2-2:50 PM', '3-3:50 PM', '4-4:50 PM', 
            '5-5:50 PM', '5:50-6:40 PM', '6:45-7:35 PM', '7:40-8:30 PM', '8:30-9:20 PM'
        ]
        if horarios_df is None:
            self.horarios_df = pd.DataFrame(columns=columnas, dtype=object)
        else:
            self.horarios_df = horarios_df

    def consultar_horario(self, codigo_ambiente: str) -> pd.Series:
        if codigo_ambiente in self.horarios_df['ambiente'].values:
            return self.horarios_df[self.horarios_df['ambiente'] == codigo_ambiente].iloc[0]
        else:
            print(f"No se encontró el ambiente con código '{codigo_ambiente}' en el horario.")
            return pd.Series()

    def mostrar_horarios(self):
        df_horarios = self.horarios_df.fillna('-')
        print(df_horarios.to_string())

    def agregar_actividad(self, ambiente_codigo: str, periodo_inicio: str, actividad_nombre: str):
        if ambiente_codigo in self.horarios_df['ambiente'].values:
            self.horarios_df.loc[self.horarios_df['ambiente'] == ambiente_codigo, periodo_inicio] = actividad_nombre
        else:
            print(f"No se encontró el ambiente con código '{ambiente_codigo}'.")

    def actualizar_actividad(self, ambiente_codigo: str, periodo_inicio: str, actividad_nombre: str):
        if ambiente_codigo in self.horarios_df['ambiente'].values:
            if periodo_inicio in self.horarios_df.columns:
                self.horarios_df.loc[self.horarios_df['ambiente'] == ambiente_codigo, periodo_inicio] = actividad_nombre
            else:
                print(f"El periodo '{periodo_inicio}' no existe en el DataFrame.")
        else:
            print(f"No se encontró el ambiente con código '{ambiente_codigo}'.")

    def eliminar_horario(self, ambiente_codigo):
        if ambiente_codigo in self.horarios_df['ambiente'].values:
            self.horarios_df = self.horarios_df[self.horarios_df['ambiente'] != ambiente_codigo]
        else:
            print(f"Registro anterior de Ambiente '{ambiente_codigo}' no encontrado.")

    def verificar_disponibilidad_en_df(self, ambiente_codigo: str, periodo_inicio: str, duracion: int) -> bool:
        if ambiente_codigo not in self.horarios_df['ambiente'].values:
            print(f"No se encontró el ambiente con el código '{ambiente_codigo}' en el DataFrame de horarios.")
            return False

        # Obtener los índices de las columnas de horario
        columnas_horarios = self.horarios_df.columns
        index_inicio = columnas_horarios.get_loc(periodo_inicio)
        periodos_ocupados = columnas_horarios[index_inicio:index_inicio + duracion]

        # Verificar la disponibilidad en los períodos necesarios
        ambiente_filtrado = self.horarios_df['ambiente'] == ambiente_codigo
        for periodo in periodos_ocupados:
            valor = self.horarios_df.loc[ambiente_filtrado, periodo].values[0]
            if pd.notna(valor) and valor is not None:
                print(f"El período '{periodo}' está ocupado en el ambiente '{ambiente_codigo}'.")
                return False
        return True

    def obtener_periodos_libres(self, ambiente_codigo: str, duracion_actividad: int) -> list[str]:
        if ambiente_codigo not in self.horarios_df['ambiente'].values:
            print(f"No se encontró el ambiente con el código '{ambiente_codigo}' en el DataFrame de horarios.")
            nueva_fila = pd.Series([ambiente_codigo] + [None] * (len(self.horarios_df.columns) - 1), index=self.horarios_df.columns)
            self.horarios_df = self.horarios_df._append(nueva_fila, ignore_index=True)
            print(f"Nuevo ambiente '{ambiente_codigo}' creado con todos los periodos libres.")

        periodos_libres = []

        columnas_horarios = self.horarios_df.columns
        periodos_totales = columnas_horarios[1:]

        for i in range(len(periodos_totales) - duracion_actividad + 1):
            periodo_inicio = periodos_totales[i]

            if self.verificar_disponibilidad_en_df(ambiente_codigo, periodo_inicio, duracion_actividad):
                periodos_libres.append(periodo_inicio)

        return periodos_libres

    def asignar_actividad_a_ambiente(self, ambiente_codigo: str, periodo_inicio: str, actividad: Actividad, gestor_ambientes: 'GestorDeAmbientes'):
        duracion = actividad.duracion
        if ambiente_codigo in self.horarios_df['ambiente'].values:
            if periodo_inicio in self.horarios_df.columns:
                if self.verificar_disponibilidad_en_df(ambiente_codigo, periodo_inicio, duracion):
                    index_inicio = self.horarios_df.columns.get_loc(periodo_inicio)
                    for i in range(duracion):
                        periodo = self.horarios_df.columns[index_inicio + i]
                        nombre_actividad = str(actividad.nombre)
                        self.horarios_df.loc[self.horarios_df['ambiente'] == ambiente_codigo, periodo] = nombre_actividad
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

    def exportar_a_csv(self, nombre_archivo):
        df_to_export = self.horarios_df
        df_to_export.to_csv(nombre_archivo, index=False)
