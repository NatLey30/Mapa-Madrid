import pandas as pd
import grafo
import networkx as nx
import matplotlib.pyplot as plt
import math


def crear_grafo(cruces):
    '''
    Función que recive los dataframes para crear el grafo de la calle de la
    comunidad de madrid.
    Args: cruces
    Return: grafo
    '''
    # Inicializamos grafo
    grafo_madrid = grafo.Grafo(False)

    dict = {}

    # Sacamos una lista con todas las calles que van a estar incluidad en nuestri gps
    vias = cruces['Literal completo del vial tratado'].unique()
    for via in vias:
        # Para cada calle cogemos el subdataframe con contiene a esa calle
        df = cruces[cruces['Literal completo del vial tratado'] == via]

        # Y creamos una lista con todas las calles a las que cruza
        lista = []
        for index, row in df.iterrows():
            lista.append(row['Literal completo del vial que cruza'])

        # Para cada calle hay un número de calles que la cruzan
        dict[via] = lista

    ### Creamos el grafo ###
    for calle1 in dict:
        calles = dict[calle1]
        for c in range(len(calles)-2):
            calle2 = calles[c]
            calle2prima = calles[c+1]

            pos = cruces[cruces['Literal completo del vial tratado'] == calle1].reset_index()
            ind1 = pos[pos['Literal completo del vial que cruza'] == calle2].reset_index()
            ind2 = pos[pos['Literal completo del vial que cruza'] == calle2prima].reset_index()

            # Coordenada de los vertices
            coorx1 = ind1['Coordenada X (Guia Urbana) cm (cruce)'][0]
            coory1 = ind1['Coordenada Y (Guia Urbana) cm (cruce)'][0]
            coorx2 = ind2['Coordenada X (Guia Urbana) cm (cruce)'][0]
            coory2 = ind2['Coordenada Y (Guia Urbana) cm (cruce)'][0]

            # Peso de la arista
            coorx = abs(coorx1-coorx2)
            coory = abs(coory1-coory2)
            dist = math.sqrt((coorx^2)+(coory^2))

            # Data de cada arista
            data = pos['Clase de la via tratado'][0].strip()

            v = [calle1.strip(), calle2.strip(), (coorx1, coory1)]
            w = [calle1.strip(), calle2prima.strip(), (coorx2, coory2)]

            # Creamos vertices #
            grafo_madrid.agregar_vertice(v)
            grafo_madrid.agregar_vertice(w)

            # Creamos aristas #
            grafo_madrid.agregar_arista(v, w, data, dist)

    return grafo_madrid


def pintar(grafo_madrid):
    print("A")
    pos = {}

    for v in grafo_madrid.vertices:
        objeto = grafo_madrid.vertices[v]
        coordenadas = objeto.datos[2]
        pos[v] = coordenadas

    G = grafo_madrid.convertir_a_NetworkX()
    plot = plt.plot()
    nx.draw(G, pos=pos, node_size=0.1)
    plt.show()
    #plt.savefig('grafp.jpg')


if __name__ == "__main__":

    # Abrimos archivos
    cruces = pd.read_csv('cruces.csv', sep=";",  encoding="LATIN_1")
    # direcciones = pd.read_csv('direcciones.csv', sep=";",  encoding="LATIN_1", low_memory=False)

    grafo_madrid = crear_grafo(cruces)

    pintar(grafo_madrid)
