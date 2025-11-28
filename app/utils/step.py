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
    Genera una imagen FINAL MUY DIDÁCTICA del grafo residual + flujo real
    """
    carpeta = crear_carpeta_steps()
    nombre = f"final_didactico_{datetime.now().strftime('%H%M%S%f')}.png"
    ruta = os.path.join(carpeta, nombre)

    plt.figure(figsize=(14, 9))  # Más grande = más claro
    pos = layout_fijo

    # -------------------------------------------------
    # 1. Construir grafo residual con TODOS los nodos
    # -------------------------------------------------
    G_vis = nx.DiGraph()
    for nodo in G_original.nodes():
        G_vis.add_node(nodo)

    edge_labels = {}        # Para mostrar "flujo/capacidad_original"
    edge_colors = []        # Color de la arista
    edge_widths = []        # Grosor según flujo
    residual_edges = []     # Solo para dibujar flechas residuales

    # -------------------------------------------------
    # 2. Recorrer TODAS las aristas originales
    # -------------------------------------------------
    for u, v, data in G_original.edges(data=True):
        cap_original = data.get("capacidad", 0)
        
        # Capacidad residual forward (u → v)
        cap_residual_uv = grafo_residual[u].get(v, 0)
        # Capacidad residual backward (v → u) → indica flujo que pasó
        cap_residual_vu = grafo_residual[v].get(u, 0)
        
        flujo_real = cap_residual_vu  # ¡Esto es el flujo que realmente pasó por (u,v)!
        
        # Guardamos etiqueta didáctica: flujo/capacidad_original
        edge_labels[(u, v)] = f"{flujo_real}/{cap_original}"

        # -------------------------------------------------
        # Colorear y engrosar según el estado
        # -------------------------------------------------
        if flujo_real == cap_original and flujo_real > 0:
            # Saturada (todo el flujo posible pasó)
            edge_colors.append("#e74c3c")    # rojo fuerte
            edge_widths.append(4.5)
        elif flujo_real > 0:
            # Parcialmente usada
            edge_colors.append("#f39c12")    # naranja
            edge_widths.append(3.5)
        else:
            # Sin flujo
            edge_colors.append("#95a5a6")    # gris
            edge_widths.append(1.5)

        # -------------------------------------------------
        # Dibujar arista residual SOLO si tiene capacidad residual > 0
        # -------------------------------------------------
        if cap_residual_uv > 0:
            G_vis.add_edge(u, v, capacidad=cap_residual_uv)
            residual_edges.append((u, v))

    # -------------------------------------------------
    # 3. Dibujar todo
    # -------------------------------------------------
    # Fondo limpio
    plt.background = "white"

    # Nodos (más grandes y bonitos)
    nx.draw_networkx_nodes(
        G_vis, pos,
        node_color="#3498db",
        node_size=1400,
        linewidths=3,
        edgecolors="white"
    )

    # Etiquetas de nodos
    nx.draw_networkx_labels(
        G_vis, pos,
        font_size=14,
        font_color="white",
        font_weight="bold"
    )

    # Aristas originales (con flujo real + capacidad original)
    nx.draw_networkx_edges(
        G_original, pos,          # usamos G_original para que dibuje TODAS las aristas originales
        edgelist=G_original.edges(),
        width=edge_widths,
        edge_color=edge_colors,
        arrows=True,
        arrowsize=20,
        arrowstyle="->",
        connectionstyle="arc3,rad=0.1"  # curvatura ligera para evitar solapamiento
    )

    # Etiquetas de flujo/capacidad (las más importantes)
    nx.draw_networkx_edge_labels(
        G_original, pos,
        edge_labels=edge_labels,
        font_size=11,
        font_color="black",
        font_weight="bold",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7),
        verticalalignment="bottom"
    )

    # Aristas residuales con capacidad > 0 (en verde brillante y dashed)
    if residual_edges:
        nx.draw_networkx_edges(
            G_vis, pos,
            edgelist=residual_edges,
            style="dashed",
            width=3,
            edge_color="#2ecc71",      # verde esmeralda
            alpha=0.8,
            arrows=True,
            arrowsize=18,
            connectionstyle="arc3,rad=0.15"
        )

    # Leyenda clara dentro de la imagen
    leyenda = (
        "Leyenda:\n"
        "■ Amarillo = Flujo / Capacidad original\n"
        "— Rojo = Arista saturada (100% usada)\n"
        "— Naranja = Parcialmente usada\n"
        "— Gris = Sin flujo\n"
        "··· Verde = Capacidad residual disponible (camino aumentante posible)"
    )
    plt.text(
        0.02, 0.98, leyenda,
        transform=plt.gca().transAxes,
        fontsize=11,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.9)
    )

    plt.title(
        f"GRAFO FINAL – Flujo máximo = {flujo_total}\n"
        f"(Rojo = saturada | Naranja = parcial | Verde punteado = capacidad residual)",
        fontsize=16, fontweight="bold", pad=20
    )

    plt.axis("off")
    plt.tight_layout()
    plt.savefig(ruta, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()

    return ruta