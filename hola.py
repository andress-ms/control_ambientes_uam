import pandas as pd

# Ruta al archivo de Excel
file_path = 'c:\\Users\\andre\\Desktop\\Ambientes UAM\\database.xlsx'

# Leer el archivo Excel y cargarlo en un DataFrame
df = pd.read_excel(file_path)

# Mostrar las primeras filas del DataFrame para verificar que se ha cargado correctamente
print(df.head())