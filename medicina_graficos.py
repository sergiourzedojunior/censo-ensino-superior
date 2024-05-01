# %%
import numpy as np

# %%
import pandas as pd
import os

# Define the file paths
file_paths = [os.path.join(r"D:\OneDrive\censo ensino superior\microdados_censo_da_educacao_superior_" + str(year), 
                           r"microdadosdocensodaeducacosuperior" + str(year) if year != 2022 else r"microdados_educaco_superior_" + str(year), 
                           r"dados\MICRODADOS_CADASTRO_CURSOS_" + str(year) + "_med.parquet") 
              for year in range(2009, 2023)]

# Initialize an empty list to store the DataFrames
dfs = []

# Loop through each file path
for file_path in file_paths:
    # Check if the file exists
    if os.path.exists(file_path):
        # Read the Parquet file into a DataFrame
        df = pd.read_parquet(file_path)
        # Append the DataFrame to the list
        dfs.append(df)
    else:
        print(f"File not found: {file_path}")

# Concatenate all the DataFrames in the list
df_concat = pd.concat(dfs, ignore_index=True)

# %%
pd.set_option('display.max_columns', None)
df_concat

# %%
# Define the columns to select
columns_to_select = [
    "NU_ANO_CENSO",
    "NO_REGIAO",
    "CO_REGIAO",
    "NO_UF",
    "SG_UF",
    "CO_UF",
    "NO_MUNICIPIO",
    "CO_MUNICIPIO",
    "IN_CAPITAL",
    "TP_ORGANIZACAO_ACADEMICA",
    "TP_CATEGORIA_ADMINISTRATIVA",
    "TP_REDE",
    "CO_IES",
    "NO_CINE_ROTULO",
    "CO_CINE_ROTULO",
    "CO_CINE_AREA_GERAL",
    "NO_CINE_AREA_GERAL",
    "CO_CINE_AREA_ESPECIFICA",
    "NO_CINE_AREA_ESPECIFICA",
    "CO_CINE_AREA_DETALHADA",
    "NO_CINE_AREA_DETALHADA",
    "TP_GRAU_ACADEMICO",
    "TP_MODALIDADE_ENSINO",
    "TP_NIVEL_ACADEMICO",
    "QT_CURSO",
    "QT_VG_TOTAL",
    "QT_VG_TOTAL_DIURNO",
    "QT_VG_TOTAL_NOTURNO",
    "QT_VG_TOTAL_EAD",
    "QT_VG_NOVA",
    "QT_VG_PROC_SELETIVO",
    "QT_VG_REMANESC",
    "QT_VG_PROG_ESPECIAL",
    "QT_INSCRITO_TOTAL",
    "QT_INSCRITO_TOTAL_DIURNO",
    "QT_INSCRITO_TOTAL_NOTURNO",
    "QT_INSCRITO_TOTAL_EAD",
    "QT_INSC_VG_NOVA",
    "QT_INSC_PROC_SELETIVO",
    "QT_INSC_VG_REMANESC",
    "QT_INSC_VG_PROG_ESPECIAL",
    "QT_ING",
    "QT_ING_FEM",
    "QT_ING_MASC",
    "QT_ING_DIURNO",
    "QT_ING_NOTURNO",
    "QT_ING_VG_NOVA",
    "QT_ING_VESTIBULAR",
    "QT_ING_ENEM"
]

# Select the necessary columns
df_selected = df_concat[columns_to_select]

# Convert the columns to integer
df_selected['QT_VG_TOTAL'] = df_selected['QT_VG_TOTAL'].astype(int)
df_selected['QT_INSCRITO_TOTAL'] = df_selected['QT_INSCRITO_TOTAL'].astype(int)

# Group the DataFrame and calculate the sum for each group
df_grouped = df_selected.groupby(['NU_ANO_CENSO', 'NO_CINE_AREA_DETALHADA'])[['QT_VG_TOTAL', 'QT_INSCRITO_TOTAL']].sum()

