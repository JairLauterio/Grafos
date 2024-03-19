import heapq

from Arco import Arco
from Nodo import Nodo
from enum import Enum

#Hacer enumeraciones dandole un valor de string un int en este caso BLANCO == 1
class Color (Enum):
    GRIS = 1
    BLANCO = 2
    NEGRO =3

class Grafo:
    def __init__(self,nombre):
        self.nombre = nombre
        self.V = {}
        self.E = []
        self.tiempo = 0

    def addNodo(self,nodo):
        """
        :param nodo: debe ser el nombre del nodo (str), no tipo nodo. Porque el nodo se crea en esta funcion
        :return: void
        """
        if nodo not in self.V:
            self.V[nodo] = Nodo(nodo)


    def getNodo(self,nodo):
        """
        :param nodo: debe ser un str con el nombre del nodo
        :return: si existe un nodo con ese nombre regresa el objeto nodo, sino regresa None
        """
        return self.V.get(nodo,None)

    def addArco(self,origen,destino,costo):
        """
        :param origen: str con el nombre del nodo origen
        :param destino: str con el nombre del nodo destino
        :param costo: str con el costo del arco
        :return:
        """
        if self.getNodo(origen) is not None and self.getNodo(destino) is not None:
            arco = Arco(self.V[origen],self.V[destino],float(costo))
            self.V[origen].addAdyacente(self.V[destino])
            self.E.append(arco)

    def getArco(self,u,v):
        """
        :param u: str del nodo origen
        :param v: str del nodo destino
        :return: el arco, sino existe un arco regresa el None
        """
        for a in self.E:
            if a.origen.nombre == u and a.destino.nombre == v:
                return a
        return None

    def BFS(self, s):
        for u in self.V.values():
            u.color = Color.BLANCO
            u.d = float("Inf")
            u.padre = None
        s = self.getNodo(s)
        s.d = 0
        Q = []
        Q.append(s)
        while len(Q) > 0:
            u = Q.pop(0)
            for v in u.adyacentes:
                if v.color == Color.BLANCO:
                    v.color = Color.GRIS
                    v.d = u.d + 1
                    v.padre = u
                    Q.append(v)
                u.color = Color.NEGRO

    def DFS(self):
        for u in self.V.values():
            u.color = Color.BLANCO
            u.padre = None

        tiempo = 0
        for u in self.V.values():
            if u.color == Color.BLANCO:
                tiempo = self.DFSVisit(u,tiempo)


    def DFSVisit(self,u,tiempo):
        u.color = Color.GRIS
        tiempo += 1
        u.d = tiempo
        for v in u.adyacentes:
            if v.color == Color.BLANCO:
                v.padre = u
                tiempo = self.DFSVisit(v,tiempo)
        u.color = Color.NEGRO
        tiempo += 1
        u.f = tiempo
        return tiempo

    def getTranspuesta(self):
        e = Grafo(self.nombre+'_T')
        for u in self.V.values():
            e.addNodo(u.nombre)
        for v in self.E:
            e.addArco(v.destino.nombre,v.origen.nombre,v.costo)
        return e

    def getListFDec(self):
        timeDicc = {}
        for u in self.V.values():
            timeDicc.update({f'{u.nombre}': u.f})
        timeDiccOrder = dict(
            sorted(timeDicc.items(),
                   key=lambda item: item[1],
                   reverse=True))

        return timeDiccOrder

    def getFDesc(self):
        lista = []
        lista_nodos = sorted(self.V.values(),key=lambda x:x.f,reverse=True)
        for nodo in lista_nodos:
            lista.append(nodo.nombre)
        return lista

    def getOrderGrafo(self,dicc):
        g = Grafo('aux')
        for k in dicc.keys():
            g.addNodo(k)
        for v in self.E:
            g.addArco(v.origen.nombre,v.destino.nombre,v.costo)
        g.E = self.E
        return g

    def scc(self):
        self.DFS()
        gt = self.getTranspuesta()
        ordenDescendente = self.getFDesc()

        for u in gt.V.values():
            u.color = Color.BLANCO
            u.padre = None
        tiempo = 0
        bosque = []
        for a in ordenDescendente:
            u = gt.getNodo(a)
            if u.color == Color.BLANCO:
                arbol = []
                tiempo = gt.sccVisit(u,tiempo,arbol)
                bosque.append(arbol)
        return bosque

    def sccVisit(self,u,tiempo,arbol):
        arbol.append(u)
        u.color = Color.GRIS
        tiempo += 1
        u.d = tiempo
        for v in u.adyacentes:
            if v.color == Color.BLANCO:
                v.padre = u
                tiempo = self.sccVisit(v,tiempo,arbol)
        u.color = Color.NEGRO
        tiempo += 1
        u.f = tiempo
        return tiempo

    def get_keys_from_value(self,d,val):
        return [k for k, v in d.items() if v == val]
    def mstKruskal(self):
        g = Grafo(self.nombre+'_kruskal')
        diccionary = {}
        c = 0
        for nodo in self.V.values():
            diccionary[nodo.nombre] = c
            c += 1
        arcosOrdenados = self.getAscAristas()
        for arco in arcosOrdenados:
            # recibe los vertices de origen y destino que son los keys del diccionary y regresa los values
            u = diccionary.get(arco.origen.nombre)
            v = diccionary.get(arco.destino.nombre)
            if u != v:
                g.addNodo(arco.origen.nombre)
                g.addNodo(arco.destino.nombre)
                g.addArco(arco.origen.nombre,arco.destino.nombre,arco.costo)
                g.addArco(arco.destino.nombre,arco.origen.nombre, arco.costo)
                valorCambiar = v
                for d in diccionary:
                    if diccionary[d] == valorCambiar:
                        diccionary[d] = u
        return g


    def getAscAristas(self):
        lista = []
        lista_aristas = sorted(self.E,key=lambda x:x.costo,reverse=False)
        for arco in lista_aristas:
            lista.append(arco)
        return lista


    def prim(self, r):
        g = Grafo(self.nombre + '_prim')
        for u in self.V.values():
            u.d = float("Inf")
            u.padre = None
        r = self.getNodo(r)
        r.d = 0
        Q = []
        for u in self.V.values():
            Q.append(u)
            while len(Q)>0:
                u=min(Q,key=lambda u:u.d)
                Q.remove(u)
                g.addNodo(u.nombre)
                g.getNodo(u.nombre).d =u.d
                g.getNodo(u.nombre).padre = u.padre
                if u.padre != None:
                    g.addArco(u.padre.nombre, u.nombre, u.d-u.padre.d)
                    g.addArco(u.nombre, u.padre.nombre, u.d-u.padre.d)
                for v in u.adyacentes:
                    costo=self.getW(u,v)
                    if costo == float("Inf"):
                        continue
                    if v in Q and costo+u.d < v.d:
                        v.d = costo+u.d
                        v.padre = u
            return g

    def mst_dijkstra(self, nodo):
        g = Grafo(self.nombre + '_Dijkstra')
        Q = []
        arcos = {}
        for u in self.V.values():
            g.addNodo(u.nombre)
            g_nodo = g.getNodo(u.nombre)
            g_nodo.d = float('Inf')
            g_nodo.padre = None
            Q.append(g_nodo)
        nodo = g.getNodo(nodo)
        nodo.d = 0
        while Q:
            nodo_min_d = g.get_min_d(Q)
            nodo_original = self.getNodo(nodo_min_d.nombre)
            for destino in nodo_original.adyacentes:
                # relax
                if g.getNodo(destino.nombre) in Q:
                    if nodo_min_d.d + self.get_costo(nodo_min_d.nombre, destino.nombre) < destino.d:
                        arcos[destino.nombre] = [nodo_min_d.nombre, self.get_costo(nodo_min_d.nombre, destino.nombre),
                                                 nodo_min_d.d]
                        destino_g = g.getNodo(destino.nombre)
                        destino_g.d = arcos[destino.nombre][1] + arcos[destino.nombre][2]
            Q.remove(nodo_min_d)
        for destino, values in arcos.items():
            g.addArco(values[0], destino, values[1])
        return g

    def get_costo(self, u, v):
        arco = self.getArco(u, v)
        return arco.costo

    def get_min_d(self, Q):
        min = float('Inf')
        min_nodo = None
        for nodo in Q:
            if nodo.d < min:
                min = nodo.d
                min_nodo = nodo
        return min_nodo

    def mst_bellman_ford(self, start_node):
        arcos = {}
        for u in self.V.values():
            u.d= float('inf')
            u.padre = None

        start_node = self.getNodo(start_node)
        start_node.d = 0

        for _ in range(len(self.V) - 1):
            for arc in self.E:
                if arc.origen.d + arc.costo < arc.destino.d:
                    arc.destino.d = arc.origen.d + arc.costo
                    arc.destino.padre = arc.origen

        bellman_ford_graph  =Grafo(self.nombre + '_Dijkstra')
        for node in self.V.values():
            bellman_ford_graph.addNodo(node.nombre)
            bellman_ford_graph.getNodo(node.nombre).d = node.d
            bellman_ford_graph.getNodo(node.nombre).padre = node.padre

        for arc in self.E:
            origen = arc.origen.nombre
            destino = arc.destino.nombre
            costo = arc.costo
            bellman_ford_graph.addArco(origen, destino, costo)

        return bellman_ford_graph


    def __str__(self):
        """
        :return:  se manda a imprimir cada nodo para hacer el grafo o la lista de grafos
        """
        resultado = self.nombre + ":\n"
        for nodo in self.V.values():
            resultado += str(nodo) + "\n"
        return resultado
