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

        # Construir grafo para visualizar
        G_nx = nx.DiGraph()
        for (u, v, c) in st.session_state.aristas:
            G_nx.add_edge(u, v, capacidad=c)

        # Layout fijo
        layout_fijo = generar_layout_por_fuente_sumidero(G_nx, fuente, sumidero)
        st.session_state["layout_fs"] = layout_fijo

        # Construir grafo para el algoritmo
        grafo_algo = Grafo()
        for (u, v, c) in st.session_state.aristas:
            grafo_algo.agregar_arista(u, v, c)

        # Ejecutar algoritmo sin registrar pasos
        flujo = grafo_algo.ford_fulkerson(fuente, sumidero, registrar_paso=None)

        # 📌 Recuperar camino final usado (desde residual)
        camino_final = []
        actual = sumidero
        padre = {}

        # reconstruimos camino desde las capacidades residuales
        while actual != fuente:
            encontrado = False
            for u in grafo_algo.grafo:
                if actual in grafo_algo.grafo[u] and grafo_algo.grafo[u][actual] > 0:
                    padre[actual] = u
                    actual = u
                    encontrado = True
                    break

            if not encontrado:
                break

        if fuente in padre.values():
            nodo = sumidero
            camino_final.append(nodo)
            while nodo != fuente:
                nodo = padre[nodo]
                camino_final.append(nodo)
            camino_final.reverse()

        # Imagen final usando la red residual + camino final
        ruta_img_final = guardar_imagen_final(
            G_original=G_nx,
            grafo_residual=grafo_algo.grafo,  # <<--- Residual real
            camino_final=camino_final,
            layout_fijo=layout_fijo,
            flujo_total=flujo
        )

        st.subheader("Grafo Original")
        mostrar_grafo(fuente, sumidero)

        st.success(f"Flujo máximo encontrado: {flujo}")

        st.subheader("Resultado Final")
        st.image(ruta_img_final)
