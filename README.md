
# 📍 Ferramenta de Pesquisa de Empreendimentos - Habitnet

Este projeto é uma ferramenta interativa criada com Streamlit para facilitar a busca por empreendimentos imobiliários da Habitnet. A plataforma permite filtrar por cidade, bairro, construtora e nome do empreendimento, além de visualizar os resultados em um mapa com marcadores interativos.

---

## 🚀 Como rodar o projeto

### 1. Clone o repositório ou envie os arquivos para o Streamlit Cloud

Inclua os seguintes arquivos no seu repositório:
- `app.py` (código principal)
- `MEGATAB_EMPREEND_JUN2025vlight.xlsx` (base de dados)
- `requirements.txt` (dependências do Python)

### 2. Requisitos

Instale os pacotes necessários:

```bash
pip install -r requirements.txt
```

### 3. Execute com Streamlit

```bash
streamlit run app.py
```

---

## 🧩 Funcionalidades

- Filtros por **Cidade**, **Bairro**, **Construtora** e **Empreendimento**
- Tabela de resultados com **valores formatados em R$**
- Link direto para **visualização no Google Maps**
- Mapa com marcadores nos empreendimentos localizados

---

## 🎯 Observações

- As colunas `LATITUDE` e `LONGITUDE` são utilizadas apenas internamente para os marcadores.
- A coluna `VER NO MAPA` permite que o usuário abra a localização exata no Google Maps.
- Visualização responsiva para desktop e dispositivos móveis.

---

## 📫 Suporte

Para dúvidas ou sugestões, entre em contato com a equipe da [Habitnet](https://habitnet.com.br).
