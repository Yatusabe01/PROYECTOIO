# ui/grafo_visu.py → VERSIÓN FINAL DEFINITIVA (flechas rectas + separadas)

import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

def generar_layout_por_fuente_sumidero(G, fuente, sumidero):
    nodos = list(G.nodes())
    niveles = {n: 1 for n in nodos}
    if fuente in nodos: niveles[fuente] = 0
    if sumidero in nodos: niveles[sumidero] = 2

    pos = {}
    columnas = {0: [], 1: [], 2: []}
    for nodo, col in niveles.items():
        columnas[col].append(nodo)

    for col, lista in columnas.items():
        lista.sort()
        espaciado = 1 / (len(lista) + 1)
        for idx, nodo in enumerate(lista):
            x = 0.1 + col * 0.4
            y = 1 - (idx + 1) * espaciado
            pos[nodo] = (x, y)
    return pos


def dibujar_grafo(G, fuente=None, sumidero=None):
    if G.number_of_nodes() == 0:
        st.info("Agrega nodos para visualizar el grafo.")
        return

    if fuente and sumidero:
        pos = generar_layout_por_fuente_sumidero(G, fuente, sumidero)
        st.session_state["layout_fs"] = pos
    else:
        pos = nx.spring_layout(G, seed=42)

    fig, ax = plt.subplots(figsize=(12, 9))
    ax.set_facecolor("#f8fbff")

    # === DIBUJAR ARISTAS: una arriba, otra abajo si es bidireccional ===
    for u, v, data in G.edges(data=True):
        capacidad = data.get("capacidad", "")

        # Calcular vector perpendicular para separar
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        dx = x2 - x1
        dy = y2 - y1
        length = (dx**2 + dy**2)**0.5 or 1
        perp_x = -dy / length
        perp_y = dx / length

        # --- Nueva separación estable basada en orientación ---
        offset = 0.0
        if G.has_edge(v, u):
            signo = 1 if (dx * perp_x + dy * perp_y) < 0 else -1
            offset = signo * 0.06

        # Posiciones desplazadas
        x1_o = x1 + offset * perp_x
        y1_o = y1 + offset * perp_y
        x2_o = x2 + offset * perp_x
        y2_o = y2 + offset * perp_y

        # Flecha recta desplazada
        ax.annotate("",
                    xy=(x2_o, y2_o),
                    xytext=(x1_o, y1_o),
                    arrowprops=dict(
                        arrowstyle='-|>',
                        color='#2ecc71',
                        lw=4.5,
                        shrinkA=30,
                        shrinkB=30,
                    ),
                    zorder=1)

        # Etiqueta ajustada
        xc = (x1_o + x2_o) / 2
        yc = (y1_o + y2_o) / 2
        if G.has_edge(v, u):
            yc += 0.04 * (1 if offset > 0 else -1)

        ax.text(xc, yc, str(capacidad),
                fontsize=13, fontweight='bold', color='#1a6600',
                bbox=dict(facecolor='white', alpha=0.97, edgecolor='none', pad=5),
                ha='center', va='center', zorder=10)
    # === NODOS ===
    node_colors = ['#e74c3c' if n in [fuente, sumidero] else '#4A90E2' for n in G.nodes()]
    nx.draw_networkx_nodes(G, pos,
                           node_color=node_colors,
                           node_size=2000,
                           linewidths=3,
                           edgecolors='black',
                           ax=ax)

    nx.draw_networkx_labels(G, pos,
                            font_size=14,
                            font_weight='bold',
                            font_color='white',
                            ax=ax)

    ax.axis('off')
    plt.tight_layout()
    st.pyplot(fig)


def mostrar_grafo(fuente=None, sumidero=None):
    G = nx.DiGraph()
    for n in st.session_state.nodos:
        G.add_node(n)
    for u, v, c in st.session_state.aristas:
        G.add_edge(u, v, capacidad=c)
    dibujar_grafo(G, fuente, sumidero)