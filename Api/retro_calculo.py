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
    
def modulo_resiliente():
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

                # Crea una lista para almacenar las distancias de los geófonos
                with open('distancia_D.txt', 'r') as file:
                    contenido = file.read()
                    distancias = [int(numero) for numero in contenido.split(',')]

                    columnas_D = sorted([col for col in df_normalized.columns if col.startswith('D')])

                    # Encuentra el índice de la columna 'D2'
                    indice_D2 = columnas_D.index('D2')

                    dataframe_unificado = pd.DataFrame()

                    # Realiza el cálculo y crea tablas separadas para cada columna D desde D2 hasta el penúltimo
                    for i, columna_D in enumerate(columnas_D[indice_D2:-1], start=2):  # Comienza desde D2 hasta el penúltimo
                        resultado = (2.4 * 40) / (df_normalized[columna_D] * distancias[i - 2] * 2.54)
                        df_resultado = pd.DataFrame({f'Modulo resiliente {columna_D}': resultado})

                        df_resultado.drop(columns=['Modulo resiliente Distancia'], inplace=True, errors='ignore')

                        dataframe_unificado = pd.concat([dataframe_unificado, df_resultado], axis=1)

                    if not dataframe_unificado.empty:
                        json_data = dataframe_unificado.to_json(orient='records')
                        return json_data
    except FileNotFoundError:
        return None