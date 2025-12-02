import streamlit as st

MAX_NODOS = 20

def gestionar_nodos():

    # Inicialización para evitar errores
    if "nodos" not in st.session_state:
        st.session_state.nodos = set()

    if "aristas" not in st.session_state:
        st.session_state.aristas = []

    st.sidebar.header("Nodos")
    nuevo_nodo = st.sidebar.text_input("Nombre del nodo:")

    if st.sidebar.button("Agregar Nodo"):

        if len(st.session_state.nodos) >= MAX_NODOS:
            st.sidebar.error(f"Límite máximo de nodos alcanzado ({MAX_NODOS}).")

        elif nuevo_nodo.strip() == "":
            st.sidebar.error("Escribe un nombre válido.")

        elif nuevo_nodo in st.session_state.nodos:
            st.sidebar.warning("Ese nodo ya existe.")

        else:
            st.session_state.nodos.add(nuevo_nodo)
            st.sidebar.success(f"Nodo '{nuevo_nodo}' agregado.")

    if not st.session_state.nodos:
        st.sidebar.info("No hay nodos todavía.")
        return

    borrar_nodo = st.sidebar.selectbox(
        "Borrar nodo:",
        ["-- Selecciona un nodo --"] + sorted(st.session_state.nodos)
    )

    if st.sidebar.button("Eliminar Nodo"):

        if borrar_nodo.startswith("--"):
            st.sidebar.error("Selecciona un nodo válido.")

        else:
            st.session_state.nodos.remove(borrar_nodo)

            st.session_state.aristas = [
                (u, v, c)
                for (u, v, c) in st.session_state.aristas
                if u != borrar_nodo and v != borrar_nodo
            ]

            st.sidebar.success(f"Nodo '{borrar_nodo}' eliminado.")
