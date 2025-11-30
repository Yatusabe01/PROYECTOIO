# ui/grafo_visu.py → VERSIÓN FINAL DEFINITIVA
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque


def generar_layout_profesional(G, fuente, sumidero):
    pos = {}
    niveles = {}
    queue = deque([fuente])
    niveles[fuente] = 0
    visitados = {fuente}

    while queue:
        actual = queue.popleft()
        for vecino in G.successors(actual):
            if vecino not in visitados:
                visitados.add(vecino)
                niveles[vecino] = niveles[actual] + 1
                queue.append(vecino)

    max_nivel = max(niveles.values(), default=0)
    for nodo in G.nodes():
        if nodo not in niveles:
            niveles[nodo] = max_nivel + 1

    nodos_por_nivel = {}
    for nodo, nivel in niveles.items():
        nodos_por_nivel.setdefault(nivel, []).append(nodo)

    for nivel, nodos in nodos_por_nivel.items():
        nodos.sort()
        y_step = 1.0 / (len(nodos) + 1)
        for i, nodo in enumerate(nodos):
            x = nivel * 3.0
            y = (i + 1) * y_step * 2 - 1
            pos[nodo] = (x, y)

    if fuente in pos:
        pos[fuente] = (0, 0)
    if sumidero in pos:
        pos[sumidero] = (max_nivel * 3.0, 0)

    return pos


def generar_layout_por_fuente_sumidero(G, fuente, sumidero):
    return generar_layout_profesional(G, fuente, sumidero)


def mostrar_grafo(fuente=None, sumidero=None):
    if not st.session_state.get("nodos"):
        st.info("Agrega al menos un nodo para visualizar el grafo.")
        return

    G = nx.MultiDiGraph()
    for n in st.session_state.nodos:
        G.add_node(n)
    for i, (u, v, c) in enumerate(st.session_state.aristas):
        G.add_edge(u, v, key=i, capacidad=c)

    if fuente and sumidero and fuente in G.nodes and sumidero in G.nodes:
        pos = generar_layout_profesional(G, fuente, sumidero)
        st.session_state["layout_fs"] = pos
    else:
        pos = nx.spring_layout(G, seed=42, k=4, iterations=100)

    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_facecolor('#f8f9fa')

    # Nodos
    color_nodos = ['#e74c3c' if n == fuente else '#9b59b6' if n == sumidero else '#3498db' for n in G.nodes]
    nx.draw_networkx_nodes(G, pos, node_size=3000, node_color=color_nodos,
                        edgecolors='white', linewidths=5, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=18, font_weight='bold', font_color='white', ax=ax)

    # Aristas: 100% rectas
    nx.draw_networkx_edges(G, pos,
                        width=6, edge_color='#27ae60',
                        arrows=True, arrowsize=45, arrowstyle='->',       # ← ESTE ES EL TRUCO REAL (y sí existe)
                        connectionstyle='arc3,rad=0', alpha=0.95, ax=ax)

    # Etiquetas: pegadas al origen
    edge_labels = {(u, v, k): str(d['capacidad']) for u, v, k, d in G.edges(keys=True, data=True)}
    nx.draw_networkx_edge_labels(G, pos,
                                edge_labels=edge_labels,
                                label_pos=0.25,
                                font_size=16, font_weight='bold',
                                font_color='#27ae60',
                                bbox=dict(facecolor='white', alpha=0.98, edgecolor='none', pad=9),
                                ax=ax)

    titulo = "Grafo Original"
    if fuente and sumidero:
        titulo += f" → Fuente: {fuente} | Sumidero: {sumidero}"
    ax.set_title(titulo, fontsize=24, fontweight='bold', pad=30, color='#2c3e50')
    ax.axis('off')
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)