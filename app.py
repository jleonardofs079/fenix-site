import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit.components.v1 import html
import io

# Estilos adaptáveis para modo claro e escuro
st.markdown(f"""
<meta name="viewport" content="width=device-width, initial-scale=1">
<div style="display: flex; justify-content: center; align-items: center; gap: 20px; flex-wrap: wrap; margin-top: 10px;">
    <img src="data:image/png;base64,{habitnet_base64}" alt="Habitnet Logo" style="height: 94px;" />
    <img src="data:image/png;base64,{fenix_base64}" alt="Fênix Logo" style="height: 94px;" />
</div>
<h2 style="text-align: center; font-size: 22px; color: #9B1113; margin: 10px 0 20px 0;">
    Habitnet - Equipe Fênix - Pesquisa de Empreendimentos
</h2>
""", unsafe_allow_html=True)

st.markdown("""
<style>
body, .stApp {
background-color: #f0f0f0;
color: #003668;
}
h1, h2, h3, h4 {
color: #003668;
}
.stSelectbox label, .stDataFrameContainer {
color: #003668;
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
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit.components.v1 import html
import io

# Estilos adaptáveis para modo claro e escuro
st.markdown(f"""
<meta name="viewport" content="width=device-width, initial-scale=1">
<div style="display: flex; justify-content: center; align-items: center; gap: 20px; flex-wrap: wrap; margin-top: 10px;">
    <img src="data:image/png;base64,{habitnet_base64}" alt="Habitnet Logo" style="height: 94px;" />
    <img src="data:image/png;base64,{fenix_base64}" alt="Fênix Logo" style="height: 94px;" />
</div>
<h2 style="text-align: center; font-size: 22px; color: #9B1113; margin: 10px 0 20px 0;">
    Habitnet - Equipe Fênix - Pesquisa de Empreendimentos
</h2>
""", unsafe_allow_html=True)

st.markdown("""
<style>
body, .stApp {
background-color: #f0f0f0;
color: #003668;
}
h1, h2, h3, h4 {
color: #003668;
}
.stSelectbox label, .stDataFrameContainer {
color: #003668;
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
""", unsafe_allow_html=True)
    """,
)

def formatar_moeda(x):
    return f"R$ {x:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")

# Carregar a base de dados com cache
@st.cache_data(ttl=600)
def carregar_dados():
    return pd.read_excel("MEGATAB_EMPREEND_JUN2025vlight.xlsx")

df = carregar_dados()

# Padronizar nomes de colunas para evitar erros de digitação ou espaços
df.columns = df.columns.str.strip().str.upper()
df = df.rename(columns={"VAGA": "GARAGEM"})

# Limpeza adicional para filtros
colunas_filtro = ["CIDADE", "BAIRRO", "CONSTRUTORA", "EMPREENDIMENTO"]
opcoes_filtro = {
    col: sorted(df[col].dropna().unique().tolist()) for col in colunas_filtro if col in df.columns
}
for col in colunas_filtro:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()

# Verificar se as colunas LATITUDE e LONGITUDE existem
if "LATITUDE" in df.columns and "LONGITUDE" in df.columns:
    for coord in ["LATITUDE", "LONGITUDE"]:
        df[coord] = pd.to_numeric(df[coord].astype(str).str.replace(",", "."), errors="coerce")
else:
    st.error("As colunas 'LATITUDE' e 'LONGITUDE' não foram encontradas na planilha.")

# Formatar colunas de moeda
valor_cols = ["A PARTIR DE", "PREÇOS ATÉ", "RENDA NECESSÁRIA"]
for col in valor_cols:
    if col in df.columns:
        df[col] = df[col].apply(formatar_moeda)

