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

def obtener_temperatura_desde_archivo():
    try:
        with open('temperatura.txt', 'r') as file:
            opcion = file.read()
            opcion = int(opcion)
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

            def calcular_FT(row, opcion):
                μ = -35.649 * (row['Espesor de capa de rodadura']) ** (-0.624)

                if opcion == 1:
                    FT = 1 / (1 + (8 * (10 ** (-4)) * row['Espesor de capa de rodadura'] * (row['T-Man'] - 20)))
                elif opcion == 2:
                    FT = (1.054) ** ((row['T-Man'] - 20) / μ)
                elif opcion == 3:
                    FT = 1
                return FT
            def aplicar_opcion(df_normalized, opcion):
                df_normalized['FT'] = df_normalized.apply(lambda row: calcular_FT(row, opcion), axis=1)
                for columna in numero_de_columnas_D:
                    df_normalized[columna] = df_normalized['FT'] * df_normalized[columna]
                return df_normalized
            
            if opcion == 1 or opcion == 2 or opcion == 3:
                df_normalized = aplicar_opcion(df_normalized, opcion)

                json_data = df_normalized.to_json(orient='records')

                return json_data
    except FileNotFoundError:
        return None