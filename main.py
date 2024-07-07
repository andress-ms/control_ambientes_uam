import os
from modulos.gestion_ambientes import GestorDeAmbientes, Ambiente
from modulos.gestion_clases import Actividad, GestorDeActividades
from modulos.administracion import Usuario
from modulos.importar_datos import cargar_datos, obtener_columnas_de_clase
from modulos.gestion_horarios import HorariosDataFrame, Horario
from menu import iniciar_menu

# IMPORTANTE, database.xlsx debe estar dentro de la carpeta de data
current_dir = os.path.dirname(os.path.abspath(__file__))
excel_path = os.path.join(current_dir, 'data', 'database.xlsx')
csv_path_ambientes = os.path.join(current_dir, 'data', 'lista_ambientes.csv')
csv_path_actividades = os.path.join(current_dir, 'data', 'lista_actividades.csv')
csv_path_horarios = os.path.join(current_dir, 'data', 'horarios.csv')

if __name__ == "__main__":
    admin = Usuario(nombre='Admin', rol='administrador')

    # Leer los datos del archivo Excel
    ambientes_data = cargar_datos(csv_path_ambientes, excel_path, obtener_columnas_de_clase(Ambiente), hoja_excel="Hoja 1")

    # Crear una instancia de GestorDeAmbientes con los datos del archivo Excel
    gestor_ambientes = GestorDeAmbientes(usuario=admin, ambientes_df=ambientes_data)

    actividades_data = cargar_datos(csv_path_actividades, excel_path, obtener_columnas_de_clase(Actividad), hoja_excel='Hoja 2')

    gestor_clases = GestorDeActividades(usuario=admin, actividades_df=actividades_data)

    horarios_data = cargar_datos(csv_path_horarios, excel_path, obtener_columnas_de_clase(Horario), hoja_excel = 'Hoja 3')
    
    horarios_contenedor = HorariosDataFrame(horarios_df=horarios_data)

    iniciar_menu(gestor_ambientes, gestor_clases, horarios_contenedor)
