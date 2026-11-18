import random
import math
import heapq
from collections import deque

class Nodo:
    def __init__(self, id_nodo, x=0.0, y=0.0):
        self.id = id_nodo
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.id)


class Arista:
    def __init__(self, origen, destino, dirigido=False, peso=None):
        self.origen = origen
        self.destino = destino
        self.dirigido = dirigido
        self.peso = peso if peso is not None else random.randint(1, 50)

    def __str__(self):
        conector = "->" if self.dirigido else "--"
        return f"{self.origen.id} {conector} {self.destino.id} [peso={self.peso}]"


class Grafo:
    def __init__(self, dirigido=False):
        self.nodos = {}
        self.aristas = []
        self.dirigido = dirigido

    def agregar_nodo(self, id_nodo, x=0.0, y=0.0):
        if id_nodo not in self.nodos:
            self.nodos[id_nodo] = Nodo(id_nodo, x, y)

    def agregar_arista(self, id_origen, id_destino, peso=None):
        if id_origen not in self.nodos:
            self.agregar_nodo(id_origen)
        if id_destino not in self.nodos:
            self.agregar_nodo(id_destino)
            
        nodo_origen = self.nodos[id_origen]
        nodo_destino = self.nodos[id_destino]
        
        self.aristas.append(Arista(nodo_origen, nodo_destino, self.dirigido, peso))

    def peso_total(self):
        """Calcula la suma de los pesos de todas las aristas del grafo/MST."""
        return sum(arista.peso for arista in self.aristas)

    def guardar_graphviz(self, nombre_archivo):
        tipo_grafo = "digraph" if self.dirigido else "graph"
        conector = "->" if self.dirigido else "--"
        
        with open(nombre_archivo, 'w') as f:
            f.write(f"{tipo_grafo} G {{\n")
            for nodo_id in self.nodos:
                f.write(f'    "{nodo_id}";\n')
            for arista in self.aristas:
                f.write(f'    "{arista.origen.id}" {conector} "{arista.destino.id}" [label={arista.peso}, weight={arista.peso}];\n')
            f.write("}\n")

    # =========================================================================
    # ALGORITMOS DE ÁRBOL DE EXPANSIÓN MÍNIMA (MST)
    # =========================================================================

    def KruskalD(self):
        mst = Grafo(dirigido=False)
        for nodo in self.nodos.values():
            mst.agregar_nodo(nodo.id, nodo.x, nodo.y)

        padre = {nodo_id: nodo_id for nodo_id in self.nodos}
        rango = {nodo_id: 0 for nodo_id in self.nodos}

        def find(u):
            if padre[u] != u:
                padre[u] = find(padre[u])
            return padre[u]

        def union(u, v):
            raiz_u = find(u)
            raiz_v = find(v)
            if raiz_u != raiz_v:
                if rango[raiz_u] < rango[raiz_v]:
                    padre[raiz_u] = raiz_v
                elif rango[raiz_u] > rango[raiz_v]:
                    padre[raiz_v] = raiz_u
                else:
                    padre[raiz_v] = raiz_u
                    rango[raiz_u] += 1
                return True
            return False

        aristas_ordenadas = sorted(self.aristas, key=lambda a: a.peso)

        for arista in aristas_ordenadas:
            u = arista.origen.id
            v = arista.destino.id
            if union(u, v):
                mst.agregar_arista(u, v, arista.peso)

        return mst

    def KruskalI(self):
        mst = Grafo(dirigido=False)
        for nodo in self.nodos.values():
            mst.agregar_nodo(nodo.id, nodo.x, nodo.y)

        ady = {nodo_id: set() for nodo_id in self.nodos}
        aristas_unicas = []
        vistas = set()

        for arista in self.aristas:
            u, v = arista.origen.id, arista.destino.id
            if u == v:
                continue
            par = tuple(sorted((u, v)))
            if par not in vistas:
                vistas.add(par)
                ady[u].add(v)
                ady[v].add(u)
                aristas_unicas.append(arista)
            else:
                for idx, a_existente in enumerate(aristas_unicas):
                    if tuple(sorted((a_existente.origen.id, a_existente.destino.id))) == par:
                        if arista.peso < a_existente.peso:
                            aristas_unicas[idx] = arista
                        break

        def sigue_conectado(origen, destino):
            visitados = {origen}
            cola = deque([origen])
            while cola:
                actual = cola.popleft()
                if actual == destino:
                    return True
                for vecino in ady[actual]:
                    if vecino not in visitados:
                        visitados.add(vecino)
                        cola.append(vecino)
            return False

        aristas_desc = sorted(aristas_unicas, key=lambda a: a.peso, reverse=True)

        for arista in aristas_desc:
            u, v = arista.origen.id, arista.destino.id
            ady[u].remove(v)
            ady[v].remove(u)

            if not sigue_conectado(u, v):
                ady[u].add(v)
                ady[v].add(u)
                mst.agregar_arista(u, v, arista.peso)

        return mst

    def Prim(self):
        mst = Grafo(dirigido=False)
        for nodo in self.nodos.values():
            mst.agregar_nodo(nodo.id, nodo.x, nodo.y)

        if not self.nodos:
            return mst

        ady = {nodo_id: [] for nodo_id in self.nodos}
        for arista in self.aristas:
            u, v, w = arista.origen.id, arista.destino.id, arista.peso
            if u != v:
                ady[u].append((w, v))
                ady[v].append((w, u))

        visitados = set()

        for nodo_inicio in self.nodos:
            if nodo_inicio in visitados:
                continue

            visitados.add(nodo_inicio)
            heap = []
            for peso, vecino in ady[nodo_inicio]:
                heapq.heappush(heap, (peso, nodo_inicio, vecino))

            while heap:
                peso, u, v = heapq.heappop(heap)
                if v not in visitados:
                    visitados.add(v)
                    mst.agregar_arista(u, v, peso)
                    for sig_peso, sig_vecino in ady[v]:
                        if sig_vecino not in visitados:
                            heapq.heappush(heap, (sig_peso, v, sig_vecino))

        return mst


