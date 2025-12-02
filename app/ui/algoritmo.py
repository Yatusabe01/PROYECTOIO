from collections import defaultdict
import networkx as nx

class Grafo:

    def __init__(self):
        self.grafo = defaultdict(dict)

    def agregar_arista(self, u, v, c):
        self.grafo[u][v] = c

    # BFS estándar para encontrar camino aumentante
    def bfs(self, fuente, sumidero, padre):
        visitado = set()
        cola = [fuente]
        visitado.add(fuente)

        while cola:
            u = cola.pop(0)
            for v in self.grafo[u]:
                if v not in visitado and self.grafo[u][v] > 0:
                    cola.append(v)
                    visitado.add(v)
                    padre[v] = u
                    if v == sumidero:
                        return True
        return False
    def ford_fulkerson(self, fuente, sumidero, registrar_paso=None):
        padre = {}
        flujo_max = 0

        G_nx = nx.DiGraph()
        for u in self.grafo:
            for v in self.grafo[u]:
                G_nx.add_edge(u, v, capacidad=self.grafo[u][v])

        # Bucle principal FF
        while self.bfs(fuente, sumidero, padre):

            camino = []
            v = sumidero
            flujo_camino = float("inf")

            while v != fuente:
                camino.append(v)
                u = padre[v]
                flujo_camino = min(flujo_camino, self.grafo[u][v])
                v = u
            camino.append(fuente)
            camino.reverse()

            flujo_max += flujo_camino

            v = sumidero
            while v != fuente:
                u = padre[v]
                self.grafo[u][v] -= flujo_camino

                if self.grafo[v].get(u) is None:
                    self.grafo[v][u] = 0
                self.grafo[v][u] += flujo_camino

                v = u

        return flujo_max
