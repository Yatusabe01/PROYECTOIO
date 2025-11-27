import streamlit as st 
import networkx as nx
import matplotlib.pyplot as plt


def generar_layout_por_fuente_sumidero(G, fuente, sumidero):
    nodos = list(G.nodes())

    niveles = {n: 1 for n in nodos}  # centro

    if fuente in nodos:
        niveles[fuente] = 0  # izquierda
    if sumidero in nodos:
        niveles[sumidero] = 2  # derecha

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

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_facecolor("#f8fbff")

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="#4A90E2",
        node_size=1600,
        font_size=12,
        font_color="white",
        edge_color="gray",
        width=2,
        ax=ax
    )

    labels = nx.get_edge_attributes(G, "capacidad")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=10)

    st.pyplot(fig)


def mostrar_grafo(fuente=None, sumidero=None):

    G = nx.DiGraph()

    for n in st.session_state.nodos:
        G.add_node(n)

    for (u, v, c) in st.session_state.aristas:
        G.add_edge(u, v, capacidad=c)

    dibujar_grafo(G, fuente, sumidero)
