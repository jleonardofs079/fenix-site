import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit.components.v1 import html
import io
import os

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
        }
        th, td {
            padding: 8px;
            text-align: left;
            border: 1px solid #ccc;
            white-space: normal;
            word-break: break-word;
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

# Verificação do arquivo Excel
excel_path = "MEGATAB_EMPREEND_JUN2025vlight.xlsx"
if not os.path.exists(excel_path):
    st.error(f"Arquivo '{excel_path}' não encontrado. Verifique se ele está no diretório do app.")
    st.stop()

# Carregar a base de dados com cache
@st.cache_data
def carregar_dados():
    return pd.read_excel(excel_path)

df = carregar_dados()

# Padronizar nomes de colunas para evitar erros de digitação ou espaços
df.columns = df.columns.str.strip().str.upper()

# Renomear coluna VAGA para GARAGEM
if "VAGA" in df.columns:
    df = df.rename(columns={"VAGA": "GARAGEM"})

# Formatar coluna ENTREGA como mmm/aa
if "ENTREGA" in df.columns:
    df["ENTREGA"] = pd.to_datetime(df["ENTREGA"], errors="coerce")

# Limpeza adicional para filtros
colunas_filtro = ["CIDADE", "BAIRRO", "CONSTRUTORA", "EMPREENDIMENTO"]
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
        df[col] = df[col].apply(lambda x: f"R$ {x:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))

# Criar coluna VER NO MAPA com link clicável
if "LATITUDE" in df.columns and "LONGITUDE" in df.columns:
    df["VER NO MAPA"] = df.apply(
        lambda row: f'<a href="https://www.google.com/maps/search/?api=1&query={row["LATITUDE"]},{row["LONGITUDE"]}" target="_blank">VER NO MAPA</a>'
        if pd.notna(row.get("LATITUDE")) and pd.notna(row.get("LONGITUDE")) else "",
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

# Exibir resultados sem LATITUDE e LONGITUDE
df_exibicao = df_filtrado.drop(columns=["LATITUDE", "LONGITUDE"], errors="ignore").copy()
if "LINK GOOGLE MAPS" in df_exibicao.columns:
    df_exibicao = df_exibicao.drop(columns=["LINK GOOGLE MAPS"], errors="ignore")

# Formatar ENTREGA na exibição como mmm/aa
if "ENTREGA" in df_exibicao.columns:
    df_exibicao["ENTREGA"] = df_exibicao["ENTREGA"].dt.strftime("%b/%y")

st.write(f"### Resultados: {len(df_exibicao)} empreendimento(s) encontrado(s)")

# Botão para exportar tabela
buffer = io.BytesIO()
if not df_exibicao.empty:
    df_exibicao.to_excel(buffer, index=False)
    st.download_button(
        label="📥 Baixar tabela em Excel",
        data=buffer,
        file_name="resultado_empreendimentos.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Tabela com rolagem horizontal e vertical com quebra de linha restaurada
st.markdown(
    f'''<div style="overflow-x: auto; overflow-y: auto; max-height: 500px; border: 1px solid #ccc; padding: 8px">
    {df_exibicao.to_html(escape=False, index=False)}
    </div>''',
    unsafe_allow_html=True
)

# Criar mapa com marcadores
if not df_filtrado.empty and "LATITUDE" in df_filtrado.columns and "LONGITUDE" in df_filtrado.columns:
    m = folium.Map(location=[-3.75, -38.5], zoom_start=11)

    for _, row in df_filtrado.iterrows():
        try:
            lat = float(row["LATITUDE"])
            lon = float(row["LONGITUDE"])
            popup_text = f"{row['EMPREENDIMENTO']}<br>{row['ENDEREÇO']} - {row['CIDADE']}"
            folium.Marker(
                location=[lat, lon],
                popup=popup_text,
                icon=folium.Icon(icon="glyphicon glyphicon-map-marker", prefix="glyphicon", color="red")
            ).add_to(m)
        except (ValueError, TypeError) as e:
            st.warning(f"Erro ao processar coordenadas para: {row['EMPREENDIMENTO']}")

    st.write("### Mapa dos Empreendimentos Filtrados")
    st_folium(m, width=None, height=500)
else:
    st.info("Nenhum empreendimento com coordenadas disponíveis para exibir no mapa.")