# =========================================================================
# MODELOS GENERADORES DE GRAFOS (PROYECTO 1)
# =========================================================================

def grafoMalla(m, n, dirigido=False):
    g = Grafo(dirigido)
    for i in range(m):
        for j in range(n):
            g.agregar_nodo(f"n_{i}_{j}")
            
    for i in range(m):
        for j in range(n):
            origen = f"n_{i}_{j}"
            if i < m - 1:
                destino_x = f"n_{i+1}_{j}"
                g.agregar_arista(origen, destino_x)
            if j < n - 1:
                destino_y = f"n_{i}_{j+1}"
                g.agregar_arista(origen, destino_y)
                
    return g

def grafoErdosRenyi(n, m, dirigido=False):
    g = Grafo(dirigido)
    for i in range(n):
        g.agregar_nodo(str(i))
        
    aristas_creadas = set()
    while len(aristas_creadas) < m:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v:
            arista = tuple(sorted([u, v])) if not dirigido else (u, v)
            if arista not in aristas_creadas:
                aristas_creadas.add(arista)
                g.agregar_arista(str(u), str(v))
                
    return g

def grafoGilbert(n, p, dirigido=False):
    g = Grafo(dirigido)
    for i in range(n):
        g.agregar_nodo(str(i))
        
    for u in range(n):
        for v in range(n):
            if u != v and (dirigido or u < v):
                if random.random() < p:
                    g.agregar_arista(str(u), str(v))
    return g

def grafoGeografico(n, r, dirigido=False):
    g = Grafo(dirigido)
    for i in range(n):
        g.agregar_nodo(str(i), x=random.random(), y=random.random())
        
    nodos_lista = list(g.nodos.values())
    for i in range(n):
        for j in range(i + 1, n):
            nodo1 = nodos_lista[i]
            nodo2 = nodos_lista[j]
            distancia = math.sqrt((nodo1.x - nodo2.x)**2 + (nodo1.y - nodo2.y)**2)
            if distancia <= r:
                g.agregar_arista(nodo1.id, nodo2.id)
                if dirigido:
                    g.agregar_arista(nodo2.id, nodo1.id)
                    
    return g

def grafoBarabasiAlbert(n, d, dirigido=False):
    g = Grafo(dirigido)
    for i in range(d):
        g.agregar_nodo(str(i))
        
    for i in range(d):
        for j in range(i + 1, d):
            g.agregar_arista(str(i), str(j))
            if dirigido:
                g.agregar_arista(str(j), str(i))
                
    grados = []
    for arista in g.aristas:
        grados.append(arista.origen.id)
        grados.append(arista.destino.id)
        
    for i in range(d, n):
        nodo_nuevo = str(i)
        g.agregar_nodo(nodo_nuevo)
        
        objetivos = set()
        while len(objetivos) < d and len(grados) > 0:
            candidato = random.choice(grados)
            if candidato != nodo_nuevo:
                objetivos.add(candidato)
                
        for obj in objetivos:
            g.agregar_arista(nodo_nuevo, obj)
            grados.append(nodo_nuevo)
            grados.append(obj)
            
    return g

def grafoDorogovtsevMendes(n, dirigido=False):
    g = Grafo(dirigido)
    for i in range(3):
        g.agregar_nodo(str(i))
        
    g.agregar_arista("0", "1")
    g.agregar_arista("1", "2")
    g.agregar_arista("2", "0")
    
    for i in range(3, n):
        nodo_nuevo = str(i)
        g.agregar_nodo(nodo_nuevo)
        arista_elegida = random.choice(g.aristas)
        g.agregar_arista(nodo_nuevo, arista_elegida.origen.id)
        g.agregar_arista(nodo_nuevo, arista_elegida.destino.id)
        
    return g