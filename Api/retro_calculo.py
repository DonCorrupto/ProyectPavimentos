import pandas as pd

df = None

if df is None:
    pass
else:
    df = pd.read_pickle('datos_dataframe.pkl')

columna = df['SalePrice']
