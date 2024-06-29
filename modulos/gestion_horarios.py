import pandas as pd 

def verificar_disponibilidad(ambientes_df, horarios_df, codigo_ambiente, hora_inicio, duracion):
    hora_fin = pd.to_datetime(hora_inicio) + pd.Timedelta(hours=duracion)
    for index, row in horarios_df.iterrows():
        if row['codigo_aula'] == codigo_ambiente:
            clase_hora_inicio = pd.to_datetime(row['hora_inicio'])
            clase_hora_fin = clase_hora_inicio + pd.Timedelta(hours=row['duracion'])
            if (hora_inicio < clase_hora_fin) and (hora_fin > clase_hora_inicio):
                return False
        return True
    
def asignar_clase(ambientes_df, horarios_df, codigo_clase, codigo_ambiente, hora_inicio, duracion):
    if verificar_disponibilidad(ambientes_df, horarios_df, codigo_ambiente, hora_inicio, duracion):
        nuevo_horario = {
            'codigo_clase': codigo_clase,
            'codigo_aula': codigo_ambiente,
            'hora_inicio': hora_inicio,
            'hora_fin': pd.to_datetime(hora_inicio) + pd.Timedelta (hours=duracion)
        }
        horarios_df = horarios_df.append(nuevo_horario, ignore_index=True)
        return horarios_df, True
    else:
        return horarios_df, False