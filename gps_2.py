import pandas as pd
import grafo
import networkx as nx
import matplotlib.pyplot as plt


def crear_grafo(cruces):
    '''
    Función que recive los dataframes para crear el grafo de la calle de la 
    comunidad de madrid
    '''
    # Inicializamod grafo
    grafo_madrid = grafo.Grafo()

    # Creamos vertices #

    # Recorremos toda la lista
    linea = 0
    fin = len(cruces) - 1
    while linea <= fin:
        # print('->', linea)
        # Cogemos los datos importantes de cada fila
        codigo = [int(cruces.loc[linea, 'Codigo de vía tratado']), int(cruces.loc[linea, 'Codigo de via que cruza o enlaza'])]
        coordenadas = [int(cruces.loc[linea, 'Coordenada X (Guia Urbana) cm (cruce)']), int(cruces.loc[linea, 'Coordenada Y (Guia Urbana) cm (cruce)'])]

        # Siempre que el cruce esté repetido en el dataframe, lo borramos de
        # este para que no se vuelva a añadir ese vertice
        try:
            # Para ello, siempre que sea posible se busca el indice en el que
            # se encuentra el cruce invertido y se elimina
            pos = cruces[cruces['Codigo de via que cruza o enlaza'] == codigo[0]]
            ind = pos[pos['Codigo de vía tratado'] == codigo[1]].index[0]
            cruces = cruces.drop([ind], axis=0).reset_index(drop=True)
            fin -= 1
        except:
            pass

        linea += 1

        # Añadimos el vertice a la clase nodo
        v = [codigo, coordenadas]
        grafo_madrid.agregar_vertice(v)

    # Rotondas/Glorietas/Plazas #
    # lista_calles = cruces['Codigo de vía tratado'].unique()
    i = 0
    fin_b = len(grafo_madrid.vertices)-1
    while i <= fin_b:
        j = i+1
        while j <= fin_b:
            if cercania(grafo_madrid.vertices[i].coordenadas, grafo_madrid.vertices[j].coordenadas, 10000):
                print(grafo_madrid.vertices[i].coordenadas, grafo_madrid.vertices[j].coordenadas)
                grafo_madrid.vertices[i].codigo.append(grafo_madrid.vertices[j].codigo) ### coger el que no está
                lista = media(grafo_madrid.vertices[i].coordenadas, grafo_madrid.vertices[j].coordenadas)
                grafo_madrid.vertices[i].coordenadas = lista
                grafo_madrid.eliminar_vertice(grafo_madrid.vertices[j])
                fin_b -= 1
            j += 1
        i += 1



    # Creamos aristas #

    return grafo_madrid


def cercania(l1, l2, n):
    if abs(l1[0]-l2[0]) > n:
        return False
    if abs(l1[1]-l2[1]) > n:
        return False
    print("Z")
    return True


def media(l1, l2):
    return [(l1[0]+l2[0])/2, (l1[1]+l2[1])/2]



if __name__ == "__main__":

    # Abrimos archivos
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

    grafo_madrid = crear_grafo(cruces)
