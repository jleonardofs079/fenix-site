import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit.components.v1 import html
import io

# Estilos adaptáveis para modo claro e escuro
st.markdown(
    """
    <style>
        body, .stApp {
            background-color: #f0f0f0;
            color: #1a237e;
        }
        h1, h2, h3, h4 {
            color: #1a237e;
            font-size: 1.2em;
        }
        .stSelectbox label, .stDataFrameContainer {
            color: #3e2723;
        }
        .stButton>button {
            background-color: #7b1fa2;
            color: white;
        }
        .stButton>button:hover {
            background-color: #512da8;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            table-layout: auto;
            word-wrap: break-word;
            white-space: nowrap;
        }
        th, td {
            padding: 8px;
            text-align: left;
            border: 1px solid #ccc;
        }
        @media (prefers-color-scheme: dark) {
            body, .stApp {
                background-color: #121212 !important;
                color: #e0e0e0 !important;
            }
            h1, h2, h3, h4 {
                color: #f0f0f0;
            }
            .stSelectbox label, .stDataFrameContainer {
                color: #f0f0f0;
            }
            .stButton>button {
                background-color: #bb86fc;
                color: black;
            }
            .stButton>button:hover {
                background-color: #985eff;
            }
            th, td {
                border: 1px solid #555;
            }
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Exibir cabeçalho com logotipos e título
col1, col2, col3 = st.columns([1, 6, 1])
with col1:
    st.image("habitnet.png", width=60)
with col2:
    st.markdown("<div style='text-align: center; font-size: 1.1em; font-weight: bold;'>🔎 Habitnet - Equipe Fênix - Pesquisa de Empreendimentos</div>", unsafe_allow_html=True)
with col3:
    st.image("fenix.png", width=60)
