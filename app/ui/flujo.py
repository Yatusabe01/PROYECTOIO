# ui/flujo.py
import streamlit as st
import networkx as nx
from ui.algoritmo import Grafo
from utils.step import guardar_imagen_final
from ui.grafo_visu import generar_layout_por_fuente_sumidero, mostrar_grafo


def calcular_flujo_maximo():
    st.header("Calcular Flujo Máximo")

    if len(st.session_state.nodos) <= 1:
        st.write("Necesitas al menos 2 nodos.")
        return

    fuente = st.selectbox("Fuente:", sorted(st.session_state.nodos))
    sumidero = st.selectbox("Sumidero:", sorted(st.session_state.nodos))

    if st.button("Calcular Flujo Máximo"):
        if fuente == sumidero:
            st.error("La fuente y el sumidero deben ser diferentes.")
            return

        # -------------------------------------------------
        # 1. Grafo original para visualización (NetworkX)
        # -------------------------------------------------
        G_nx = nx.DiGraph()
        for (u, v, c) in st.session_state.aristas:
            G_nx.add_edge(u, v, capacidad=c)

        # Layout fijo (fuente izquierda, sumidero derecha)
        layout_fijo = generar_layout_por_fuente_sumidero(G_nx, fuente, sumidero)
        st.session_state["layout_fs"] = layout_fijo

        # -------------------------------------------------
        # 2. Grafo para el algoritmo (clase Grafo personalizada)
        # -------------------------------------------------
        grafo_algo = Grafo()
        for (u, v, c) in st.session_state.aristas:
            grafo_algo.agregar_arista(u, v, c)

        # -------------------------------------------------
        # 3. Ejecutar Ford-Fulkerson
        # -------------------------------------------------
        flujo = grafo_algo.ford_fulkerson(fuente, sumidero, registrar_paso=None)

        # -------------------------------------------------
        # 4. NO intentar reconstruir un camino final
        #     → cuando el flujo máximo se alcanza NO existe camino aumentante
        # -------------------------------------------------
        camino_final = None  # o [] si tu función lo prefiere

        # -------------------------------------------------
        # 5. Generar imagen final (red residual + flujo total)
        # -------------------------------------------------
        try:
            ruta_img_final = guardar_imagen_final(
                G_original=G_nx,
                grafo_residual=grafo_algo.grafo,      # red residual real
                camino_final=camino_final,             # puede ser None
                layout_fijo=layout_fijo,
                flujo_total=flujo
            )
        except Exception as e:
            st.error(f"Error al generar la imagen final: {e}")
            ruta_img_final = None

        # -------------------------------------------------
        # 6. Mostrar resultados
        # -------------------------------------------------
        st.subheader("Grafo Original")
        mostrar_grafo(fuente, sumidero)

        st.success(f"**Flujo máximo encontrado: {flujo}**")

        st.subheader("Red Residual Final")
        if ruta_img_final:
            st.image(ruta_img_final)
        else:
            st.warning("No se pudo generar la imagen de la red residual.")
