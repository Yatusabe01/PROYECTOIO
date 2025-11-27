import streamlit as st

def init_session():
    if "nodos" not in st.session_state:
        st.session_state.nodos = set()
    if "aristas" not in st.session_state:
        st.session_state.aristas = []
