import streamlit as st
from utils.session import init_session

from ui.nodos import gestionar_nodos
from ui.arista import gestionar_aristas
from ui.grafo_visu import mostrar_grafo
from ui.flujo import calcular_flujo_maximo


def main():
    init_session()

    st.title("Proyecto – Flujo Máximo y Editor de Grafos")

    tab1, tab2, tab3 = st.tabs(["📝 Editor", "📊 Grafo", "⚡ Flujo Máximo"])

    # ============================
    # TAB 1: Editor
    # ============================
    with tab1:
        st.subheader("Editor de Nodos y Aristas")
        gestionar_nodos()
        gestionar_aristas()

    # ============================
    # TAB 2: Grafo
    # ============================
    with tab2:
        st.subheader("Visualización del Grafo")
        mostrar_grafo()

    # ============================
    # TAB 3: Flujo Máximo
    # ============================
    with tab3:
        calcular_flujo_maximo()


if __name__ == "__main__":
    main()
