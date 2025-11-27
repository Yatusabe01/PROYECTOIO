import streamlit as st
from utils.session import init_session

from ui.nodos import gestionar_nodos
from ui.arista import gestionar_aristas
from ui.grafo_visu import mostrar_grafo
from ui.flujo import calcular_flujo_maximo


def main():
    init_session()

    st.title("Proyecto – Flujo Máximo y Editor de Grafos")

    tab1, tab2= st.tabs(["Editor", "Grafo", "Flujo Máximo"])

    with tab1:
        st.subheader("Visualización del Grafo")
        mostrar_grafo()
    with tab2:
        calcular_flujo_maximo()

