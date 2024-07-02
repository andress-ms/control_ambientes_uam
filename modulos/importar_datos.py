import pandas as pd 
import os 

def cargar_datos(archivo_csv, archivo_excel, columnas, hoja_excel=None):
    if os.path.exists(archivo_csv):
        # Leer datos del CSV
        df = pd.read_csv(archivo_csv)
        if df.empty:
            # Si el CSV está vacío, intentar leer del Excel
            if os.path.exists(archivo_excel):
                try:
                    df = pd.read_excel(archivo_excel, sheet_name=hoja_excel)
                except ValueError as e:
                    # Si la hoja de Excel no existe, crear un DataFrame vacío con las columnas especificadas
                    print(f"Advertencia: {e}. Se creará un DataFrame vacío.")
                    df = pd.DataFrame(columns=columnas)
            else:
                # Si el Excel no existe, crear un DataFrame vacío con las columnas especificadas
                df = pd.DataFrame(columns=columnas)
    else:
        # Si el CSV no existe, intentar leer del Excel
        if os.path.exists(archivo_excel):
            try:
                df = pd.read_excel(archivo_excel, sheet_name=hoja_excel)
            except ValueError as e:
                # Si la hoja de Excel no existe, crear un DataFrame vacío con las columnas especificadas
                print(f"Advertencia: {e}. Se creará un DataFrame vacío.")
                df = pd.DataFrame(columns=columnas)
        else:
            # Si el Excel no existe, crear un DataFrame vacío con las columnas especificadas
            df = pd.DataFrame(columns=columnas)
    return df


def obtener_columnas_de_clase(clase):
    return list(clase.__annotations__.keys())
