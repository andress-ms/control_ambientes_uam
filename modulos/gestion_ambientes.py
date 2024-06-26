def agregar_ambiente(ambientes_df, nuevo_ambiente):
    ambientes_df = ambientes_df.append(nuevo_ambiente, ignore_index=True)
    return ambientes_df

def eliminar_ambiente(ambientes_df, codigo_ambiente):
    ambientes_df = ambientes_df[ambientes_df['codigo'] != codigo_ambiente]
    return ambientes_df

def actualizar_ambiente(ambientes_df, codigo_ambiente, datos_actualizados):
    ambientes_df.loc[ambientes_df['codigo'] == codigo_ambiente, datos_actualizados.keys()] = datos_actualizados.values()
    return ambientes_df

def consultar_ambiente(ambientes_df, codigo_ambiente):
    return ambientes_df[ambientes_df['codigo'] == codigo_ambiente]
