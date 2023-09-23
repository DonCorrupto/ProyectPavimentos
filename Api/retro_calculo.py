import pandas as pd
import json

def geofonos():
    df = pd.read_pickle('dataframe.pkl')

    columnas_con_D = [col for col in df.columns if col.startswith('D')]
    numero_de_columnas_D = len(columnas_con_D) - 2
    columnas_micras = [f'D{i}' for i in range(1, numero_de_columnas_D + 1)]

    return numero_de_columnas_D


def normalizacion_unidades():

    df = pd.read_pickle('dataframe.pkl')

    columnas_con_D = [col for col in df.columns if col.startswith('D')]
    numero_de_columnas_D = len(columnas_con_D) - 2
    columnas_micras = [f'D{i}' for i in range(1, numero_de_columnas_D + 1)]

    numero_de_columnas_D = columnas_micras
    columnas_micras

    for col in columnas_micras:
        col_cm = col
        df[col_cm] = df[col] / 10000

    json_data = df.to_json(orient='records')

    return json_data


def normalizacion_carga():
    df = pd.read_pickle('dataframe.pkl')

    columnas_con_D = [col for col in df.columns if col.startswith('D')]
    numero_de_columnas_D = len(columnas_con_D) - 2
    columnas_micras = [f'D{i}' for i in range(1, numero_de_columnas_D + 1)]

    numero_de_columnas_D = columnas_micras
    columnas_micras

    for col in columnas_micras:
        col_cm = col
        df[col_cm] = df[col] / 10000

    df_normalized = df.copy()

    cols_to_normalize = numero_de_columnas_D

    df_normalized[cols_to_normalize] = df[cols_to_normalize].div(40 / df['Carga'], axis=0)

    json_data = df_normalized.to_json(orient='records')

    return json_data
