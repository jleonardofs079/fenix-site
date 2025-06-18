import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit.components.v1 import html
import io

# Estilos adaptáveis para modo claro e escuro

st.markdown(
    f'''
    <div style="display: flex; justify-content: center; align-items: center; gap: 20px; flex-wrap: wrap; margin-top: 10px;">
        <img src="data:image/png;base64,{habitnet_base64}" alt="Habitnet Logo" style="height: 94px;" />
        <img src="data:image/png;base64,{fenix_base64}" alt="Fênix Logo" style="height: 94px;" />
    </div>
    <h2 style="text-align: center; font-size: 22px; color: #9B1113; margin: 10px 0 20px 0;">
        🔍 Habitnet - Equipe Fênix - Pesquisa de Empreendimentos
    </h2>
    ''',
    unsafe_allow_html=True
)
,
    unsafe_allow_html=True
)

# Filtros com dropdowns
cidade = st.multiselect("Selecione a Cidade", options=opcoes_filtro.get("CIDADE", []), default=opcoes_filtro.get("CIDADE", [])))
bairro = st.multiselect("Selecione o Bairro", options=opcoes_filtro.get("BAIRRO", []), default=opcoes_filtro.get("BAIRRO", [])))
construtora = st.multiselect("Selecione a Construtora", options=opcoes_filtro.get("CONSTRUTORA", []), default=opcoes_filtro.get("CONSTRUTORA", [])))
empreendimento = st.multiselect("Selecione o Empreendimento", options=opcoes_filtro.get("EMPREENDIMENTO", []), default=opcoes_filtro.get("EMPREENDIMENTO", [])))

# Aplicar filtros
df_filtrado = df.copy()
if cidade:
    df_filtrado = df_filtrado[df_filtrado["CIDADE"].isin(cidade)]
if bairro:
    df_filtrado = df_filtrado[df_filtrado["BAIRRO"].isin(bairro)]
if construtora:
    df_filtrado = df_filtrado[df_filtrado["CONSTRUTORA"].isin(construtora)]
if empreendimento:
    df_filtrado = df_filtrado[df_filtrado["EMPREENDIMENTO"].isin(empreendimento)]

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
