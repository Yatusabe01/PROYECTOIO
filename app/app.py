import streamlit as st
from utils.session import init_session
from ui.nodos import gestionar_nodos
from ui.arista import gestionar_aristas
from ui.grafo_visu import mostrar_grafo
from ui.flujo import calcular_flujo_maximo
from ui.matriz import cargar_desde_matriz  # ← ya lo tienes

def limpiar_todo():
    """Función central para resetear TODO el estado"""
    st.session_state.nodos = set()
    st.session_state.aristas = []
    st.session_state.layout_fs = None
    # Si usas más variables en session_state, límpialas aquí también
    st.success("¡Todo limpiado! Listo para un grafo nuevo.")
    st.rerun()

def main():
    init_session()

    st.title("Proyecto – Flujo Máximo y Editor de Grafos")

    with st.sidebar:
        st.markdown("### Controles")
        
        if st.button("Limpiar todo", use_container_width=True):
            st.session_state.nodos = set()
            st.session_state.aristas = []
            st.session_state.layout_fs = None
            st.rerun()
            
    # Pestañas normales
    tab1, tab2, tab3 = st.tabs(["Grafo", "Flujo Máximo", "Cargar Matriz"])

    with tab1:
        st.subheader("Editor y Visualización del Grafo")
        gestionar_nodos()
        gestionar_aristas()
        mostrar_grafo()

    with tab2:
        calcular_flujo_maximo()

    with tab3:
        cargar_desde_matriz()
        
main()