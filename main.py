import os 
from modulos.gestion_ambientes import GestorDeAmbientes, Ambiente
from modulos.gestion_clases import Actividad, GestorDeActividades
from modulos.administracion import Usuario
from modulos.importar_datos import cargar_datos, obtener_columnas_de_clase
from modulos.gestion_horarios import Horario, HorariosDataFrame

# IMPORTANTE, database.xlsx debe estar dentro de la carpeta de data
current_dir = os.path.dirname(os.path.abspath(__file__))
excel_path = os.path.join(current_dir, 'data', 'database.xlsx')
csv_path_ambientes = os.path.join(current_dir, 'data', 'lista_ambientes.csv')
csv_path_actividades = os.path.join(current_dir, 'data', 'lista_actividades.csv')
csv_path_horarios = os.path.join(current_dir, 'data', 'horarios.csv')

if __name__ == "__main__":
    admin = Usuario(nombre='Admin', rol='administrador')

    # Leer los datos del archivo Excel
    ambientes_data = cargar_datos(csv_path_ambientes, excel_path,obtener_columnas_de_clase(Ambiente) ,hoja_excel="Hoja 1")

    # Crear una instancia de GestorDeAmbientes con los datos del archivo Excel
    gestor_ambientes = GestorDeAmbientes(usuario=admin, ambientes_df=ambientes_data)
    
    print("Ambientes iniciales:")
    print(gestor_ambientes.ambientes_df)

    # Crear un nuevo ambiente y agregarlo
    nuevo_ambiente = Ambiente(codigo_ambiente="C201", tipo_ambiente="Aula", disponibilidad=True, activo=True, capacidad=25)
    gestor_ambientes.agregar_ambiente(nuevo_ambiente)
    print("\nAmbientes después de agregar uno nuevo:")
    print(gestor_ambientes.ambientes_df)

    # Eliminar un ambiente
    gestor_ambientes.eliminar_ambiente("C101")
    print("\nAmbientes después de eliminar uno:")
    print(gestor_ambientes.ambientes_df)
    
    # Exportar el DataFrame modificado a un archivo .csv en la carpeta data
    gestor_ambientes.ambientes_df.to_csv(csv_path_ambientes, index=False)
    print(f"\nEl DataFrame modificado se ha guardado en {csv_path_ambientes}")
    
    actividades_data = cargar_datos(csv_path_actividades, excel_path, obtener_columnas_de_clase(Actividad), hoja_excel='Hoja 2')
    
    gestor_clases = GestorDeActividades(usuario=admin, actividades_df=actividades_data)
    print(gestor_clases.actividades_df)
    
    print("\nDataframe despues de agregar una clase")
    nueva_clase = Actividad(codigo_clase="SIS108", nombre="Logica y algoritmos", duracion=2, tamaño=25, grupo=3,docente="Ivan Arguello")
    gestor_clases.agregar_actividad(nueva_clase)
    print(gestor_clases.actividades_df)
    
    # Actualizar la actividad
    gestor_clases.actualizar_actividad('SIS108', {'nombre': 'Logica y algoritmos avanzados', 'duracion': 3})
    
    # Consultar nuevamente para ver los cambios
    print("\nActividades después de actualizar:")
    print(gestor_clases.consultar_actividad('SIS108'))

    # Eliminar la actividad
    gestor_clases.eliminar_actividad('SIS108')
    print(gestor_clases.actividades_df)
    
    # Consultar nuevamente para ver que ha sido eliminada
    print("\nActividades después de eliminar:")
    print(gestor_clases.consultar_actividad('SIS108'))
    
    print(gestor_clases.actividades_df)
    # Exportar el DataFrame de actividades a un archivo .csv en la carpeta data
    gestor_clases.exportar_a_csv(csv_path_actividades)
    
    aula1 = Ambiente("A101", "Aula", True, True, 30)
    aula2 = Ambiente("A102", "Laboratorio", True, True, 20)

    actividad1 = Actividad("SIS108", "Lógica y Algoritmos", 2, 25, 3, "Ivan Arguello")
    actividad2 = Actividad("MAT201", "Álgebra Lineal", 2, 30, 1, "María García")

    # Crear un horario para cada ambiente
    horario_aula1 = Horario(aula1)
    horario_aula2 = Horario(aula2)

    # Asignar actividades a diferentes períodos para cada horario
    horario_aula1.asignar_actividad('8-8:50 AM', actividad1)
    horario_aula1.asignar_actividad('10-10:50 AM', actividad2)
    horario_aula2.asignar_actividad('9-9:50 AM', actividad1)
    horario_aula2.asignar_actividad('11-11:50 AM', actividad2)

    # Crear un contenedor de horarios y agregar los horarios creados
    horarios_contenedor = HorariosDataFrame()
    horarios_contenedor.agregar_horario(horario_aula1)
    horarios_contenedor.agregar_horario(horario_aula2)

    # Obtener y mostrar los horarios como un DataFrame
    horarios_df = horarios_contenedor.obtener_horarios_como_dataframe()
    print("Horarios de Aulas:")
    print(horarios_df)
    
    horarios_contenedor.exportar_a_csv(csv_path_horarios)
    
    gestor_ambientes.agregar_ambiente(Ambiente('A101', 'Laboratorio', True, True, 30))
    gestor_ambientes.agregar_ambiente(Ambiente('A102', 'Aula', True, True, 25))
    gestor_ambientes.agregar_ambiente(Ambiente('A103', 'Aula', False, True, 20))

    # Crear instancia de Actividad
    actividad = Actividad('LOL203','Lógica y Algoritmos', 2, 25, 5, 'Christopher Ibarra')

    # Filtrar ambientes disponibles para la actividad
    ambientes_disponibles = gestor_ambientes.filtrar_ambientes_para_actividad(actividad)
    print(ambientes_disponibles)

    # Crear instancias de Horario y HorariosDataFrame
    horarios_df = HorariosDataFrame()

    horario_a101 = Horario(gestor_ambientes.consultar_ambiente('A101').iloc[0])
    horario_a102 = Horario(gestor_ambientes.consultar_ambiente('A102').iloc[0])

    horarios_df.agregar_horario(horario_a101)
    horarios_df.agregar_horario(horario_a102)

    # Asignar actividad a ambiente
    horarios_df.asignar_actividad_a_ambiente('A101', '8-8:50 AM', actividad)

    # Exportar horarios a CSV
    horarios_df.exportar_a_csv('horarios.csv')