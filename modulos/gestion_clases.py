def agregar_clase(clases_df, nueva_clase):
    clases_df = clases_df.append(nueva_clase, ignore_index=True)
    return clases_df

def eliminar_clase(clases_df, codigo_clase):
    clases_df = clases_df[clases_df['codigo_clase'] != codigo_clase]
    return clases_df

def actualizar_clase(clases_df, codigo_clase, datos_actualizados):
    clases_df.loc[clases_df['codigo_clase'] == codigo_clase, datos_actualizados.keys()] = datos_actualizados.values()
    return clases_df

def consultar_clase(clases_df, codigo_clase):
    return clases_df[clases_df['codigo_clase'] == codigo_clase]