# # Print the grouped DataFrame
# print(df_grouped)

# %%
import pandas as pd
from prophet import Prophet

# Resetando o índice do DataFrame agrupado para facilitar o acesso aos dados
df_grouped_reset = df_grouped.reset_index()
df_grouped_reset.to_csv(r'D:\OneDrive\censo ensino superior\df_grouped_reset.csv')
# Preparando os DataFrames para o Prophet
df_prophet_vg = pd.DataFrame({
    'ds': pd.to_datetime(df_grouped_reset['NU_ANO_CENSO'], format='%Y'),
    'y': df_grouped_reset['QT_VG_TOTAL']
})

df_prophet_insc = pd.DataFrame({
    'ds': pd.to_datetime(df_grouped_reset['NU_ANO_CENSO'], format='%Y'),
    'y': df_grouped_reset['QT_INSCRITO_TOTAL']
})

# Inicialização e ajuste dos modelos para VG_TOTAL e INSCRITO_TOTAL
m_vg = Prophet()
m_insc = Prophet()
m_vg.fit(df_prophet_vg)
m_insc.fit(df_prophet_insc)

# Extendendo o DataFrame para incluir previsões até 2023
future_vg = m_vg.make_future_dataframe(periods=2, freq='Y')
future_insc = m_insc.make_future_dataframe(periods=2, freq='Y')

# Gerando previsões
forecast_vg = m_vg.predict(future_vg)
forecast_insc = m_insc.predict(future_insc)

# Removendo a previsão de 31 de dezembro de 2022
forecast_vg = forecast_vg[forecast_vg['ds'] != '2022-12-31']
forecast_insc = forecast_insc[forecast_insc['ds'] != '2022-12-31']

# Juntando as previsões com os dados reais para cálculo do MAE
forecast_vg = forecast_vg.set_index('ds').join(df_prophet_vg.set_index('ds'))
forecast_insc = forecast_insc.set_index('ds').join(df_prophet_insc.set_index('ds'))
forecast_vg.reset_index(inplace=True)
forecast_insc.reset_index(inplace=True)

# Cálculo do MAPE para cada conjunto de previsões
forecast_vg['percentage_error'] = ((forecast_vg['yhat'] - forecast_vg['y']).abs() / forecast_vg['y']) * 100
forecast_insc['percentage_error'] = ((forecast_insc['yhat'] - forecast_insc['y']).abs() / forecast_insc['y']) * 100
mape_vg = forecast_vg['percentage_error'].mean()
mape_insc = forecast_insc['percentage_error'].mean()

# # Mostrando os resultados
# print("MAPE for QT_VG_TOTAL predictions up to 2022:", mape_vg)
# print("MAPE for QT_INSCRITO_TOTAL predictions up to 2022:", mape_insc)

# # Visualização opcional das previsões e erros
# print("\nPredictions and Percentage Errors for QT_VG_TOTAL:")
# print(forecast_vg[['ds', 'yhat', 'y', 'percentage_error']])
# print("\nPredictions and Percentage Errors for QT_INSCRITO_TOTAL:")
# print(forecast_insc[['ds', 'yhat', 'y', 'percentage_error']])


# %%
import sys
import pandas as pd

# Lista todas as variáveis no namespace
variables = %who_ls

# Itera sobre as variáveis e imprime apenas os DataFrames
for variable in variables:
    if isinstance(eval(variable), pd.DataFrame):
        print(f"{variable}:\n{eval(variable)}\n")

# %%
import sys
import pandas as pd

# Lista todas as variáveis no namespace
variables = %who_ls

# Itera sobre as variáveis e imprime apenas as informações de cada DataFrame
for variable in variables:
    if isinstance(eval(variable), pd.DataFrame):
        print(f"{variable}:\n")
        eval(variable).info()
        print("\n")

# %%
# Obtém o nome de todas as colunas que começam com 'QT_'
cols = [col for col in df_selected.columns if col.startswith('QT_')]

