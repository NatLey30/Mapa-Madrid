import pandas as pd
import grafo
import networkx as nx
import matplotlib.pyplot as plt
import math
import sys

INFTY = sys.float_info.max


def datos(direcciones, direccion):
    '''
    Lee el csv de direcciones y busca las coincidencias con la direccion
    que se quiere buscar y escoge la primera.
    Args:
        direcciones: csv
        direccion: la que se quiere buscar
    Return: dir y coordenadas
    '''

    index = direcciones[direcciones['Direccion completa para el numero'].str.contains(direccion, case=False)].reset_index()

    # Se saca el nombre de la calle
    cla = index['Clase de la via'][0].strip()
    par = index['Partícula de la vía'][0].strip()
    nom = index['Nombre de la vía'][0].strip()

    # Se obtienen las coordenadas
    coordenada_x = index['Coordenada X (Guia Urbana) cm'][0]
    coordenada_y = index['Coordenada Y (Guia Urbana) cm'][0]

    # datos
    dir = cla + ' ' + par + ' ' + nom
    coordenada = (int(coordenada_x), int(coordenada_y))

    return dir, coordenada


def cercano(u, dir, coordenada, grafo_madrid):
    '''
    Función que busca el vértice más cercano al vertice que se introduce como
    argumento y se crea una arista entre estos dos.
    Args:
        dir: vertice a añadir
        coordenada: coordenadas del vertice
        grafo_madrid: grafo al que se añade
    Return: None
    '''
    coordenadas_c = (INFTY, INFTY)
    # df = cruces[cruces['Literal completo del vial tratado'].str.contains(dir, case=False)].reset_index()
    # calle = ''

    # for index, row in df.iterrows():
    #     x = row['Coordenada X (Guia Urbana) cm (cruce)']
    #     y = row['Coordenada Y (Guia Urbana) cm (cruce)']
    #     resta_x = abs(coordenada[0] - x)
    #     resta_y = abs(coordenada[0] - y)
    #     if resta_x < coordenadas_c[0] or resta_y < coordenadas_c[0]:
    #         coordenadas_c = (x, y)
    #         calle = row['Literal completo del vial que cruza'].strip()

    # w = [dir, calle]
    # w.sort()
    # w.append(coordenadas_c)
    # print(w)

    w = None
    for v in grafo_madrid.vertices:
        if v != 'origen' and v != 'destino':
            vertice = grafo_madrid.vertices[v]
            c = vertice.datos[2]
            resta_x = abs(coordenada[0] - int(c[0]))
            resta_y = abs(coordenada[0] - int(c[1]))
            if resta_x < coordenadas_c[0] or resta_y < coordenadas_c[0]:
                coordenadas_c = (c[0], c[1])
                w = v
        print(coordenadas_c)

    grafo_madrid.agregar_arista(u, w, None, 1)


if __name__ == "__main__":
    # ABRIMOS ARCHIVOS #
    cruces = pd.read_csv('cruces.csv', sep=";",  encoding="LATIN_1")
    direcciones = pd.read_csv('direcciones.csv', sep=";",  encoding="LATIN_1",
                              low_memory=False)

    # GRAFOS #
    grafo_madrid_e = grafo.Grafo(False)
    grafo_madrid_a = grafo.Grafo(False)

    dict = {}

    # Sacamos una lista con todas las calles que van a estar incluidas
    # en nuestro gps
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
            coorx1 = int(ind1['Coordenada X (Guia Urbana) cm (cruce)'][0])
            coory1 = int(ind1['Coordenada Y (Guia Urbana) cm (cruce)'][0])
            coorx2 = int(ind2['Coordenada X (Guia Urbana) cm (cruce)'][0])
            coory2 = int(ind2['Coordenada Y (Guia Urbana) cm (cruce)'][0])

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
            v = [calle1.strip(), calle2.strip()]
            v.sort()
            v.append((coorx1, coory1))
            w = [calle1.strip(), calle2prima.strip()]
            w.sort()
            w.append((coorx2, coory2))

            # Creamos vertices #
            grafo_madrid_e.agregar_vertice(v)
            grafo_madrid_e.agregar_vertice(w)
            grafo_madrid_a.agregar_vertice(v)
            grafo_madrid_a.agregar_vertice(w)

            # Creamos aristas #
            grafo_madrid_e.agregar_arista(v, w, data, dist)
            grafo_madrid_a.agregar_arista(v, w, data, peso)

    # NAVEGADOR #

    # Pedimos al usuario que introduzca las direcciones de origen y destino
    origen = input("Introduzca la dirección completa del origen tal y como está en la base de datos (Presione intro para finalizar): ")
    destino = input("Introduzca la dirección completa del destino tal y como está en la base de datos (Presione intro para finalizar): ")

    # Mientras estas direcciones no estén vacias
    while origen != '' and destino != '':

        # datos
        dir_o, coordenada_o = datos(direcciones, origen)
        dir_d, coordenada_d = datos(direcciones, destino)

        # El ususario debe decidir si quiere escoger la ruta
        continuar = True
        while continuar:
            op = str(input('¿Desea encontrar la ruta más corta(1) o más rápida(2)?: '))
            if op == '1' or op == '2':
                continuar = False
            else:
                print('No ha introducido una opción correcta, o 1 o 2')

        if op == 1:
            grafo_madrid = grafo_madrid_e
        else:
            grafo_madrid = grafo_madrid_a

        # Añadimos dos vértices nuevos al grafo, el origen y el destino
        grafo_madrid.agregar_vertice('origen')
        grafo_madrid.agregar_vertice('destino')

        # Buscamos el vértice del grafo más cercano al y añadimos una
        # arista entre estos dos
        cercano('origen', dir_o, coordenada_o, grafo_madrid)

        # Hacemos lo mismo para el destino
        cercano('destino', dir_d, coordenada_d, grafo_madrid)

        # Buscamos la ruta
        camino = grafo_madrid.camino_minimo('origen', 'destino')
        print(camino)

        aristas_camino = []
        for i in range(len(camino)-2):
            arista = (camino[i],camino[i+1])
            aristas_camino.append(arista)
        print(aristas_camino)


        # Pasamos a NetworkX
        # Sacamos las posiciones de los vértices
        pos = {}
        # Para cada vértice del grafo
        for v in grafo_madrid.vertices:
            if v != 'origen' and v != 'destino':
                objeto = grafo_madrid.vertices[v]
                # en la posición 3 de la lista de datos, se encuentran
                # sus coordenadas
                coordenadas = objeto.datos[2]
                pos[v] = coordenadas
        pos['origen'] = coordenada_o
        pos['destino'] = coordenada_d

        G = grafo_madrid.convertir_a_NetworkX()

        # Pintamos
        plot = plt.plot()
        nx.draw(G, pos=pos, node_size=0.1, width=0.1, edge_color='k')
        # nx.draw(camino, pos=pos, edge_color='b')
        nx.draw_networkx_nodes(G, pos=pos, nodelist=['origen', 'destino'], node_size=5, node_color='r')
        plt.show()

        origen = input("Introduzca la dirección completa del origen tal y como está en la base de datos (Presione intro para finalizar): ")
        destino = input("Introduzca la dirección completa del destino tal y como está en la base de datos (Presione intro para finalizar): ")
