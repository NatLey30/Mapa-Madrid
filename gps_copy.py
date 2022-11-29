import pandas as pd
import grafo
import networkx as nx
import matplotlib.pyplot as plt


def crear_grafo(cruces):
    '''
    Función que recive los dataframes para crear el grafo de la calle de la 
    comunidad de madrid
    '''
    # Inicializamod grafo #
    grafo_madrid = grafo.Grafo()

    # Creamos vertices #
    dict = {}
    vias = cruces['Literal completo del vial tratado'].unique()
    for via in vias:
        df = cruces[cruces['Literal completo del vial tratado'] == via]
        lista = []
        for index, row in df.iterrows():
            lista.append(row['Literal completo del vial que cruza'])
        dict[via] = lista
    print(dict)

    # Rotondas/Glorietas/Plazas #

    # Creamos aristas #

    return grafo_madrid



if __name__ == "__main__":

    # Abrimos archivos
    cruces = pd.read_csv('cruces.csv', sep=";",  encoding="LATIN_1")
    # direcciones = pd.read_csv('direcciones.csv', sep=";",  encoding="LATIN_1", low_memory=False)

    grafo_madrid = crear_grafo(cruces)
