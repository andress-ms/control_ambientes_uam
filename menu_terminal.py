import os
import pandas as pd

from modulos.gestion_ambientes import GestorDeAmbientes, Ambiente
from modulos.gestion_clases import Actividad, GestorDeActividades
from modulos.administracion import Usuario
from modulos.importar_datos import cargar_datos, obtener_columnas_de_clase
from modulos.gestion_horarios import Horario, HorariosDataFrame

# IMPORTANTE, database.xlsx debe estar dentro de la carpeta de data
current_dir = os.path.dirname(os.path.abspath(__file__))
excel_path = os.path.join(current_dir, 'data', 'database.xlsx')
csv_path_ambientes = os.path.join(current_dir,'data', 'lista_ambientes.csv')
csv_path_actividades = os.path.join(current_dir, 'data', 'lista_actividades.csv')
csv_path_horarios = os.path.join(current_dir, 'data', 'horarios.csv')

def mostrar_menu():
    print("\nMenu de opciones:")
    print("1. Agregar Ambiente")
    print("2. Eliminar Ambiente")
    print("3. Agregar Actividad")
    print("4. Eliminar Actividad")
    print("5. Asignar Actividad a Horario")
    print("6. Mostrar Horarios")
    print("7. Asignar aula y horario a actividad")
    print("8. Busqueda de ambientes con filtro. ")
    print("9. Salir")

def agregar_ambiente_menu(gestor_ambientes: GestorDeAmbientes):
    codigo = input("Ingrese el código del ambiente: ")
    tipo = input("Ingrese el tipo de ambiente: ")
    activo = input("¿Está activo? (s/n): ").lower() == 's'
    capacidad = int(input("Ingrese la capacidad: "))
    nuevo_ambiente = Ambiente(codigo, tipo, activo, capacidad)
    gestor_ambientes.agregar_ambiente(nuevo_ambiente)
    print("Ambiente agregado.")

def agregar_actividad_menu(gestor_clases: GestorDeActividades):
    codigo = input("Ingrese el código de la clase: ")
    nombre = input("Ingrese el nombre de la clase: ")
    duracion = int(input("Ingrese la duración: "))
    tamaño = int(input("Ingrese el tamaño: "))
    grupo = input("Ingrese el grupo: ")
    docente = input("Ingrese el nombre del docente: ")
    nueva_actividad = Actividad(codigo, nombre, duracion, tamaño, grupo, docente)
    gestor_clases.agregar_actividad(nueva_actividad)
    print("Actividad agregada exitosamente.")
    
def iniciar_menu(gestor_ambientes: GestorDeAmbientes, gestor_clases: GestorDeActividades, horarios_contenedor: HorariosDataFrame):
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        if not manejar_opcion(opcion, gestor_ambientes, gestor_clases, horarios_contenedor):
            break

def manejar_opcion(opcion, gestor_ambientes: GestorDeAmbientes, gestor_clases: GestorDeActividades, horarios_contenedor: HorariosDataFrame):
    if opcion == '1':
        agregar_ambiente_menu(gestor_ambientes)
    elif opcion == '2':
        codigo = input("Ingrese el código del ambiente a eliminar: ")
        gestor_ambientes.eliminar_ambiente(codigo)
        print("Ambiente eliminado.")
    elif opcion == '3':
        agregar_actividad_menu(gestor_clases)
    elif opcion == '4':
        codigo = input("Ingrese el código de la actividad a eliminar: ")
        gestor_clases.eliminar_actividad(codigo)
        print("Actividad eliminada.")
    elif opcion == '5':
        print(gestor_ambientes.ambientes_df)
        codigo_ambiente = input("Ingrese el código del ambiente: ")
        ambiente = gestor_ambientes.consultar_ambiente(codigo_ambiente)
        if not ambiente.empty:
            periodo = input("Ingrese el periodo (e.g., '8-8:50 AM'): ")
            codigo_actividad = input("Ingrese el código de la actividad: ")
            actividad = gestor_clases.consultar_actividad(codigo_actividad)
            if not actividad.empty:
                actividad_obj = Actividad(**actividad.iloc[0].to_dict())
                horarios_contenedor.asignar_actividad_a_ambiente(codigo_ambiente, periodo, actividad_obj, gestor_ambientes)
            else:
                print("No se encontró la actividad.")
        else:
            print("No se encontró el ambiente.")
    elif opcion == '6':
        print("Mostrando Horarios:")
        horarios_contenedor.mostrar_horarios()
    elif opcion == '7':
        codigo_actividad = input("Ingrese el código de la actividad: ")
        actividad = gestor_clases.consultar_actividad(codigo_actividad)
        if not actividad.empty:
                actividad_obj = Actividad(**actividad.iloc[0].to_dict())
                horarios_contenedor.seleccionar_ambiente_asignar_actividad(actividad_obj, gestor_ambientes)
        else:
                print("No se encontró la actividad.")
    elif opcion == '8':
        print("Busqueda por filtros, escriba el el valor por el cual desea filtrar los ambientes.")
        print("Deje el campo en blanco si no desea aplicar ese filtro.")

        tipo = input("Ingrese el tipo de aula: ")
        
        activo = input("Activo: s/n: ").strip().upper()
        if activo == 'S':
            activo = 'Activo'
        elif activo == 'N':
            activo = 'Inactivo'
        else:
            activo = None

        capacidad_min_input = input("Ingrese la capacidad mínima del ambiente: ").strip()
        if capacidad_min_input.isdigit():
            capacidad_min = int(capacidad_min_input)
        else:
            capacidad_min = None

        capacidad_max_input = input("Ingrese la capacidad máxima del ambiente: ").strip()
        if capacidad_max_input.isdigit():
            capacidad_max = int(capacidad_max_input)
        else:
            capacidad_max = None

        # Verificar que los valores mínimos y máximos sean válidos
        if capacidad_min is not None and capacidad_max is not None and capacidad_min > capacidad_max:
            print("Error: La capacidad mínima no puede ser mayor que la capacidad máxima.")
        else:
            ambientes_filtrados = gestor_ambientes.buscar_ambientes_con_filtros(tipo, activo, capacidad_min, capacidad_max)
            if ambientes_filtrados.empty:
                print("No se encontraron ambientes que coincidan con los criterios de búsqueda.")
            else:
                print("Ambientes encontrados:")
                print(ambientes_filtrados)
    elif opcion == '9':
        print("Saliendo...")
        return False
    else:
        print("Opción no válida.")
    return True