# Criar coluna VER NO MAPA com link clicável
if "LATITUDE" in df.columns and "LONGITUDE" in df.columns:
    df["VER NO MAPA"] = df.apply(
        lambda row: f'<a href="https://www.google.com/maps/search/?api=1&query={row["LATITUDE"]},{row["LONGITUDE"]}" target="_blank">VER NO MAPA</a>'
        if pd.notna(row.get("LATITUDE")) and pd.notna(row.get("LONGITUDE")) else "",
        axis=1
    )

import base64

def img_to_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

habitnet_base64 = img_to_base64("Habitnet_hor.png")
fenix_base64 = img_to_base64("fenix.png")

st.markdown(
    f"""
    <div style="display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 20px;">
        <img src="data:image/png;base64,{habitnet_base64}" alt="Habitnet Logo" width="108" style="margin-right: 10px;">
    Habitnet - Equipe Fênix - Pesquisa de Empreendimentos
        <img src="data:image/png;base64,{fenix_base64}" alt="Fênix Logo" width="81" style="margin-left: 10px;">
    </div>
    """,
    unsafe_allow_html=True
)

# Filtros com dropdowns
cidade = st.multiselect("Selecione a Cidade", options=sorted(df["CIDADE"].dropna().unique()))
bairro = st.multiselect("Selecione o Bairro", options=sorted(df["BAIRRO"].dropna().unique()))
construtora = st.multiselect("Selecione a Construtora", options=sorted(df["CONSTRUTORA"].dropna().unique()))
empreendimento = st.multiselect("Selecione o Empreendimento", options=sorted(df["EMPREENDIMENTO"].dropna().unique()))

# Aplicar filtros
df_filtrado = df.copy()
if cidade:
    df_filtrado = df_filtrado[df_filtrado["CIDADE"].isin(cidade)]
if cidade:
    df_filtrado = df_filtrado[df_filtrado['CIDADE'].isin(cidade)]
if bairro:
    df_filtrado = df_filtrado[df_filtrado["BAIRRO"].isin(bairro)]
if bairro:
    df_filtrado = df_filtrado[df_filtrado['BAIRRO'].isin(bairro)]
if construtora:
    df_filtrado = df_filtrado[df_filtrado["CONSTRUTORA"].isin(construtora)]
if construtora:
    df_filtrado = df_filtrado[df_filtrado['CONSTRUTORA'].isin(construtora)]
if empreendimento:
    df_filtrado = df_filtrado[df_filtrado["EMPREENDIMENTO"].isin(empreendimento)]
if empreendimento:
    df_filtrado = df_filtrado[df_filtrado['EMPREENDIMENTO'].isin(empreendimento)]

# Exibir resultados sem LATITUDE e LONGITUDE
df_exibicao = df_filtrado.drop(columns=["LATITUDE", "LONGITUDE"], errors="ignore").copy()
if "LINK GOOGLE MAPS" in df_exibicao.columns:
    df_exibicao = df_exibicao.drop(columns=["LINK GOOGLE MAPS"], errors="ignore")

# Formatar ENTREGA como mm/aaaa
if "ENTREGA" in df_exibicao.columns:
    df_exibicao["ENTREGA"] = pd.to_datetime(df_exibicao["ENTREGA"], errors="coerce").dt.strftime('%m/%Y')

st.markdown(f"<h4 style=\"font-size: 22px; color: #003668;\">Resultados: {len(df_exibicao)} empreendimento(s) encontrado(s)</h4>", unsafe_allow_html=True)

