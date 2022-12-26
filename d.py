import pandas as pd

direcciones = pd.read_csv('direcciones.csv', sep=";",  encoding="LATIN_1", low_memory=False)
direcciones.to_csv('b.csv', index=False)