# Transforma essas colunas em numéricas
df_selected[cols] = df_selected[cols].apply(pd.to_numeric, errors='coerce')

# %%
# Transforma a coluna 'NU_ANO_CENSO' em datetime
df_selected['NU_ANO_CENSO'] = pd.to_datetime(df_selected['NU_ANO_CENSO'], format='%Y')

# %%
df_selected.info()

# %%
# import plotly.graph_objects as go
# import pandas as pd
# import numpy as np


# # Separar dados até 2022 e dados de 2023
# df_until_2022 = forecast_vg[forecast_vg['ds'] <= '2022-12-31']
# df_2023 = forecast_vg[forecast_vg['ds'] > '2022-12-31']

# # Gráfico comparativo de yhat (previsões) e y (valores reais)
# fig_comparison = go.Figure()

# # Dados até 2022
# fig_comparison.add_trace(go.Scatter(
#     x=df_until_2022['ds'], 
#     y=df_until_2022['yhat'], 
#     mode='lines+markers', 
#     name='Predicted until 2022', 
#     line=dict(color='blue'),
#     customdata=np.stack((df_until_2022['y'], df_until_2022['percentage_error']), axis=-1),
#     hovertemplate="<b>%{x}</b><br><br>Predicted: %{y:.2f}<br>Actual: %{customdata[0]:.2f}<br>Error: %{customdata[1]:.2f}%<extra></extra>"
# ))

# # Dados reais até 2022
# fig_comparison.add_trace(go.Scatter(
#     x=df_until_2022['ds'], 
#     y=df_until_2022['y'], 
#     mode='lines+markers', 
#     name='Actual until 2022', 
#     line=dict(color='red')
# ))

# # Previsões para 2023
# fig_comparison.add_trace(go.Scatter(
#     x=df_2023['ds'], 
#     y=df_2023['yhat'], 
#     mode='lines+markers', 
#     name='Predicted for 2023', 
#     line=dict(color='green', dash='dash'),
#     hovertemplate="<b>%{x}</b><br><br>Predicted: %{y:.2f}<br><extra></extra>"
# ))

# # Adicionando título e labels
# fig_comparison.update_layout(
#     title='Comparison of Predicted and Actual Values with 2023 Projections',
#     xaxis_title='Year',
#     yaxis_title='Values',
#     template='plotly_dark'
# )

# # Mostrar o gráfico
# fig_comparison.show()


# %%
import plotly.graph_objects as go

# %%
# Calcular a taxa de crescimento percentual para os dados reais e previstos
forecast_vg['actual_growth_rate'] = forecast_vg['y'].pct_change()
forecast_vg['predicted_growth_rate'] = forecast_vg['yhat'].pct_change()

# Atualizar a seleção de dados
df_until_2022 = forecast_vg[forecast_vg['ds'] <= '2022-12-31']
df_2023 = forecast_vg[forecast_vg['ds'] > '2022-12-31']

# Atualizar o gráfico
fig_comparison = go.Figure()

# Dados até 2022
fig_comparison.add_trace(go.Scatter(
    x=df_until_2022['ds'], 
    y=df_until_2022['yhat'], 
    mode='lines+markers', 
    name='Predicted until 2022', 
    line=dict(color='blue'),
    customdata=np.stack((df_until_2022['y'], df_until_2022['percentage_error'], df_until_2022['predicted_growth_rate']), axis=-1),
    hovertemplate="<b>%{x}</b><br><br>Predicted: %{y:.2f}<br>Actual: %{customdata[0]:.2f}<br>Error: %{customdata[1]:.2f}%<br>Predicted Growth Rate: %{customdata[2]:.2f}%<extra></extra>"
))

