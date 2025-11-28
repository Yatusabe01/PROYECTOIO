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
    """
    Genera una imagen FINAL limpia y consistente con la visualización principal.
    Muestra: flujo/capacidad en cada arista original.
    Colores: rojo (saturada), naranja (parcial), gris (sin flujo).
    MISMO LAYOUT que el grafo principal → ¡nunca se apelotonan los nodos!
    Sin leyenda, sin líneas verdes, sin curvas.
    """
    carpeta = crear_carpeta_steps()
    nombre = f"final_{datetime.now().strftime('%H%M%S%f')}.png"
    ruta = os.path.join(carpeta, nombre)

    plt.figure(figsize=(14, 9))
    pos = layout_fijo  # ← ¡CLAVE! Mismo layout que el grafo principal

    # Diccionarios para etiquetas y estilos
    edge_labels = {}
    edge_colors = []
    edge_widths = []

    # Recorrer todas las aristas originales
    for u, v, data in G_original.edges(data=True):
        cap_original = data.get("capacidad", 0)

        # Flujo real que pasó por (u → v) = capacidad residual en dirección contraria
        flujo_real = grafo_residual[v].get(u, 0)

        # Etiqueta didáctica: flujo/capacidad
        edge_labels[(u, v)] = f"{flujo_real}/{cap_original}"

        # Estilo según uso
        if flujo_real == cap_original and flujo_real > 0:
            edge_colors.append("#e74c3c")  # Rojo saturada
            edge_widths.append(5)
        elif flujo_real > 0:
            edge_colors.append("#e67e22")  # Naranja parcial
            edge_widths.append(3.5)
        else:
            edge_colors.append("#95a5a6")  # Gris sin flujo
            edge_widths.append(1.5)

    # === DIBUJAR TODO ===
    # Nodos (igual que en tu grafo principal)
    nx.draw_networkx_nodes(
        G_original, pos,
        node_color="#4A90E2",
        node_size=1400,
        linewidths=2.5,
        edgecolors="white"
    )

    nx.draw_networkx_labels(
        G_original, pos,
        font_size=14,
        font_color="white",
        font_weight="bold"
    )

    # Aristas originales con grosor y color según flujo
    nx.draw_networkx_edges(
        G_original, pos,
        width=edge_widths,
        edge_color=edge_colors,
        arrows=True,
        arrowsize=25,
        arrowstyle="->",
        connectionstyle="arc3,rad=0"  # ← ¡LÍNEAS RECTAS!
    )

    # Etiquetas flujo/capacidad (fondo amarillo suave, sin bordes molestos)
    nx.draw_networkx_edge_labels(
        G_original, pos,
        edge_labels=edge_labels,
        font_size=11,
        font_color="black",
        font_weight="bold",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#f1c40f", alpha=0.8)  # amarillo suave
    )


    plt.axis("off")
    plt.tight_layout()
    plt.savefig(ruta, dpi=200, bbox_inches="tight", facecolor="white", edgecolor="none")
    plt.close()

    return ruta