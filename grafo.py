import heapq
import sys
from typing import Dict, List, Tuple
import networkx as nx
import pandas as pd
import ast

INFTY = sys.float_info.max


class Grafo:

    # Diseñar y construir la clase grafo

    def __init__(self, dirigido):
        """
        Crea un grafo dirigido o no dirigido.
        Args:
            dirigido: Flag que indica si el grafo es dirigido o no.
        Returns: Grafo o grafo dirigido (según lo indicado por el flag)
        inicializado sin vértices ni aristas.
        """
        self.dirigido = dirigido
        self.vertices = {}
        # self.aristas = []

    #### Operaciones básicas del TAD ####

    def es_dirigido(self) -> bool:
        """
        Indica si el grafo es dirigido o no
        Args: None
        Returns: True si el grafo es dirigido, False si no.
        """
        return self.dirigido

    def agregar_vertice(self, v: object) -> None:
        """
        Agrega el vértice v al grafo.
        Args: v vértice que se quiere agregar
        Returns: None
        """
        # Solo si v no está en el grafo, se añade
        if str(v) not in self.vertices:
            # Si es none -> Error
            if v is None:
                raise ValueError("None cannot be a node")
            vertice = Vertice(v)
            self.vertices[str(v)] = vertice

    def agregar_arista(self, s: object, t: object, data: object, weight: float) -> None:
        """
        Si los objetos s y t son vértices del grafo, agrega
        una arista al grafo que va desde el vértice s hasta el vértice t
        y le asocia los datos "data" y el peso weight.
        En caso contrario, no hace nada.
        Args:
            s: vértice de origen (source)
            t: vértice de destino (target)
            data: datos de la arista
            weight: peso de la arista
        Returns: None
        """
        # Agregamos los vertices
        self.agregar_vertice(s)
        self.agregar_vertice(t)

        # Si t no está en la lista de adyacencia de s, se añade
        vertice_s = self.vertices[str(s)]
        if str(t) not in vertice_s.adyacencia:
            vertice_s.adyacencia[str(t)] = [data, weight]

        # Si no es dirigido el grafo se añade del sentido contrario
        if not self.es_dirigido():
            # Si s no está en la lista de adyacencia de t, se añade
            vertice_t = self.vertices[str(t)]
            if str(s) not in vertice_s.adyacencia:
                vertice_t.adyacencia[str(s)] = [data, weight]

    def eliminar_vertice(self, v: object) -> None:
        """
        Si el objeto v es un vértice del grafo lo elimiina.
        Si no, no hace nada.
        Args: v vértice que se quiere eliminar
        Returns: None
        """
        if str(v) in self.vertices:
            # Objeto vertice
            vertice = self.vertices[str(v)]
            # Lista de adyacencia de v
            lista = list(vertice.adyacencia.keys())
            if self.es_dirigido():  # Si el grafo es dirigido
                # Para cada vertice del grafo
                for j in self.vertices:
                    vertice_j = self.vertices[j]
                    lista_j = list(vertice_j.adyacencia.keys())
                    if str(v) in lista_j:  # Si v está en la lista de adyacencia
                        # Lo eliminamos de esta
                        vertice_j.adyacencia.pop(str(v), None)
            else:  # Si no es dirigido
                # Para cada vertice adyacente con v
                # eliminamos v de su lista de ayacencia
                for i in lista:
                    vertice_a = self.vertices[i]
                    vertice_a.adyacencia.pop(str(v), None)
            self.vertices.pop(v, None)

    def eliminar_arista(self, s: object, t: object) -> None:
        """
        Si los objetos s y t son vértices del grafo y existe
        una arista de s a t la elimina.
        Si no, no hace nada.
        Args:
            s: vértice de origen de la arista
            t: vértice de destino de la arista
        Returns: None
        """

        if str(s) in self.vertices:
            # Objeto vertice
            vertice_s = self.vertices[str(s)]
            # Lista de adyacencia de s
            lista = list(vertice_s.adyacencia.keys())
            # Si el vertice t es adyacente con s
            # lo eliminamos de su lista de ayacencia
            if str(t) in lista:
                vertice_s.adyacencia.pop(str(t), None)

        # Si no es dirigido
        if not self.es_dirigido() and str(t) in self.vertices:
            # Objeto vertice
            vertice_t = self.vertices[str(t)]
            # Lista de adyacencia de s
            lista = list(vertice_t.adyacencia.keys())
            # Si el vertice s es adyacente con t
            # lo eliminamos de su lista de ayacencia
            if str(s) in lista:
                vertice_t.adyacencia.pop(str(s), None)

    def obtener_arista(self, s: object, t: object) -> Tuple[object, float] or None:
        """
        Si los objetos s y t son vértices del grafo y existe
        una arista de u a v, devuelve sus datos y su peso en una tupla.
        Si no, devuelve None
        Args:
            s: vértice de origen de la arista
            t: vértice de destino de la arista
        Returns: Una tupla (a,w) con los datos de la arista "a" y su peso
        "w" si la arista existe. None en caso contrario.
        """
        if (str(s) in self.vertices) and (str(t) in self.vertices):
            try:
                vertice = self.vertices[str(s)]
                # Lista de adyacencia de s
                datos = vertice.adyacencia[str(t)]
                return datos
            except:
                vertice = self.vertices[str(t)]
                # Lista de adyacencia de s
                datos = vertice.adyacencia[str(s)]
                return datos

    def lista_adyacencia(self, u: object) -> List[object] or None:
        """
        Si el objeto u es un vértice del grafo, devuelve
        su lista de adyacencia.
        Si no, devuelve None.
        Args: u vértice del grafo
        Returns: Una lista [v1,v2,...,vn] de los vértices del grafo
        adyacentes a u si u es un vértice del grafo y None en caso
        contrario
        """
        if str(u) in self.vertices:
            vertice = self.vertices[str(u)]
            return list(vertice.adyacencia.keys())

    #### Grados de vértices ####

    def grado_saliente(self, v: object) -> int or None:
        """
        Si el objeto v es un vértice del grafo, devuelve
        su grado saliente.
        Si no, devuelve None.
        Args: v vértice del grafo
        Returns: El grado saliente (int) si el vértice existe y
        None en caso contrario.
        """
        # El grado saliente es el número de vertices que haya en
        # su lista de adyacencia
        if str(v) in self.vertices:
            vertice = self.vertices[str(v)]
            return len(list(vertice.adyacencia.keys()))

    def grado_entrante(self, v: object) -> int or None:
        """
        Si el objeto u es un vértice del grafo, devuelve
        su grado entrante.
        Si no, devuelve None.
        Args: u vértice del grafo
        Returns: El grado entrante (int) si el vértice existe y
        None en caso contrario.
        """
        if str(v) in self.vertices:
            grado = 0
            # Para cada vertice en el diccionario vertices
            for w in list(self.vertices.keys()):
                vertice = self.vertices[w]
                # Si v está en su diccionario de adyacencia
                if str(v) in list(vertice.adyacencia.keys()):
                    # Sumamos 1 al grado del grafo
                    grado += 1
            return grado

    def grado(self, v: object) -> int or None:
        """
        Si el objeto v es un vértice del grafo, devuelve
        su grado si el grafo no es dirigido y su grado saliente si
        es dirigido.
        Si no pertenece al grafo, devuelve None.
        Args: u vértice del grafo
        Returns: El grado (int) o grado saliente (int) según corresponda
        si el vértice existe y None en caso contrario.
        """
        # Como para los grafos no dirigidos el grado entrante y el saliente
        # son iguales, y para los dirigidos hay que devolver el saliente,
        # para los dos devolvemos el saliente
        if str(v) in self.vertices:
            return self.grado_saliente(v)

    #### Algoritmos ####

    def dijkstra(self, origen: object) -> Dict[object, object]:
        """
        Calcula un Árbol Abarcador Mínimo para el grafo partiendo
        del vértice "origen" usando el algoritmo de Dijkstra. Calcula únicamente
        el árbol de la componente conexa que contiene a "origen".
        Args: origen vértice del grafo de origen
        Returns: Devuelve un diccionario que indica, para cada vértice alcanzable
        desde "origen", qué vértice es su padre en el árbol abarcador mínimo.
        """
        # Inicializamos todos los diccionarios
        padre = {}
        visitado = {}
        d = {}
        for v in self.vertices:
            padre[v] = None
            visitado[v] = False
            d[v] = INFTY

        # La distancia del punto de partida es 0
        d[str(origen)] = 0

        # Ordenamos los vértices de menor a mayor distancia
        Q = sorted(d, key=d.get)

        # Recorremos todos los vértices
        while Q != []:
            # Cogemos el vértice más cercano
            v = Q.pop(0)
            # Siempre que ese vértice no haya sido visitado anteriormente
            if not visitado[v]:
                # Ahora sí está visitado
                visitado[v] = True
                # Estudiamos todos los vértices adyacentes a él
                for w in self.vertices[v].adyacencia:
                    # Si ese vértice adyacente no había sido visitado
                    if not visitado[w]:
                        # Recalculamos distancias
                        if d[w] > d[v] + self.vertices[v].adyacencia[w][1]:
                            d[w] = d[v] + self.vertices[v].adyacencia[w][1]
                            padre[w] = v
                # Volvemos a ordenar los vértices
                d.pop(v, None)
                Q = sorted(d, key=d.get)
            else:
                d.pop(v, None)
        return padre


    def camino_minimo(self, origen: object, destino: object) -> List[object]:
        """ Calcula el camino mínimo desde el vértice origen hasta el vértice
        destino utilizando el algoritmo de Dijkstra.
        Args:
            origen: vértice del grafo de origen
            destino: vértice del grafo de destino
        Returns: Devuelve una lista con los vértices del grafo por los que pasa
        el camino más corto entre el origen y el destino. El primer elemento de
        la lista es origen y el último destino.
        """

        padre = self.dijkstra(origen)
        vertice = destino
        camino = [vertice]
        while vertice != origen:
            vertice = padre[vertice]
            camino.append(vertice)

        camino.reverse()
        return camino


    def prim(self) -> Dict[object, object]:
        """
        Calcula un Árbol Abarcador Mínimo para el grafo
        usando el algoritmo de Prim.
        Args: None
        Returns: Devuelve un diccionario que indica, para cada vértice del
        grafo, qué vértice es su padre en el árbol abarcador mínimo.
        """
        padre = {}
        coste_minimo = {}
        for v in self.vertices:
            padre[v] = None
            coste_minimo[v] = INFTY

        # Ordenamos los vértices de menor a mayor distancia
        Q = sorted(coste_minimo, key=coste_minimo.get)

        while Q != []:
            v = Q.pop(0)
            # Para todos los vertices adyacentes a v y que estén en Q
            for w in self.vertices[v].adyacencia:
                if w in Q:
                    # Actualizamos los costes
                    if coste_minimo[w] > self.vertices[v].adyacencia[w][1]:
                        coste_minimo[w] = self.vertices[v].adyacencia[w][1]
                        padre[w] = v
            # Volvemos a ordenar los vértices
            coste_minimo.pop(v, None)
            Q = sorted(coste_minimo, key=coste_minimo.get)
        return padre

    def kruskal(self) -> List[Tuple[object, object]]:
        """ Calcula un Árbol Abarcador Mínimo para el grafo
        usando el algoritmo de Kruskal.  
        Args: None
        Returns: Devuelve una lista [(s1,t1),(s2,t2),...,(sn,tn)]
        de los pares de vértices del grafo
        que forman las aristas del arbol abarcador mínimo.
        """
        dict = {}
        c = []
        for v in self.vertices:
            c.append([v])
            # Objeto vertice
            vertice = self.vertices[v]
            # Lista de adyacencia de v
            lista_a = list(vertice.adyacencia.keys())
            for u in lista_a:  # Si el vertice t es adyacente con s
                ar = [v, u]
                ar.sort()
                aristas = list(dict.values())
                if ar not in aristas:
                    peso = self.vertices[v].adyacencia[u][1]
                    dict[str(ar)] = peso

        L = sorted(dict, key=dict.get)

        aristas_conexas = []
        while L != []:
            a = ast.literal_eval(L.pop(0))
            v = a[0]
            u = a[1]
            for k in c:
                if (v in k):
                    com_v = k
                if (u in k):
                    com_u = k

            if com_u != com_v:
                c.remove(com_u)
                c.remove(com_v)
            else:
                c.remove(com_v)

            if not self.comun(com_v, com_u):
                joined = com_v + com_u
                c.append(joined)
                aristas_conexas.append(a)
            else:
                c.append(com_v)

        return aristas_conexas

    def comun(self, l1, l2):
        for j in l1:
            if j in l2:
                return True
        return False

    #### NetworkX ####

    def convertir_a_NetworkX(self) -> nx.Graph or nx.DiGraph:
        """
        Construye un grafo o digrafo de Networkx según corresponda
        a partir de los datos del grafo actual.
        Args: None
        Returns: Devuelve un objeto Graph de NetworkX si el grafo es
        no dirigido y un objeto DiGraph si es dirigido. En ambos casos,
        los vértices y las aristas son los contenidos en el grafo dado.
        """
        if self.es_dirigido():
            G = nx.DiGraph()
        else:
            G = nx.Graph()

        # vertices
        vertices = list(self.vertices.keys())
        G.add_nodes_from(vertices)

        # aristas
        for v in self.vertices:
            ady = self.lista_adyacencia(v)
            for u in ady:
                if v != u:
                    G.add_edge(v, u)

        return G


class Vertice:
    def __init__(self, datos):
        self.datos = datos
        self.adyacencia = {}