# Dados reais até 2022
fig_comparison.add_trace(go.Scatter(
    x=df_until_2022['ds'], 
    y=df_until_2022['y'], 
    mode='lines+markers', 
    name='Actual until 2022', 
    line=dict(color='red'),
    customdata=np.stack((df_until_2022['yhat'], df_until_2022['percentage_error'], df_until_2022['actual_growth_rate']), axis=-1),
    hovertemplate="<b>%{x}</b><br><br>Actual: %{y:.2f}<br>Predicted: %{customdata[0]:.2f}<br>Error: %{customdata[1]:.2f}%<br>Actual Growth Rate: %{customdata[2]:.2f}%<extra></extra>"
))

# Previsões para 2023
fig_comparison.add_trace(go.Scatter(
    x=df_2023['ds'], 
    y=df_2023['yhat'], 
    mode='lines+markers', 
    name='Predicted for 2023', 
    line=dict(color='green', dash='dash'),
    customdata=df_2023['predicted_growth_rate'],
    hovertemplate="<b>%{x}</b><br><br>Predicted: %{y:.2f}<br>Predicted Growth Rate: %{customdata:.2f}%<extra></extra>"
))

# Adicionando título e labels
fig_comparison.update_layout(
    title='Comparison of Predicted and Actual Values with 2023 Projections',
    xaxis_title='Year',
    yaxis_title='Values',
    template='plotly_dark'
)

# Mostrar o gráfico
fig_comparison.show()

# %%
# Calcular a taxa de crescimento percentual para os dados reais e previstos
forecast_insc['actual_growth_rate'] = forecast_insc['y'].pct_change()
forecast_insc['predicted_growth_rate'] = forecast_insc['yhat'].pct_change()

# Atualizar a seleção de dados
df_until_2022 = forecast_insc[forecast_insc['ds'] <= '2022-12-31']
df_2023 = forecast_insc[forecast_insc['ds'] > '2022-12-31']

# Atualizar o gráfico
fig_comparison = go.Figure()

# Dados até 2022
fig_comparison.add_trace(go.Scatter(
    x=df_until_2022['ds'], 
    y=df_until_2022['yhat'], 
    mode='lines+markers', 
    name='Predicted until 2022', 
    line=dict(color='blue'),
    customdata=np.stack((df_until_2022['y'], df_until_2022['percentage_error'], df_until_2022['predicted_growth_rate']), axis=-1),
    hovertemplate="<b>%{x}</b><br><br>Predicted: %{y:.2f}<br>Actual: %{customdata[0]:.2f}<br>Error: %{customdata[1]:.2f}%<br>Predicted Growth Rate: %{customdata[2]:.2f}%<extra></extra>"
))

# Dados reais até 2022
fig_comparison.add_trace(go.Scatter(
    x=df_until_2022['ds'], 
    y=df_until_2022['y'], 
    mode='lines+markers', 
    name='Actual until 2022', 
    line=dict(color='red'),
    customdata=np.stack((df_until_2022['yhat'], df_until_2022['percentage_error'], df_until_2022['actual_growth_rate']), axis=-1),
    hovertemplate="<b>%{x}</b><br><br>Actual: %{y:.2f}<br>Predicted: %{customdata[0]:.2f}<br>Error: %{customdata[1]:.2f}%<br>Actual Growth Rate: %{customdata[2]:.2f}%<extra></extra>"
))

# Previsões para 2023
fig_comparison.add_trace(go.Scatter(
    x=df_2023['ds'], 
    y=df_2023['yhat'], 
    mode='lines+markers', 
    name='Predicted for 2023', 
    line=dict(color='green', dash='dash'),
    customdata=df_2023['predicted_growth_rate'],
    hovertemplate="<b>%{x}</b><br><br>Predicted: %{y:.2f}<br>Predicted Growth Rate: %{customdata:.2f}%<extra></extra>"
))

# Adicionando título e labels
fig_comparison.update_layout(
    title='Comparison of Predicted and Actual Values with 2023 Projections',
    xaxis_title='Year',
    yaxis_title='Values',
    template='plotly_dark'
)

# Mostrar o gráfico
fig_comparison.show()

# %%
# import plotly.graph_objects as go
# import pandas as pd
# import numpy as np

