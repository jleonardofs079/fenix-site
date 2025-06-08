import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit.components.v1 import html
import re

# Aplicar estilo personalizado para fundo cinza e destaques bordô e azul marinho
st.markdown(
    """
    <style>
        body {
            background-color: #f0f0f0;
        }
        .stApp {
            background-color: #f0f0f0;
        }
        h1, h2, h3, h4 {
            color: #1a237e; /* azul marinho */
        }
        .stSelectbox label, .stDataFrameContainer {
            color: #3e2723; /* tom escuro para boa leitura */
        }
        .css-1cpxqw2, .css-1aumxhk, .css-1v3fvcr {
            color: #7b1fa2; /* roxo bordô escuro */
        }
        .stButton>button {
            background-color: #7b1fa2;
            color: white;
        }
        .stButton>button:hover {
            background-color: #512da8;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Carregar a base de dados com cache
@st.cache_data
def carregar_dados():
    return pd.read_excel("MEGATAB_EMPREEND_JUN2025vlight.xlsx")

df = carregar_dados()

# Formatar colunas de moeda
valor_cols = ["A PARTIR DE", "PREÇOS ATÉ", "RENDA NECESSÁRIA"]
for col in valor_cols:
    df[col] = df[col].apply(lambda x: f"R$ {x:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))

st.title("🔎 Pesquisa de Empreendimentos - Habitnet")

# Filtros com dropdowns
cidade = st.selectbox("Selecione a Cidade", options=["Todas"] + sorted(df["CIDADE"].dropna().unique().tolist()))
bairro = st.selectbox("Selecione o Bairro", options=["Todos"] + sorted(df["BAIRRO"].dropna().unique().tolist()))
construtora = st.selectbox("Selecione a Construtora", options=["Todas"] + sorted(df["CONSTRUTORA"].dropna().unique().tolist()))
empreendimento = st.selectbox("Selecione o Empreendimento", options=["Todos"] + sorted(df["EMPREENDIMENTO"].dropna().unique().tolist()))

# Aplicar filtros
df_filtrado = df.copy()
if cidade != "Todas":
    df_filtrado = df_filtrado[df_filtrado["CIDADE"] == cidade]
if bairro != "Todos":
    df_filtrado = df_filtrado[df_filtrado["BAIRRO"] == bairro]
if construtora != "Todas":
    df_filtrado = df_filtrado[df_filtrado["CONSTRUTORA"] == construtora]
if empreendimento != "Todos":
    df_filtrado = df_filtrado[df_filtrado["EMPREENDIMENTO"] == empreendimento]

# Exibir resultados
st.write(f"### Resultados: {len(df_filtrado)} empreendimento(s) encontrado(s)")
st.dataframe(df_filtrado, use_container_width=True, height=400)

# Criar mapa com marcadores
if not df_filtrado.empty:
    m = folium.Map(location=[-3.75, -38.5], zoom_start=11)

    for _, row in df_filtrado.iterrows():
        kml_str = row.get("COORDENADA(DEC)", "")
        match = re.search(r"<coordinates>([-\d.]+),([-\d.]+)(?:,0)?</coordinates>", kml_str)
        if match:
            lon, lat = float(match.group(1)), float(match.group(2))
            popup_text = f"{row['EMPREENDIMENTO']}<br>{row['ENDEREÇO']} - {row['CIDADE']}"
            folium.Marker(location=[lat, lon], popup=popup_text).add_to(m)
        else:
            st.warning(f"Coordenada inválida em: {row['EMPREENDIMENTO']}")

    st.write("### Mapa dos Empreendimentos Filtrados")
    st_folium(m, width=None, height=500)
else:
    st.info("Nenhum empreendimento com coordenadas disponíveis para exibir no mapa.")
