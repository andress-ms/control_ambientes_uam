import pandas as pd 
import os 

from modulos.gestion_ambientes import GestorDeAmbientes, Ambiente
from modulos.gestion_clases import Actividad, GestorDeActividades
from modulos.administracion import Usuario
from modulos.importar_datos import cargar_datos, obtener_columnas_de_clase

# IMPORTANTE, database.xlsx debe estar dentro de la carpeta de data
current_dir = os.path.dirname(os.path.abspath(__file__))
excel_path = os.path.join(current_dir, 'data', 'database.xlsx')
csv_path_ambientes = os.path.join(current_dir, 'data', 'lista_ambientes.csv')
csv_path_actividades = os.path.join(current_dir, 'data', 'lista_actividades.csv')


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