# # Separar dados até 2022 e dados de 2023
# df_until_2022 = forecast_insc[forecast_insc['ds'] <= '2022-12-31']
# df_2023 = forecast_insc[forecast_insc['ds'] > '2022-12-31']

# # Gráfico comparativo de yhat (previsões) e y (valores reais)
# fig_comparison = go.Figure()

# # Dados até 2022
# fig_comparison.add_trace(go.Scatter(
#     x=df_until_2022['ds'], 
#     y=df_until_2022['yhat'], 
#     mode='lines+markers', 
#     name='Predicted until 2022', 
#     line=dict(color='blue'),
#     customdata=np.stack((df_until_2022['y'], df_until_2022['percentage_error']), axis=-1),
#     hovertemplate="<b>%{x}</b><br><br>Predicted: %{y:.2f}<br>Actual: %{customdata[0]:.2f}<br>Error: %{customdata[1]:.2f}%<extra></extra>"
# ))

# # Dados reais até 2022
# fig_comparison.add_trace(go.Scatter(
#     x=df_until_2022['ds'], 
#     y=df_until_2022['y'], 
#     mode='lines+markers', 
#     name='Actual until 2022', 
#     line=dict(color='red')
# ))

# # Previsões para 2023
# fig_comparison.add_trace(go.Scatter(
#     x=df_2023['ds'], 
#     y=df_2023['yhat'], 
#     mode='lines+markers', 
#     name='Predicted for 2023', 
#     line=dict(color='green', dash='dash'),
#     hovertemplate="<b>%{x}</b><br><br>Predicted: %{y:.2f}<br><extra></extra>"
# ))

# # Adicionando título e labels
# fig_comparison.update_layout(
#     title='Comparison of Predicted and Actual Values with 2023 Projections',
#     xaxis_title='Year',
#     yaxis_title='Values',
#     template='plotly_dark'
# )

# # Mostrar o gráfico
# fig_comparison.show()


# %%
# Criando um identificador único para cada combinação de ano e UF
df_selected['Year_UF'] = df_selected['NU_ANO_CENSO'].astype(str) + '_' + df_selected['SG_UF']

# %%
# Convert 'NU_ANO_CENSO' to datetime format
df_selected['NU_ANO_CENSO'] = pd.to_datetime(df_selected['NU_ANO_CENSO'], format='%Y')

# %%
df_selected.info()

# %%
# Agrupar df_selected por Year_UF para sumarizar 'QT_VG_TOTAL'
uf_annual_summary = df_selected.groupby(['Year_UF', 'NU_ANO_CENSO', 'SG_UF'])['QT_VG_TOTAL'].sum().reset_index()

# %%
# Calcular o total nacional para cada ano
total_annual = df_selected.groupby('NU_ANO_CENSO')['QT_VG_TOTAL'].sum().reset_index()
total_annual.rename(columns={'QT_VG_TOTAL': 'Total'}, inplace=True)


# %%
# Juntar os totais ao resumo por Year_UF e calcular a proporção
uf_annual_summary = uf_annual_summary.merge(total_annual, on='NU_ANO_CENSO')
uf_annual_summary['Proportion'] = uf_annual_summary['QT_VG_TOTAL'] / uf_annual_summary['Total']


# %%
# Converter 'ds' para o formato de ano no DataFrame forecast_vg e assegurar que é inteiro
forecast_vg['Year'] = pd.to_datetime(forecast_vg['ds']).dt.year

# %%
forecast_vg.info()

# %%
# Ensure 'NU_ANO_CENSO' in uf_annual_summary is an integer for compatibility
if pd.api.types.is_datetime64_any_dtype(uf_annual_summary['NU_ANO_CENSO']):
    uf_annual_summary['NU_ANO_CENSO'] = uf_annual_summary['NU_ANO_CENSO'].dt.year
else:
    uf_annual_summary['NU_ANO_CENSO'] = uf_annual_summary['NU_ANO_CENSO'].astype(int)

