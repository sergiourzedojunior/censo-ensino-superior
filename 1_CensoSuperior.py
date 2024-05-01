import streamlit as st
import pandas as pd
import time

# Set Streamlit page config
st.set_page_config(
    layout="wide",
    page_title="Dados do Censo Ensino Superior - Medicina"
)

# Decorator for caching data functions
def cache_data(func):
    def wrapper():
        key = func.__name__
        if key not in st.session_state:
            st.session_state[key] = func()
        return st.session_state[key]
    return wrapper

# Function to load data with caching
@cache_data
def load_df_grouped_reset():
    time.sleep(5)  # Simulated delay to mimic a long loading process
    return pd.read_csv("df_grouped_reset.csv")

@cache_data
def load_df_selected():
    time.sleep(5)  # Simulated delay to mimic a long loading process
    return pd.read_csv("df_selected.csv")

@cache_data
def load_final_forecast():
    time.sleep(5)  # Simulated delay to mimic a long loading process
    return pd.read_csv("final_forecast.csv")

@cache_data
def load_forecast_insc():
    time.sleep(5)  # Simulated delay to mimic a long loading process
    return pd.read_csv("forecast_insc.csv")

@cache_data
def load_forecast_vg():
    time.sleep(5)  # Simulated delay to mimic a long loading process
    return pd.read_csv("forecast_vg.csv")

@cache_data
def load_df_unique_count_IES_UF():
    time.sleep(5)  # Simulated delay to mimic a long loading process
    return pd.read_csv("df_unique_count_IES_UF.csv")

# App main interface
st.markdown("# Dados do Censo Ensino Superior - Medicina! 🩺")
st.sidebar.markdown("Desenvolvido por [SergioUrzedoJr_github](https://github.com/sergiourzedojunior/sergiourzedojunior.git)")

# Main Markdown Introduction
st.markdown(
    """
    O Censo da Educação Superior, realizado anualmente pelo Inep, é a pesquisa mais completa do Brasil sobre as instituições de educação superior que ofertam cursos de graduação e sequenciais de formação específica, bem como sobre seus alunos e docentes.

    Em 2022, foram oferecidas mais de 22,8 milhões de vagas em cursos de graduação, sendo 75,5% vagas novas e 24,4% vagas remanescentes. A rede privada ofertou 96,2% do total de vagas em cursos de graduação em 2022. A rede pública correspondeu a 3,8% das vagas ofertadas pelas IES.

    Além disso, 72% dos alunos que foram aprovados no ensino superior privado optaram por estudar à distância, segundo dados do Censo da Educação Superior 2022.

    Este aplicativo foi desenvolvido para explorar os dados do Censo da Educação Superior, com foco em Medicina, de 2009 a 2022. Acesse os dados e explore as análises disponíveis!
    """
)
st.markdown("---")  # Markdown syntax for a horizontal line

# Ensure all data is loaded upfront
df_unique_count_IES_UF = load_df_unique_count_IES_UF().drop(columns=['Unnamed: 0'])
df_unique_count_IES_UF.reset_index(drop=True, inplace=True)
df_selected = load_df_selected()  # Load df_selected here

# Rounding the specific columns to one decimal place
df_unique_count_IES_UF['ProporçãoBR'] = df_unique_count_IES_UF['ProporçãoBR'].apply(lambda x: round(x, 1))
df_unique_count_IES_UF['Proporção_Região'] = df_unique_count_IES_UF['Proporção_Região'].apply(lambda x: round(x, 1))

# Display data
col1, col2, col3, col4 = st.columns(4)
unique_count_IES = df_unique_count_IES_UF['QTD_EscolasMed'].sum()
unique_count_MUNIC = df_selected['CO_MUNICIPIO'].nunique()

col1.metric(label="**Quantidade de Escolas de Medicina no período:**", value=unique_count_IES)
col2.metric(label="**Quantidade de Municípios com Escolas de Medicina no período:**", value=unique_count_MUNIC)

# Apply a background gradient that changes based on value
styled_df = df_unique_count_IES_UF.style.background_gradient(subset=['ProporçãoBR', 'Proporção_Região'], cmap='Greens', low=0.5, high=0.5)

# Display styled DataFrame in Streamlit
st.dataframe(styled_df)

