import pandas as pd 
import typing as dict

from modulos.gestion_ambientes import agregar_ambiente, eliminar_ambiente, actualizar_ambiente, consultar_ambiente

file_path = 'c:\\Users\\andre\\Desktop\\Ambientes UAM\\database.xlsx'

if __name__ == "__main__":
    ambientes_df = pd.read_excel(file_path)
    
print(ambientes_df)

nuevo_ambiente = {'codigo_ambiente': "C201",
                  'tipo_ambiente': "Aula",
                  'estado': "Disponible",
                  'capacidad': 25}



ambientes_df = agregar_ambiente(ambientes_df, nuevo_ambiente)
print("\nAmbientes después de agregar uno nuevo:")
print(ambientes_df)

ambientes_df = eliminar_ambiente(ambientes_df, "C101")
print("despues de eliminar")
print(ambientes_df)
    