# %%
# Mesclar proporções com as previsões de yhat
forecast_distributed = uf_annual_summary.merge(forecast_vg[['Year', 'yhat']], left_on='NU_ANO_CENSO', right_on='Year', how='left')
forecast_distributed['yhat_adjusted'] = forecast_distributed['Proportion'] * forecast_distributed['yhat']

# Calcular o erro percentual entre o valor real e a previsão ajustada
forecast_distributed['error_percentage'] = ((forecast_distributed['yhat_adjusted'] - forecast_distributed['QT_VG_TOTAL']).abs() / forecast_distributed['QT_VG_TOTAL']) * 100

# Criar o DataFrame final com as previsões ajustadas por UF
final_forecast = forecast_distributed[['NU_ANO_CENSO', 'SG_UF', 'yhat_adjusted', 'QT_VG_TOTAL', 'error_percentage']]

# Filtrar as previsões apenas para o ano de 2023
forecast_distributed_2023 = forecast_distributed[forecast_distributed['NU_ANO_CENSO'] == 2023]

# Concatenar as previsões de 2023 com final_forecast
final_forecast = pd.concat([final_forecast, forecast_distributed_2023[['NU_ANO_CENSO', 'SG_UF', 'yhat_adjusted', 'QT_VG_TOTAL', 'error_percentage']]])

# %%
# Atualizar a média móvel no DataFrame para todos os anos e arredondar
final_forecast['rolling_yhat_adjusted'] = final_forecast.groupby('SG_UF')['yhat_adjusted'].transform(lambda x: x.rolling(window=3, min_periods=1).mean()).round(2)

# Calcular a média móvel de dois anos apenas para a última entrada (assumindo que são os dados para 2023) e arredondar
window_size = 2
final_forecast['MA_yhat_adjusted'] = final_forecast.groupby('SG_UF')['yhat_adjusted'].transform(lambda x: x.rolling(window=window_size, min_periods=1).mean()).round(2)

# Filtrar para manter apenas as entradas mais recentes por UF, presumindo ser de 2023
latest_forecasts = final_forecast.drop_duplicates(subset=['SG_UF'], keep='last')

# Criar o gráfico com linhas para 'yhat_adjusted' e 'QT_VG_TOTAL'
fig = go.Figure()

uf_dropdown = final_forecast['SG_UF'].unique()
for uf in uf_dropdown:
    filtered_df = final_forecast[final_forecast['SG_UF'] == uf]
    latest_data = latest_forecasts[latest_forecasts['SG_UF'] == uf]
    fig.add_trace(go.Scatter(x=filtered_df['NU_ANO_CENSO'], y=filtered_df['yhat_adjusted'].round(2),
                             mode='lines+markers',
                             name=f'{uf} Previsão'))
    fig.add_trace(go.Scatter(x=filtered_df['NU_ANO_CENSO'], y=filtered_df['QT_VG_TOTAL'].round(2),
                             mode='lines+markers',
                             name=f'{uf} Real'))
    # Atualizar ano para 2023 na previsão de 2023
    fig.add_trace(go.Scatter(x=[latest_data['NU_ANO_CENSO'].values[0] + 1], y=latest_data['MA_yhat_adjusted'],
                             mode='markers',
                             marker=dict(size=10, color='green'),
                             name=f'{uf} Previsão 2023'))

# Criar botões de filtro para cada UF no dropdown
buttons = [dict(label='Todos',
                method='update',
                args=[{'visible': [True] * len(uf_dropdown) * 3},
                      {'title': 'Previsão Ajustada, Valores Reais por UF'}])]
for i, uf in enumerate(uf_dropdown):
    visibility = [False] * len(uf_dropdown) * 3
    visibility[i*3:(i+1)*3] = [True, True, True]  # Visibilidade para previsão, real, e previsão 2023
    buttons.append(dict(label=uf,
                        method='update',
                        args=[{'visible': visibility},
                              {'title': f'Previsão e Valores Reais para {uf}'}]))

