import pandas as pd 
import os 

from modulos.gestion_ambientes import GestorDeAmbientes, Ambiente
from modulos.administracion import Usuario

# IMPORTANTE, database.xlsx debe estar dentro de la carpeta de data
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'data', 'database.xlsx')
output_path = os.path.join(current_dir, 'data', 'database_modificado.csv')


if __name__ == "__main__":
    admin = Usuario(nombre='Admin', rol='administrador')

    # Leer los datos del archivo Excel
    ambientes_data = pd.read_excel(file_path)

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
    gestor_ambientes.ambientes_df.to_csv(output_path, index=False)
    print(f"\nEl DataFrame modificado se ha guardado en {output_path}")