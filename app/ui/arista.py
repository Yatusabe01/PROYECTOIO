import streamlit as st

def gestionar_aristas():
    st.sidebar.header("Aristas")

    if st.session_state.nodos:

        u = st.sidebar.selectbox("Desde:", sorted(st.session_state.nodos))
        v = st.sidebar.selectbox("Hasta:", sorted(st.session_state.nodos))
        capacidad = st.sidebar.number_input(
            "Capacidad:", min_value=1, max_value=10_000_000, value=10
        )

        if st.sidebar.button("Agregar Arista"):

            if u == v:
                st.sidebar.error("No puedes conectar un nodo consigo mismo.")
                return

            if (u, v, capacidad) in st.session_state.aristas:
                st.sidebar.error("Esa arista ya existe.")
                return

            for (a, b, _) in st.session_state.aristas:
                if a == u and b == v:
                    st.sidebar.error("Ya existe una arista entre esos nodos.")
                    return

            st.session_state.aristas.append((u, v, capacidad))
            st.success(f"Arista {u} → {v} agregada.")


    if st.session_state.aristas:
        st.sidebar.header("Eliminar Arista")

        aristas_unicas = list(dict.fromkeys(st.session_state.aristas))

        lista_aristas = [
            f"{a[0]} → {a[1]} (cap={a[2]})"
            for a in aristas_unicas
        ]

        idx = st.sidebar.selectbox(
            "Aristas:",
            list(range(len(aristas_unicas))),
            format_func=lambda x: lista_aristas[x]
        )

        if st.sidebar.button("Eliminar Arista"):
            eliminada = aristas_unicas[idx]

            # quitar SOLO UNA OCURRENCIA aunque hayan duplicados
            for i, a in enumerate(st.session_state.aristas):
                if a == eliminada:
                    st.session_state.aristas.pop(i)
                    break

            st.success(f"Arista {eliminada[0]} → {eliminada[1]} eliminada.")
