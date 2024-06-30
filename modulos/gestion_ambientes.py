import pandas as pd
from typing import Dict

def agregar_ambiente(ambientes_df: pd.DataFrame, nuevo_ambiente: Dict) -> None:
    nuevo_df = pd.DataFrame([nuevo_ambiente])
    ambientes_df = pd.concat([ambientes_df, nuevo_df], ignore_index=True)
    return None

def eliminar_ambiente(ambientes_df: pd.DataFrame, codigo_ambiente: str) -> None:
    ambientes_df.drop(ambientes_df[ambientes_df['codigo_ambiente'] == codigo_ambiente].index, inplace=True)
    return None

def actualizar_ambiente(ambientes_df: pd.DataFrame, codigo_ambiente: str, datos_actualizados: Dict) -> None:
    try:
        ambientes_df.loc[ambientes_df['codigo_ambiente'] == codigo_ambiente, list(datos_actualizados.keys())] = list(datos_actualizados.values())
    except Exception as e:
        print(f"Error al actualizar el ambiente: {e}")
    return None

def consultar_ambiente(ambientes_df: pd.DataFrame, codigo_ambiente: str) -> pd.DataFrame:
    ambiente = ambientes_df[ambientes_df['codigo_ambiente'] == codigo_ambiente]
    if ambiente.empty:
        print("No se encontró el ambiente con el código proporcionado.")
    return ambiente
