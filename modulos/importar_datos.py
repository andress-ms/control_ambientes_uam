import pandas as pd 

def cargar_datos():
    ambientes_df = pd.read_csv('data/lista_ambientes.csv')
    clases_df = pd.read_csv('data/lista_clases.csv')
    horarios_df = pd.read_csv('data/horarios.csv')
    return ambientes_df, clases_df, horarios_df

def validar_datos(ambientes_df, clases_df, horarios_df):
    pass 

