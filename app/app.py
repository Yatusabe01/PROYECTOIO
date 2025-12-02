import streamlit as st
from utils.session import init_session
from ui.nodos import gestionar_nodos
from ui.arista import gestionar_aristas
from ui.grafo_visu import mostrar_grafo
from ui.flujo import calcular_flujo_maximo

# Configuración
st.set_page_config(
    page_title="Flujo Máximo • Editor de Grafos",
    page_icon="logo/logo.png", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS MEJORADO - Botones perfectos y sin "Press Enter"
st.markdown("""
<style>
    /* Quitar botón Deploy y menús molestos */
    .stAppDeployButton {display: none !important;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Fondo blanco puro */
    .stApp {background-color: #ffffff;}

    /* Contenedor del grafo con borde negro elegante */
    .graph-container {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border: 3px solid #2c3e50;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        margin: 25px 0;
    }

    /* BOTONES COMPACTOS Y ELEGANTES */
    div.stButton > button {
        background-color: white !important;
        color: #212529 !important;
        border: 2px solid #2c3e50 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 8px 16px !important;
        height: 38px !important;
        font-size: 14px !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06) !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }
    
    div.stButton > button:hover {
        background-color: #f8f9fa !important;
        border-color: #1a1a1a !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
    }
    
    div.stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* INPUTS DE TEXTO COMPACTOS */
    .stTextInput > div > div > input {
        border: 2px solid #2c3e50 !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        background-color: white !important;
        height: 38px !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #1a1a1a !important;
        box-shadow: 0 0 0 3px rgba(44, 62, 80, 0.1) !important;
    }

    /* NUMBER INPUT COMPACTO */
    .stNumberInput > div > div > input {
        border: 2px solid #2c3e50 !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        background-color: white !important;
        height: 38px !important;
    }
    
    /* QUITAR "Press Enter to apply" */
    .stNumberInput [data-testid="InputInstructions"] {
        display: none !important;
    }

    /* SELECTBOX COMPACTO */
    .stSelectbox > div > div > div {
        border: 2px solid #2c3e50 !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        background-color: white !important;
        height: 38px !important;
    }

    /* Labels compactas */
    .stTextInput label, .stSelectbox label, .stNumberInput label {
        font-weight: 600 !important;
        color: #2c3e50 !important;
        font-size: 13px !important;
        margin-bottom: 6px !important;
    }

    /* Títulos bonitos */
    h1, h2, h3 {
        color: #2c3e50 !important;
        font-weight: 700 !important;
    }

    /* Sidebar limpia */
    section[data-testid="stSidebar"] {
        background-color: #f8f9fc;
        border-right: 2px solid #2c3e50;
    }
    
    /* Tabs con estilo compacto */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 42px;
        padding: 8px 20px;
        background-color: white;
        border: 2px solid #2c3e50;
        border-radius: 8px 8px 0 0;
        font-weight: 600;
        font-size: 14px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #2c3e50 !important;
        color: white !important;
    }
    
    /* Sidebar más compacta */
    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }
    
    /* Espaciado entre elementos del sidebar */
    section[data-testid="stSidebar"] .stButton {
        margin-bottom: 1rem;
    }
    
    /* Títulos de secciones en sidebar */
    section[data-testid="stSidebar"] h3 {
        font-size: 16px !important;
        margin-bottom: 1rem !important;
    }
</style>
""", unsafe_allow_html=True)

# App
init_session()

st.title("""
         SNOWFLOW • CALCULADORA DE FLUJO MAXIMO
         """)

with st.sidebar:
    st.markdown("### Controles")
    if st.button("Limpiar todo", use_container_width=True):
        st.session_state.clear()
        init_session()
        st.success("¡Todo limpiado!")
        st.rerun()

tab1, tab2 = st.tabs(["Grafo", "Flujo Máximo"])

with tab1:
    st.subheader("Editor y Visualización del Grafo")
    gestionar_nodos()
    gestionar_aristas()
    mostrar_grafo()

with tab2:
    calcular_flujo_maximo()

st.markdown("<p style='font-size:14px; font-weight:600;'>Creado por:", unsafe_allow_html=True)
st.markdown("<p style='font-size:14px; font-weight:600;'>Fredy Alexander de la Cruz Gomez</p>", unsafe_allow_html=True)
st.markdown("<p style='font-size:14px; font-weight:600;'>Manuel de Jesus Flores de la Cruz</p>", unsafe_allow_html=True)
st.markdown("<p style='font-size:14px; font-weight:600;'>Sebastian Emiliano Anzueto Escobar</p>", unsafe_allow_html=True)

st.markdown("<p style='font-size:14px; font-weight:600; margin-top:12px;'>Colaboraciones:</p>", unsafe_allow_html=True)
st.markdown("<p style='font-size:14px;'>Lester Randolf Ford, Jr. y Delbert Ray Fulkerson</p>", unsafe_allow_html=True)
