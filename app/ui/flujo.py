# app/ui/flujo.py
# Con bordes elegantes para las imágenes

import streamlit as st
import networkx as nx
from ui.algoritmo import Grafo
from utils.step import guardar_imagen_final
from ui.grafo_visu import mostrar_grafo


def calcular_flujo_maximo():
    st.header("Calcular Flujo Máximo")

    if len(st.session_state.nodos) < 2:
        st.info("Necesitas al menos 2 nodos para calcular flujo máximo.")
        return

    col1, col2 = st.columns(2)
    with col1:
        fuente = st.selectbox("Fuente:", sorted(st.session_state.nodos), key="fuente_flujo")
    with col2:
        sumidero = st.selectbox("Sumidero:", sorted(st.session_state.nodos), key="sumidero_flujo")

    if st.button("Calcular Flujo Máximo", type="primary", use_container_width=True):

        if fuente == sumidero:
            st.error("La fuente y el sumidero deben ser diferentes.")
            return

        # Grafo con TODOS los nodos
        G_temp = nx.DiGraph()
        G_temp.add_nodes_from(st.session_state.nodos)
        for u, v, c in st.session_state.aristas:
            G_temp.add_edge(u, v, capacity=c)

        # Validación segura
        try:
            if not nx.has_path(G_temp, fuente, sumidero):
                st.error(
                    f"No existe camino dirigido de **{fuente}** → **{sumidero}**.\n\n"
                    "Agrega aristas que conecten la fuente con el sumidero."
                )
                return
        except nx.NodeNotFound:
            st.error("Error interno: nodo no encontrado. Esto no debería pasar.")
            return

        # Algoritmo
        grafo_algo = Grafo()
        for u, v, c in st.session_state.aristas:
            grafo_algo.agregar_arista(u, v, c)

        flujo_maximo = grafo_algo.ford_fulkerson(fuente, sumidero)

        # Imagen final
        try:
            ruta_img = guardar_imagen_final(
                G_original=G_temp,
                grafo_residual=grafo_algo.grafo,
                camino_final=None,
                layout_fijo=st.session_state.get("layout_fs", {}),
                flujo_total=flujo_maximo
            )
        except Exception as e:
            st.warning(f"No se pudo generar imagen final: {e}")
            ruta_img = None

        st.success(f"**Flujo máximo encontrado: {flujo_maximo}**")

        st.subheader("Grafo Original")
        mostrar_grafo(fuente, sumidero)

        st.subheader("Red Residual Final")
        if ruta_img:
            # Contenedor con columna para controlar mejor el layout
            with st.container():
                st.markdown("""
                    <div style='
                        background: #f8f9fa;
                        padding: 20px;
                        border-radius: 12px;
                        border: 3px solid #2c3e50;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                        margin: 20px 0;
                    '>
                """, unsafe_allow_html=True)
                
                st.image(ruta_img, use_container_width=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("No se generó imagen de la red residual.")