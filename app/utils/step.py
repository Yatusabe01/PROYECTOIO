# utils/step.py → VERSIÓN FINAL DEFINITIVA
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

    plt.figure(figsize=(16, 10))
    pos = layout_fijo

    edge_labels = {}
    edge_colors = []
    edge_widths = []

    for u, v, data in G_original.edges(data=True):
        cap = data.get("capacidad", 0)
        flujo = grafo_residual[v].get(u, 0)  # flujo real = capacidad residual contraria
        edge_labels[(u, v)] = f"{flujo}/{cap}"

        if flujo == cap and flujo > 0:
            edge_colors.append("#e74c3c")   # saturada
            edge_widths.append(6)
        elif flujo > 0:
            edge_colors.append("#e67e22")   # parcial
            edge_widths.append(4.5)
        else:
            edge_colors.append("#95a5a6")   # sin flujo
            edge_widths.append(2)

    nx.draw_networkx_nodes(G_original, pos,
                           node_size=3000, node_color="#4A90E2",
                           edgecolors="white", linewidths=5)
    nx.draw_networkx_labels(G_original, pos,
                            font_size=18, font_color="white", font_weight="bold")

    nx.draw_networkx_edges(G_original, pos,
                           width=edge_widths, edge_color=edge_colors,
                           arrows=True, arrowsize=45, arrowstyle="->",
                           connectionstyle="arc3,rad=0", alpha=0.95)

    nx.draw_networkx_edge_labels(G_original, pos,
                                 edge_labels=edge_labels,
                                 label_pos=0.25,
                                 font_size=14, font_weight="bold",
                                 font_color="black",
                                 bbox=dict(boxstyle="round,pad=0.5", facecolor="#f1c40f", alpha=0.9))

    plt.title(f"Red Residual Final → Flujo Máximo = {flujo_total}",
              fontsize=26, fontweight="bold", color="#2c3e50", pad=30)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(ruta, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()
    return ruta