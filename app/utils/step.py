# app/utils/step.py
# Con fondo gris para mantener consistencia visual

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
    if not G_original.nodes:
        return None

    carpeta = crear_carpeta_steps()
    nombre = f"final_{datetime.now().strftime('%H%M%S%f')}.png"
    ruta = os.path.join(carpeta, nombre)

    # Figura con fondo gris claro igual que grafo_visu.py
    fig, ax = plt.subplots(figsize=(18, 10))
    fig.patch.set_facecolor('#f8f9fa')
    ax.set_facecolor('#f8f9fa')
    
    pos = layout_fijo or nx.spring_layout(G_original, seed=42)

    edge_labels = {}
    edge_colors = []
    edge_widths = []

    for u, v in G_original.edges():
        cap = G_original[u][v]['capacity']
        flujo = grafo_residual[v].get(u, 0)  # flujo real = capacidad inversa en residual
        edge_labels[(u, v)] = f"{flujo}/{cap}"

        if flujo == cap and flujo > 0:
            edge_colors.append("#e74c3c")
            edge_widths.append(8)
        elif flujo > 0:
            edge_colors.append("#e67e22")
            edge_widths.append(6)
        else:
            edge_colors.append("#95a5a6")
            edge_widths.append(2)

    nx.draw_networkx_nodes(G_original, pos, node_size=3500, node_color="#4A90E2",
                           edgecolors="white", linewidths=6, ax=ax)
    nx.draw_networkx_nodes(G_original, pos, node_size=3500, node_color="#4A90E2",
                           edgecolors="white", linewidths=6, ax=ax)
    nx.draw_networkx_labels(G_original, pos, font_size=20, font_color="white", 
                           font_weight="bold", ax=ax)
    
    nx.draw_networkx_edges(G_original, pos, width=edge_widths, edge_color=edge_colors,
                           arrows=True, arrowsize=50, arrowstyle="->", alpha=0.95,
                           min_source_margin=30, min_target_margin=30, ax=ax)
    
    nx.draw_networkx_edge_labels(G_original, pos, edge_labels=edge_labels,
                                 label_pos=0.15,  # ← MUY CERCA DEL ORIGEN
                                 font_size=18, font_weight="bold",
                                 font_color="white",
                                 bbox=dict(facecolor="#f39c12", alpha=0.9, boxstyle="round,pad=0.6"))

    ax.set_title(f"Red Residual Final → Flujo Máximo = {flujo_total}",
                 fontsize=30, fontweight="bold", color="#2c3e50", pad=40)
    ax.axis("off")
    plt.tight_layout()
    
    # Guardar con fondo gris
    plt.savefig(ruta, dpi=200, bbox_inches="tight", facecolor="#f8f9fa", edgecolor="none")
    plt.close()

    return ruta