# Atualizar o layout do gráfico com o dropdown e detalhes de estilo
fig.update_layout(
    title='Previsão Ajustada e Valores Reais por UF',
    xaxis_title='Ano',
    yaxis_title='Valores',
    legend_title='Séries',
    updatemenus=[dict(active=0,
                      buttons=buttons,
                      direction='down',
                      pad={'r': 10, 't': 10},
                      showactive=True,
                      x=0.1,
                      xanchor='left',
                      y=1.15,
                      yanchor='top')],
    hovermode='closest'
)

# Mostrar o gráfico
fig.show()


# %%
df_selected.info()

# %%
unique_count_IES = df_selected['CO_IES'].nunique()

# %%
unique_count_MUNIC = df_selected['CO_MUNICIPIO'].nunique()

# %%
unique_count_IES_UF = df_selected.groupby(['NO_REGIAO','SG_UF'])['CO_IES'].nunique()

# %%
unique_count_IES_UF

# %%
df_unique_count_IES_UF = unique_count_IES_UF.reset_index()


# %%
df_unique_count_IES_UF['Proportion'] = (df_unique_count_IES_UF['CO_IES'] / df_unique_count_IES_UF['CO_IES'].sum())*100

# %%
df_unique_count_IES_UF['Proportion'].sum()

# %%
df_unique_count_IES_UF

# %%
# Primeiro, calcule a soma de 'CO_IES' para cada 'NO_REGIAO'
sum_CO_IES_by_NO_REGIAO = df_unique_count_IES_UF.groupby('NO_REGIAO')['CO_IES'].sum()

# Em seguida, divida cada valor em 'CO_IES' pela soma correspondente em 'NO_REGIAO' e multiplique por 100
df_unique_count_IES_UF['Proportion_by_NO_REGIAO'] = df_unique_count_IES_UF.apply(lambda row: (row['CO_IES'] / sum_CO_IES_by_NO_REGIAO[row['NO_REGIAO']]) * 100, axis=1)

# %%
df_unique_count_IES_UF

# %%
df_unique_count_IES_UF = df_unique_count_IES_UF.rename(columns={
    'CO_IES': 'QTD_EscolasMed',
    'SG_UF': 'UF',
    'Proportion': 'ProporçãoBR',
    'Proportion_by_NO_REGIAO': 'Proporção_Região',
    'NO_REGIAO': 'REGIAO'
})

# %%
df_unique_count_IES_UF['ProporçãoBR'] = df_unique_count_IES_UF['ProporçãoBR'].round(0)
df_unique_count_IES_UF['Proporção_Região'] = df_unique_count_IES_UF['Proporção_Região'].round(0)

# %%
df_unique_count_IES_UF['ProporçãoBR'] = df_unique_count_IES_UF['ProporçãoBR'].astype(int)
df_unique_count_IES_UF['Proporção_Região'] = df_unique_count_IES_UF['Proporção_Região'].astype(int)

# %%
df_unique_count_IES_UF.info()

# %%
df_unique_count_IES_UF

# %%
df_unique_count_IES_UF.to_csv(r'D:\OneDrive\censo ensino superior\df_unique_count_IES_UF.csv')

# %%
df_unique_count_IES_UF

# %%
unique_counts = df_selected.nunique()

# %%
unique_counts

# %%
df_selected['TP_ORGANIZACAO_ACADEMICA']

# %%
df_selected['TP_ORGANIZACAO_ACADEMICA'].value_counts()

# %%


# %%


# %%
forecast_vg.to_csv(r'D:\OneDrive\censo ensino superior\forecast_vg.csv')

# %%
forecast_insc.to_csv(r'D:\OneDrive\censo ensino superior\forecast_insc.csv')

# %%
final_forecast.to_csv(r'D:\OneDrive\censo ensino superior\final_forecast.csv')

# %%
df_selected.to_csv(r'D:\OneDrive\censo ensino superior\df_selected.csv')


