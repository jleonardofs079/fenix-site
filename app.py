import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit.components.v1 import html

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
            color: #1a237e;
        }
        .stSelectbox label, .stDataFrameContainer {
            color: #3e2723;
        }
        .css-1cpxqw2, .css-1aumxhk, .css-1v3fvcr {
            color: #7b1fa2;
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

# Adicionar coluna de link para Google Maps
df["LINK GOOGLE MAPS"] = df.apply(
    lambda row: f"https://www.google.com/maps/search/?api=1&query={row['LATITUDE']},{row['LONGITUDE']}" if pd.notna(row.get("LATITUDE")) and pd.notna(row.get("LONGITUDE")) else "",
    axis=1
)

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

# Exibir resultados com link clicável
df_exibicao = df_filtrado.copy()
df_exibicao["LINK GOOGLE MAPS"] = df_exibicao["LINK GOOGLE MAPS"].apply(lambda url: f'<a href="{url}" target="_blank">Abrir no Mapa</a>' if url else "")

st.write(f"### Resultados: {len(df_filtrado)} empreendimento(s) encontrado(s)")
st.write(df_exibicao.to_html(escape=False, index=False), unsafe_allow_html=True)

# Criar mapa com marcadores
if not df_filtrado.empty:
    m = folium.Map(location=[-3.75, -38.5], zoom_start=11)

    for _, row in df_filtrado.iterrows():
        try:
            lat = float(row["LATITUDE"])
            lon = float(row["LONGITUDE"])
            popup_text = f"{row['EMPREENDIMENTO']}<br>{row['ENDEREÇO']} - {row['CIDADE']}"
            folium.Marker(location=[lat, lon], popup=popup_text).add_to(m)
        except:
            st.warning(f"Erro ao processar coordenadas para: {row['EMPREENDIMENTO']}")

    st.write("### Mapa dos Empreendimentos Filtrados")
    st_folium(m, width=None, height=500)
else:
    st.info("Nenhum empreendimento com coordenadas disponíveis para exibir no mapa.")
