import pandas as pd
import grafo
import networkx as nx
import matplotlib.pyplot as plt

if __name__ == "__main__":
    grafo_madrid = grafo.Grafo()

    cruces = pd.read_csv('cruces.csv', sep=";",  encoding="LATIN_1")
    # direcciones = pd.read_csv('direcciones.csv', sep=";",  encoding="LATIN_1", low_memory=False)

    # glorietas_df = cruces[cruces['Clase de la via tratado'] == 'GLORIETA                '].reset_index(drop=True)

    # cruces_ac_df = cruces[cruces['Clase de la via tratado'] != 'GLORIETA                ']
    # cruces_ac_df = cruces_ac_df[cruces_ac_df['Clase de la via que cruza'] != 'GLORIETA                '].reset_index(drop=True)

    # glorietas = sorted(list(pd.unique(glorietas_df['Codigo de vía tratado'])))

    # for codigo_glorieta in glorietas:
    #     for i in range(len(glorietas_df)):
    #         if glorietas_df.loc[i, 'Codigo de vía tratado'] == codigo_glorieta:
    #             print(codigo_glorieta)
    #     print('-')

    # codigos_calles = sorted(list(pd.unique(cruces['Codigo de vía tratado'])))

    # for codigo in codigos_calles:
    #     calles = cruces[cruces['Codigo de vía tratado'] == codigo].reset_index(drop=True)

    for linea in range(len(cruces)):
        codigo = [int(cruces.loc[linea, 'Codigo de vía tratado']), int(cruces.loc[linea, 'Codigo de via que cruza o enlaza'])]
        coordenadas = [int(cruces.loc[linea, 'Coordenada X (Guia Urbana) cm (cruce)']), int(cruces.loc[linea, 'Coordenada Y (Guia Urbana) cm (cruce)'])]
        v = [codigo, coordenadas]
        grafo_madrid.agregar_vertice(v)
