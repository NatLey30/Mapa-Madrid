import pandas as pd

if __name__ == "__main__":

    cruces = pd.read_csv('cruces.csv', sep=";",  encoding="LATIN_1")
    # direcciones = pd.read_csv('direcciones.csv', sep=";",  encoding="LATIN_1", low_memory=False)

    glorietas = cruces[cruces['Clase de la via tratado'] == 'GLORIETA                ']
    glorietas.to_csv('glorietas.csv', index=False)

    cruces_ac = cruces[cruces['Clase de la via tratado'] != 'GLORIETA                ']
    cruces_ac = cruces_ac[cruces_ac['Clase de la via que cruza'] != 'GLORIETA                ']

    cruces_ac.to_csv('cruces_ac.csv', index=False)