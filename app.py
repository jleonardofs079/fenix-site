import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit.components.v1 import html
import io
import os

# Estilos adaptáveis para modo claro e escuro
st.markdown(
    """ ... (conteúdo truncado no exemplo para brevidade) ... """
)

# Verificação do arquivo Excel
excel_path = "MEGATAB_EMPREEND_JUN2025vlight.xlsx"
if not os.path.exists(excel_path):
    st.error(f"Arquivo '{excel_path}' não encontrado. Verifique se ele está no diretório do app.")
    st.stop()

# Resto do código já incluído no canvas
... (continuação omitida aqui, mas foi salva integralmente)
