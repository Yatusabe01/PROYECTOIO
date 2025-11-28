# ui/matriz.py
import streamlit as st
import re
import networkx as nx

def cargar_desde_matriz():
    st.header("Pegar Matriz → Resultado Final Inmediato")

    matriz_texto = st.text_area(
        "Pega tu matriz aquí (Ctrl+V)",
        height=200,
        placeholder="0 10 0 20\n0 0 5 10\n0 0 0 5\n0 0 0 0",
        label_visibility="collapsed"
    )

    if st.button("CARGAR Y CALCULAR FLUJO MÁXIMO", type="primary", use_container_width=True):
        if not matriz_texto.strip():
            st.warning("Pega una matriz primero.")
            return

        try:
            # --- 1. Parsear matriz ---
            numeros = [int(x) for x in re.findall(r'\d+', matriz_texto)]
            n = int(len(numeros) ** 0.5)
            if n * n != len(numeros) or n < 2 or n > 20:
                st.error("Error: debe ser matriz cuadrada de 2×2 a 20×20")
                return

            nodos = [chr(65 + i) for i in range(n)]
            fuente = nodos[0]
            sumidero = nodos[-1]

            # --- 2. Limpiar sesión ---
            st.session_state.nodos = set(nodos)
            st.session_state.aristas = []

            # --- 3. Construir G_original con TODOS los nodos ---
            G_original = nx.DiGraph()
            for nodo in nodos:
                G_original.add_node(nodo)               # ← imprescindible

            idx = 0
            for i in range(n):
                for j in range(n):
                    cap = numeros[idx]
                    if cap > 0:
                        u, v = nodos[i], nodos[j]
                        st.session_state.aristas.append((u, v, cap))
                        G_original.add_edge(u, v, capacidad=cap)
                    idx += 1

            # --- 4. Ejecutar Ford-Fulkerson ---
            from ui.algoritmo import Grafo
            grafo_algo = Grafo()
            for u, v, c in st.session_state.aristas:
                grafo_algo.agregar_arista(u, v, c)

            flujo_max = grafo_algo.ford_fulkerson(fuente, sumidero)

            # --- 5. Layout perfecto y guardarlo en session_state ---
            from ui.grafo_visu import generar_layout_por_fuente_sumidero
            layout = generar_layout_por_fuente_sumidero(G_original, fuente, sumidero)
            st.session_state["layout_fs"] = layout          # ← clave para que no se pierda

            # --- 6. Generar imagen final ---
            from utils.step import guardar_imagen_final
            ruta_img = guardar_imagen_final(
                G_original=G_original,
                grafo_residual=grafo_algo.grafo,
                camino_final=None,
                layout_fijo=layout,
                flujo_total=flujo_max
            )

            # --- 7. MOSTRAR RESULTADO PERFECTO ---
            st.success(f"**FLUJO MÁXIMO = {flujo_max}**")
            
            # ← SOLUCIÓN AL WARNING + gráfica perfecta
            st.image(ruta_img, use_container_width=True)
            
            st.caption(f"Fuente: **{fuente}** → Sumidero: **{sumidero}**")

        except Exception as e:
            st.error(f"Error inesperado: {e}")