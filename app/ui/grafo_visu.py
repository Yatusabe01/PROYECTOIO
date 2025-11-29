# ui/grafo_visu.py → VERSIÓN FINAL PROFESIONAL (como en los libros)
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

def generar_layout_profesional(G, fuente, sumidero):
    """Layout perfecto: niveles automáticos por distancia desde la fuente"""
    pos = {}
    
    # Calcular niveles con BFS desde la fuente
    niveles = {}
    from collections import deque
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
    
    # Asignar coordenadas: x por nivel, y distribuido uniformemente
    max_nivel = max(niveles.values()) if niveles else 0
    nodos_por_nivel = {}
    for nodo, nivel in niveles.items():
        nodos_por_nivel.setdefault(nivel, []).append(nodo)
    
    # Añadir nodos no alcanzables (raro, pero por seguridad)
    for nodo in G.nodes():
        if nodo not in niveles:
            niveles[nodo] = max_nivel + 1
            nodos_por_nivel.setdefault(niveles[nodo], []).append(nodo)
    
    # Posicionar
    for nivel, nodos in nodos_por_nivel.items():
        nodos.sort()  # orden alfabético para consistencia
        y_step = 1.0 / (len(nodos) + 1)
        for i, nodo in enumerate(nodos):
            x = nivel / max(1, max_nivel) * 10  # espaciado horizontal generoso
            y = (i + 1) * y_step * 2 - 1  # centrado verticalmente
            pos[nodo] = (x, y)
    
    # Asegurar que fuente y sumidero estén bien alineados
    if fuente in pos:
        pos[fuente] = (0, 0)
    if sumidero in pos:
        pos[sumidero] = (10, 0)
    
    return pos

# ← MANTENEMOS ESTA PARA QUE NO HAYA ERRORES DE IMPORT
def generar_layout_por_fuente_sumidero(G, fuente, sumidero):
    return generar_layout_profesional(G, fuente, sumidero)

def mostrar_grafo(fuente=None, sumidero=None):
    if not st.session_state.get("nodos"):
        st.info("Agrega nodos para ver el grafo")
        return

    G = nx.DiGraph()
    for n in st.session_state.nodos:
        G.add_node(n)
    for u, v, c in st.session_state.aristas:
        G.add_edge(u, v, capacidad=c)

    # Layout profesional si tenemos fuente y sumidero
    if fuente and sumidero and fuente in G.nodes and sumidero in G.nodes:
        pos = generar_layout_profesional(G, fuente, sumidero)
        st.session_state["layout_fs"] = pos
    else:
        pos = nx.spring_layout(G, seed=42, k=2, iterations=50)

    fig, ax = plt.subplots(figsize=(14, 8))

    # Nodos
    color_nodos = ['#e74c3c' if n in [fuente, sumidero] else '#3498db' for n in G.nodes]
    nx.draw_networkx_nodes(G, pos, node_size=2200, node_color=color_nodos,
                           edgecolors='white', linewidths=4, ax=ax)

    nx.draw_networkx_labels(G, pos, font_size=16, font_weight='bold', font_color='white', ax=ax)

    # Aristas verdes rectas y bonitas
    nx.draw_networkx_edges(G, pos,
                           width=5,
                           edge_color='#27ae60',
                           arrows=True,
                           arrowsize=35,
                           arrowstyle='->',
                           connectionstyle='arc3,rad=0',  # ← RECTA PERFECTA
                           alpha=0.9,
                           ax=ax)

    # Etiquetas de capacidad
    edge_labels = {(u, v): str(c) for u, v, c in st.session_state.aristas}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                                 font_size=14, font_weight='bold', font_color='#27ae60',
                                 bbox=dict(facecolor='white', alpha=0.9, edgecolor='none', pad=6),
                                 ax=ax)

    ax.set_facecolor('#f8f9fa')
    ax.set_title("Grafo Original", fontsize=20, fontweight='bold', pad=30)
    ax.axis('off')
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)