import networkx as nx
import matplotlib.pyplot as plt
import os
from datetime import datetime

def crear_carpeta_steps():
    carpeta = "steps"
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    return carpeta


def guardar_imagen_final(G_original, grafo_residual, camino_final, layout_fijo, flujo_total):
    carpeta = crear_carpeta_steps()
    nombre = f"final_{datetime.now().strftime('%H%M%S%f')}.png"
    ruta = os.path.join(carpeta, nombre)

    plt.figure(figsize=(8, 6))

    pos = layout_fijo

    # ======================
    #   Construir grafo residual NX
    # ======================
    G_residual = nx.DiGraph()

    for u in grafo_residual:
        for v in grafo_residual[u]:
            cap = grafo_residual[u][v]
            if cap > 0:       # NO mostrar aristas sin capacidad
                G_residual.add_edge(u, v, capacidad=cap)

    # ======================
    #   Dibujar nodos
    # ======================
    nx.draw(
        G_residual,
        pos,
        with_labels=True,
        node_color="#4A90E2",
        node_size=1200,
        font_size=10,
        font_color="white",
        edge_color="gray",
        width=2
    )

    # ======================
    #   Mostrar capacidades residuales
    # ======================
    labels = nx.get_edge_attributes(G_residual, "capacidad")
    nx.draw_networkx_edge_labels(
        G_residual,
        pos,
        edge_labels=labels,
        font_size=9
    )

    # ======================
    #   Dibujar camino final en ROJO
    # ======================
    if camino_final and len(camino_final) >= 2:
        edges = list(zip(camino_final, camino_final[1:]))

        nx.draw_networkx_edges(
            G_residual,
            pos,
            edgelist=edges,
            width=3,
            edge_color="red"
        )

    plt.title(f"Grafo Residual Final (Flujo máximo = {flujo_total})")
    plt.tight_layout()
    plt.savefig(ruta, dpi=140)
    plt.close()

    return ruta
