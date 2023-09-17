import pandas as pd
import json

def realizar_analisis():
    df = pd.read_pickle('dataframe.pkl')

    columna = df['SalePrice']

    columna_list = columna.tolist()
    json_columna = json.dumps(columna_list)

    return json_columna