# Botão para exportar tabela
buffer = io.BytesIO()
if not df_exibicao.empty:
    df_exibicao.to_excel(buffer, index=False)
    st.download_button(
        label="📅 Baixar tabela em Excel",
        data=buffer,
        file_name="resultado_empreendimentos.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Tabela com rolagem horizontal e vertical
tabela_html = df_exibicao.to_html(escape=False, index=False)

st.markdown(
    '<div style="overflow-x: auto; overflow-y: auto; max-height: 500px; border: 1px solid #ccc; padding: 8px">' + tabela_html + '</div>',
    unsafe_allow_html=True
)

# Criar mapa com marcadores
if not df_filtrado.empty and "LATITUDE" in df_filtrado.columns and "LONGITUDE" in df_filtrado.columns:
    m = folium.Map(location=[-3.75, -38.5], zoom_start=11)

    for _, row in df_filtrado.iterrows():
        try:
            lat = float(row["LATITUDE"])
            lon = float(row["LONGITUDE"])
            popup_text = f"{row['EMPREENDIMENTO']}"
            folium.Marker(
                location=[lat, lon],
                popup=popup_text,
                icon=folium.Icon(icon="glyphicon glyphicon-map-marker", prefix="glyphicon", color="red")
            ).add_to(m)
        except (ValueError, TypeError) as e:
            st.warning(f"Erro ao processar coordenadas para: {row['EMPREENDIMENTO']}")

    st.markdown("<h4 style=\"font-size: 22px;\">Mapa dos Empreendimentos Filtrados</h4>", unsafe_allow_html=True)
    st_folium(m, width=None, height=500)
else:
    st.info("Nenhum empreendimento com coordenadas disponíveis para exibir no mapa.")

# Carregar a base de dados com cache
@st.cache_data(ttl=600)
def carregar_dados():
    return pd.read_excel("MEGATAB_EMPREEND_JUN2025vlight.xlsx")

df = carregar_dados()

# Padronizar nomes de colunas para evitar erros de digitação ou espaços
df.columns = df.columns.str.strip().str.upper()
df = df.rename(columns={"VAGA": "GARAGEM"})

# Limpeza adicional para filtros
colunas_filtro = ["CIDADE", "BAIRRO", "CONSTRUTORA", "EMPREENDIMENTO"]
opcoes_filtro = {
    col: sorted(df[col].dropna().unique().tolist()) for col in colunas_filtro if col in df.columns
}
for col in colunas_filtro:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()

# Verificar se as colunas LATITUDE e LONGITUDE existem
if "LATITUDE" in df.columns and "LONGITUDE" in df.columns:
    for coord in ["LATITUDE", "LONGITUDE"]:
        df[coord] = pd.to_numeric(df[coord].astype(str).str.replace(",", "."), errors="coerce")
else:
    st.error("As colunas 'LATITUDE' e 'LONGITUDE' não foram encontradas na planilha.")

# Formatar colunas de moeda
valor_cols = ["A PARTIR DE", "PREÇOS ATÉ", "RENDA NECESSÁRIA"]
for col in valor_cols:
    if col in df.columns:
        df[col] = df[col].apply(formatar_moeda)

# Criar coluna VER NO MAPA com link clicável
if "LATITUDE" in df.columns and "LONGITUDE" in df.columns:
    df["VER NO MAPA"] = df.apply(
        lambda row: f'<a href="https://www.google.com/maps/search/?api=1&query={row["LATITUDE"]},{row["LONGITUDE"]}" target="_blank">VER NO MAPA</a>'
        if pd.notna(row.get("LATITUDE")) and pd.notna(row.get("LONGITUDE")) else "",
        axis=1
    )

import base64

def img_to_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

habitnet_base64 = img_to_base64("Habitnet_hor.png")
fenix_base64 = img_to_base64("fenix.png")

st.markdown(
    f"""
    <div style="display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 20px;">
        <img src="data:image/png;base64,{habitnet_base64}" alt="Habitnet Logo" width="108" style="margin-right: 10px;">
    Habitnet - Equipe Fênix - Pesquisa de Empreendimentos
        <img src="data:image/png;base64,{fenix_base64}" alt="Fênix Logo" width="81" style="margin-left: 10px;">
    </div>
    """,
    unsafe_allow_html=True
)

# Filtros com dropdowns
cidade = st.multiselect("Selecione a Cidade", options=sorted(df["CIDADE"].dropna().unique()))
bairro = st.multiselect("Selecione o Bairro", options=sorted(df["BAIRRO"].dropna().unique()))
construtora = st.multiselect("Selecione a Construtora", options=sorted(df["CONSTRUTORA"].dropna().unique()))
empreendimento = st.multiselect("Selecione o Empreendimento", options=sorted(df["EMPREENDIMENTO"].dropna().unique()))

# Aplicar filtros
df_filtrado = df.copy()
if cidade:
    df_filtrado = df_filtrado[df_filtrado["CIDADE"].isin(cidade)]
if cidade:
    df_filtrado = df_filtrado[df_filtrado['CIDADE'].isin(cidade)]
if bairro:
    df_filtrado = df_filtrado[df_filtrado["BAIRRO"].isin(bairro)]
if bairro:
    df_filtrado = df_filtrado[df_filtrado['BAIRRO'].isin(bairro)]
if construtora:
    df_filtrado = df_filtrado[df_filtrado["CONSTRUTORA"].isin(construtora)]
if construtora:
    df_filtrado = df_filtrado[df_filtrado['CONSTRUTORA'].isin(construtora)]
if empreendimento:
    df_filtrado = df_filtrado[df_filtrado["EMPREENDIMENTO"].isin(empreendimento)]
if empreendimento:
    df_filtrado = df_filtrado[df_filtrado['EMPREENDIMENTO'].isin(empreendimento)]

# Exibir resultados sem LATITUDE e LONGITUDE
df_exibicao = df_filtrado.drop(columns=["LATITUDE", "LONGITUDE"], errors="ignore").copy()
if "LINK GOOGLE MAPS" in df_exibicao.columns:
    df_exibicao = df_exibicao.drop(columns=["LINK GOOGLE MAPS"], errors="ignore")

# Formatar ENTREGA como mm/aaaa
if "ENTREGA" in df_exibicao.columns:
    df_exibicao["ENTREGA"] = pd.to_datetime(df_exibicao["ENTREGA"], errors="coerce").dt.strftime('%m/%Y')

st.markdown(f"<h4 style=\"font-size: 22px; color: #003668;\">Resultados: {len(df_exibicao)} empreendimento(s) encontrado(s)</h4>", unsafe_allow_html=True)

# Botão para exportar tabela
buffer = io.BytesIO()
if not df_exibicao.empty:
    df_exibicao.to_excel(buffer, index=False)
    st.download_button(
        label="📅 Baixar tabela em Excel",
        data=buffer,
        file_name="resultado_empreendimentos.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Tabela com rolagem horizontal e vertical
tabela_html = df_exibicao.to_html(escape=False, index=False)

st.markdown(
    '<div style="overflow-x: auto; overflow-y: auto; max-height: 500px; border: 1px solid #ccc; padding: 8px">' + tabela_html + '</div>',
    unsafe_allow_html=True
)

# Criar mapa com marcadores
if not df_filtrado.empty and "LATITUDE" in df_filtrado.columns and "LONGITUDE" in df_filtrado.columns:
    m = folium.Map(location=[-3.75, -38.5], zoom_start=11)

    for _, row in df_filtrado.iterrows():
        try:
            lat = float(row["LATITUDE"])
            lon = float(row["LONGITUDE"])
            popup_text = f"{row['EMPREENDIMENTO']}"
            folium.Marker(
                location=[lat, lon],
                popup=popup_text,
                icon=folium.Icon(icon="glyphicon glyphicon-map-marker", prefix="glyphicon", color="red")
            ).add_to(m)
        except (ValueError, TypeError) as e:
            st.warning(f"Erro ao processar coordenadas para: {row['EMPREENDIMENTO']}")

    st.markdown("<h4 style=\"font-size: 22px;\">Mapa dos Empreendimentos Filtrados</h4>", unsafe_allow_html=True)
    st_folium(m, width=None, height=500)
else:
    st.info("Nenhum empreendimento com coordenadas disponíveis para exibir no mapa.")
