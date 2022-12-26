import pandas as pd
import grafo
import networkx as nx
import matplotlib.pyplot as plt
import math


def pintar(grafo_madrid):
    '''
    Pintamos el grafo llamando a la función del grafo que pasa
    nuestro grafo a un grafo de NetworkX.
    Args: grafo creado
    Return: None
    '''

    # Sacamos las posiciones de los vértices #
    pos = {}
    # Para cada vértice del grafo
    for v in grafo_madrid.vertices:
        objeto = grafo_madrid.vertices[v]
        # en la posición 3 de la lista de datos, se encuentran sus coordenadas
        coordenadas = objeto.datos[2]
        pos[v] = coordenadas

    G = grafo_madrid.convertir_a_NetworkX()
    plot = plt.plot()
    nx.draw(G, pos=pos, node_size=0.1)
    plt.show()


if __name__ == "__main__":

    # ABRIMOS ARCHIVOS
    cruces = pd.read_csv('cruces.csv', sep=";",  encoding="LATIN_1")
    direcciones = pd.read_csv('direcciones.csv', sep=";",  encoding="LATIN_1", low_memory=False)

    # GRAFOS
    grafo_madrid_e = grafo.Grafo(False)
    grafo_madrid_a = grafo.Grafo(False)

    dict = {}

    # Sacamos una lista con todas las calles que van a estar incluidad en nuestro gps
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

    # Creamos el grafo #
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

            # Data de cada arista
            data = pos['Clase de la via tratado'][0].strip()

            # Peso de la arista
            coorx = abs(coorx1-coorx2)
            coory = abs(coory1-coory2)
            dist = math.sqrt((coorx^2)+(coory^2)) # Para la distancia euclidea

            # Para calcular el tiempo mínimo por cada uno de los tipos de vías
            # pasamos la distancia de cm a km y lo dividimos por la velocidad
            # mámima en ese tipo de vía
            if data == 'AUTOVIA':
                peso = ((dist*0.000001)/100)*60
            elif data == 'AVENIDA':
                peso = ((dist*0.000001)/90)*60
            elif data == 'CARRETERA':
                peso = ((dist*0.000001)/70)*60
            elif data == 'CALLEJON' or data == 'CAMINO':
                peso = ((dist*0.000001)/30)*60
            elif data == 'ESTACION DE METRO' or data == 'PLAZUELA' or data == 'PASADIZO' or data == 'COLONIA':
                peso = ((dist*0.000001)/20)*60
            else:
                peso = ((dist*0.000001)/50)*60

            # Creamos los vértices
            v = [calle1.strip(), calle2.strip(), (coorx1, coory1)]
            w = [calle1.strip(), calle2prima.strip(), (coorx2, coory2)]

            # Creamos vertices #
            grafo_madrid_e.agregar_vertice(v)
            grafo_madrid_e.agregar_vertice(w)
            grafo_madrid_a.agregar_vertice(v)
            grafo_madrid_a.agregar_vertice(w)

            # Creamos aristas #
            grafo_madrid_e.agregar_arista(v, w, data, dist)
            grafo_madrid_a.agregar_arista(v, w, data, peso)

    # NAVEGADOR
    grafo_madrid_e = euclidea(cruces)
    grafo_madrid_a = autovia(cruces)

    origen = input("Introduzca la dirección completa del origen tal y como está en la base de datos (Presione intro para finalizar): ")
    destino = input("Introduzca la dirección completa del origen tal y como está en la base de datos (Presione intro para finalizar): ")

    while origen != '' and destino != '':

        index_o = direcciones[direcciones['Direccion completa para el numero'] == origen].reset_index
        cla_o = index_o['Clase de la via'][0].strip()
        par_o = index_o['Partícula de la vía'][0].strip()
        nom_o = index_o['Nombre de la vía'][0].strip()

        coordenada_o_x = index_o['Coordenada X (Guia Urbana) cm'][0]
        coordenada_o_y = index_o['Coordenada Y (Guia Urbana) cm'][0]

        # datos origen
        dir_o = cla_o + ' ' + par_o + ' ' + nom_o
        coordenada_o = (coordenada_o_x, coordenada_o_y)

        index_d = direcciones[direcciones['Direccion completa para el numero'] == destino].reset_index
        cla_d = index_d['Clase de la via'][0].strip()
        par_d = index_d['Partícula de la vía'][0].strip()
        nom_d = index_d['Nombre de la vía'][0].strip()

        coordenada_d_x = index_d['Coordenada X (Guia Urbana) cm'][0]
        coordenada_d_y = index_d['Coordenada Y (Guia Urbana) cm'][0]

        # datos destino
        dir_d = cla_d + ' ' + par_d + ' ' + nom_d
        coordenada_d = (coordenada_d_x, coordenada_d_y)

        continuar = True
        while continuar:
            op = input('Desea encontrar la ruta más corta(1) o más rápida(2): ')
            if op == 1 or op == 2:
                continuar = False
            else:
                print('No ha introducido una opción correcta, o 1 o 2')

        if op == 1:
            grafo_madrid = grafo_madrid_e

        else:
            grafo_madrid = grafo_madrid_a

        grafo_madrid.agregar_vertice('origen')
        grafo_madrid.agregar_vertice('destino')

        print(nom_o)
        print(nom_d)

        # pintar(grafo_madrid)

        origen = input("Introduzca la dirección completa del origen tal y como está en la base de datos (Presione intro para finalizar): ")
        destino = input("Introduzca la dirección completa del origen tal y como está en la base de datos (Presione intro para finalizar): ")
