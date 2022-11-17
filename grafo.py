import heapq
import sys
from typing import Dict, List, Tuple
import networkx as nx
import pandas as pd
import math

INFTY = sys.float_info.max


class Grafo:

    # Diseñar y construir la clase grafo

    def __init__(self, dirigido=False):
        """
        Crea un grafo dirigido o no dirigido.
        Args:
            dirigido: Flag que indica si el grafo es dirigido o no.
        Returns: Grafo o grafo dirigido (según lo indicado por el flag)
        inicializado sin vértices ni aristas.
        """
        self.dirigido = dirigido
        self.vertices = []
        self.aristas = []

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
        if v not in self.vertices:
            if v is None:
                raise ValueError("None cannot be a node")
            vertice = Vertice(v[0], v[1])
            self.vertices.append(vertice)
        return

    def agregar_arista(self, s: object, t: object, data: object, weight: float = 1) -> None:
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
        if s not in self.vertices:
            if s is None:
                raise ValueError("None cannot be a node")
            vertice = Vertice(s[0], s[1])
            self.vertices.append(vertice)
        if t not in self.vertices:
            if t is None:
                raise ValueError("None cannot be a node")
            vertice = Vertice(t[0], t[1])
            self.vertices.append(vertice)
        arista = Arista(s, t, data, weight)
        if arista not in self.aristas:
            self.aristas.append(arista)
        # if not self.dirigido:
        #     arista = Arista(t, s, data, weight)
        #     if arista not in self.aristas:
        #         self.aristas.append(arista)
        return

    def eliminar_vertice(self, v: object) -> None:
        """
        Si el objeto v es un vértice del grafo lo elimiina.
        Si no, no hace nada.
        Args: v vértice que se quiere eliminar
        Returns: None
        """
        if v in self.vertices:
            pos = self.vertices.index(v)
            self.vertices.pop(pos)
            for i in range(len(self.aristas)):
                if (self.aristas[i].vertice1 == v or self.aristas[i].vertice2 == v):
                    self.aristas.pop(i)
        return

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
        if (s in self.vertices) and (t in self.vertices):
            for i in range(len(self.aristas)):
                if (self.aristas[i].vertice1 == s and self.aristas[i].vertice2 == t) or (self.aristas[i].vertice1 == t and self.aristas[i].vertice2 == s):
                    self.aristas.pop(i)
                    return
            print("No se ha encontrado arista")
            return
        else:
            print("No se ha encontrado algun vertice")
            return

    def obtener_arista(self, s: object, t: object) -> Tuple[object,float] or None:
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
        if (s in self.vertices) and (t in self.vertices):
            for i in range(len(self.aristas)):
                if (self.aristas[i].vertice1 == s and self.aristas[i].vertice2 == t) or (self.aristas[i].vertice1 == t and self.aristas[i].vertice2 == s):
                    data = self.aristas[i].data
                    weight = self.aristas[i].weight
                    return (data, weight)
            print("No se ha encontrado arista")
            return
        else:
            print("No se ha encontrado algun vertice")
            return 

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
        lista = []
        if u in self.vertices:
            for ar in range(len(self.aristas)):
                if self.aristas[ar].vertice1 == u:
                    lista.append(self.aristas[ar].vertice2)
                elif self.aristas[ar].vertice2 == u:
                    lista.append(self.aristas[ar].vertice1)
            return lista
        else:
            return

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
        grado = 0
        if v in self.vertices:
            for ar in range(len(self.aristas)):
                if self.aristas[ar].vertice1 == v:
                    grado += 1
                if not self.es_dirigido() and self.aristas[ar].vertice2 == v:
                    grado += 1
            return grado
        else:
            return

    def grado_entrante(self, v: object) -> int or None:
        """
        Si el objeto u es un vértice del grafo, devuelve
        su grado entrante.
        Si no, devuelve None.
        Args: u vértice del grafo
        Returns: El grado entrante (int) si el vértice existe y
        None en caso contrario.
        """
        grado = 0
        if v in self.vertices:
            for ar in range(len(self.aristas)):
                if self.aristas[ar].vertice2 == v:
                    grado += 1
                if not self.es_dirigido() and self.aristas[ar].vertice1 == v:
                    grado += 1
            return grado
        else:
            return

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
        if v in self.vertices:
            return self.grado_saliente(v)
        else:
            return

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
        for v in self.vertices:
            padre[v] = None
            visitado[v] = False
            d[v] = math.inf
        
        d[origen] = 0
        Q = sorted([origen],v[d])
        while Q != None:
            Q.pop(Q[0])             #Creo que la lista es de menor a mayor
                                    #Quito el primer elemento
            if visitado[v] == False:
                visitado[v] = True
                for w in N:
                    if d[w] > d[v] + c:
                        d[w] = d[v] + c
                        padre[w] = v
                        Q.append(v)
        return padre

    def camino_minimo(self, origen: object, destino: object) -> List[object]:
        pass

    def prim(self) -> Dict[object, object]:
        """
        Calcula un Árbol Abarcador Mínimo para el grafo
        usando el algoritmo de Prim.
        Args: None
        Returns: Devuelve un diccionario que indica, para cada vértice del
        grafo, qué vértice es su padre en el árbol abarcador mínimo.
        """
        padres = []
        coste_minimo = []
        Q = sorted([],coste_minimo)
        for v in self.vertices:
            coste_minimo[v] = math.inf
            Q.append(v)
        while Q != None:
            Q.pop(Q[0]) 
            for w in N and Q:
                if c < coste_minimo[w]:
                    coste_minimo[w] = c
                    padre[w] = v
                    w.peso = c
        return padre

        

    def kruskal(self) -> List[Tuple[object, object]]:
        """
        Calcula un Árbol Abarcador Mínimo para el grafo
        usando el algoritmo de Prim.
        Args: None
        Returns: Devuelve una lista [(s1,t1),(s2,t2),...,(sn,tn)]
        de los pares de vértices del grafo
        que forman las aristas del arbol abarcador mínimo.
        """
        pass

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
        pass


class Vertice:
    def __init__(self, codigo, coordenadas):
        self.vertice = None
        self.codigo = codigo
        self.coordenadas = coordenadas


class Arista:
    def __init__(self, s: object, t: object, data: object, weight: float) -> None:
        self.vertice1 = s
        self.vertice2 = t
        self.data = data
        self.weight = weight
