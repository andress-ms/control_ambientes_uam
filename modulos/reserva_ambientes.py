def reservar_ambiente(ambientes_df, clases_df, horarios_df, codigo_clase, hora_inicio, duracion):
    clase = clases_df[clases_df['codigo_clase'] == codigo_clase]
    num_alumnos = clase['alumnos'].values[0]
    for index, aula in ambientes_df.iterrows():
        if aula['estado'] == 'disponible' and aula['capacidad'] >= num_alumnos:
            horarios_df, reservado = asignar_clase(ambientes_df, horarios_df, codigo_clase, aula['codigo'], hora_inicio, duracion)
            if reservado:
                return horarios_df, aula['codigo']
    return horarios_df, None
