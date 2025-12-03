import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import io
from PIL import Image


def generar_layout_niveles(G, nodo_inicial=None):
    if not G.nodes:
        return {}, None

    if nodo_inicial is None or nodo_inicial not in G.nodes:
        nodo_inicial = min(G.nodes, key=str)

    pos = {}
    niveles = {}
    queue = deque([nodo_inicial])
    niveles[nodo_inicial] = 0
    visitados = {nodo_inicial}

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

    for nivel, lista in nodos_por_nivel.items():
        lista.sort(key=str)
        y_step = 1.0 / (len(lista) + 1)
        for i, nodo in enumerate(lista):
            x = nivel * 5.0
            y = (i + 1) * y_step * 2 - 1
            pos[nodo] = (x, y)

    return pos, nodo_inicial


def mostrar_grafo(fuente=None, sumidero=None):
    if not st.session_state.get("nodos"):
        st.info("Agrega al menos un nodo para visualizar el grafo.")
        return

    G = nx.DiGraph()
    G.add_nodes_from(st.session_state.nodos)
    for u, v, c in st.session_state.aristas:
        G.add_edge(u, v, capacity=c)

    if fuente and sumidero and fuente in G.nodes and sumidero in G.nodes:
        pos, _ = generar_layout_niveles(G, nodo_inicial=fuente)
        max_x = max(x for x, y in pos.values())
        pos[sumidero] = (max_x + 5.0, 0)
        titulo = f"Grafo del Flujo → Fuente: {fuente} | Sumidero: {sumidero}"
        caption = f"Ordenado desde la fuente **{fuente}**"
        color_map = ['#e74c3c' if n == fuente else '#9b59b6' if n == sumidero else '#3498db' for n in G.nodes]
    else:
        pos, nodo_raiz = generar_layout_niveles(G)
        titulo = "Editor y Visualización del Grafo"
        caption = f"Layout automático ordenado desde el nodo **{nodo_raiz}**"
        color_map = '#3498db'

    st.session_state.layout_fs = pos

    # Crear figura con fondo gris
    fig, ax = plt.subplots(figsize=(18, 10))
    fig.patch.set_facecolor('#f8f9fa')
    ax.set_facecolor('#f8f9fa')

    nx.draw_networkx_nodes(G, pos,
                           node_size=3800,
                           node_color=color_map,
                           edgecolors='white',
                           linewidths=6,
                           ax=ax)

    nx.draw_networkx_labels(G, pos,
                            font_size=22,
                            font_color='white',
                            font_weight='bold',
                            ax=ax)

    nx.draw_networkx_edges(G, pos,
                           width=8,
                           edge_color='#27ae60',
                           arrows=True,
                           arrowsize=55,
                           arrowstyle='->',
                           alpha=0.95,
                           min_source_margin=35,  # ← Margen desde el nodo origen
                           min_target_margin=35,  # ← Margen hasta el nodo destino
                           ax=ax)

    # Etiquetas MUY cerca del nodo de origen (label_pos=0.15)
    edge_labels = {(u, v): f"{d['capacity']}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos,
                                 edge_labels=edge_labels,
                                 label_pos=0.15,  # ← MUY CERCA DEL ORIGEN
                                 font_size=19,
                                 font_weight='bold',
                                 font_color='white',
                                 bbox=dict(facecolor='#27ae60',
                                           edgecolor='none',
                                           boxstyle='round,pad=0.7',
                                           alpha=0.9))

    ax.set_title(titulo, fontsize=30, fontweight='bold', color='#2c3e50', pad=40)
    ax.axis('off')
    plt.tight_layout()

    # Guardar en buffer y convertir a imagen
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', 
                facecolor='#f8f9fa', edgecolor='none')
    buf.seek(0)
    img = Image.open(buf)
    
    # Agregar borde a la imagen directamente con CSS global
    st.markdown(f"""
        <style>
        div[data-testid="stImage"] {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 12px;
            border: 3px solid #2c3e50;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            margin: 20px 0;
        }}
        </style>
    """, unsafe_allow_html=True)
    
    st.image(img, use_container_width=True)
    
    plt.close(fig)
    buf.close()

    st.caption(caption)