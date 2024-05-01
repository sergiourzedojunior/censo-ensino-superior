import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Vagas de Medicina por UF", layout="wide")

# Load the forecast data
final_forecast = pd.read_csv(r'D:\OneDrive\censo ensino superior\final_forecast.csv')

# Update the rolling average on the DataFrame for all years and round off
final_forecast['rolling_yhat_adjusted'] = final_forecast.groupby('SG_UF')['yhat_adjusted'].transform(
    lambda x: x.rolling(window=3, min_periods=1).mean()).round(2)

# Calculate a two-year rolling average only for the last entry (assuming it's for 2023) and round off
window_size = 2
final_forecast['MA_yhat_adjusted'] = final_forecast.groupby('SG_UF')['yhat_adjusted'].transform(
    lambda x: x.rolling(window=window_size, min_periods=1).mean()).round(2)

# Filter to keep only the most recent entries per UF, assuming it's from 2023
latest_forecasts = final_forecast.drop_duplicates(subset=['SG_UF'], keep='last')

fig = go.Figure()

uf_dropdown = final_forecast['SG_UF'].unique()
for uf in uf_dropdown:
    filtered_df = final_forecast[final_forecast['SG_UF'] == uf]
    latest_data = latest_forecasts[latest_forecasts['SG_UF'] == uf]

    fig.add_trace(go.Scatter(
        x=filtered_df['NU_ANO_CENSO'],
        y=filtered_df['rolling_yhat_adjusted'],
        mode='lines+markers',
        name=f'{uf} Prediction'
    ))

    fig.add_trace(go.Scatter(
        x=filtered_df['NU_ANO_CENSO'],
        y=filtered_df['QT_VG_TOTAL'],
        mode='lines+markers',
        name=f'{uf} Actual'
    ))

    # Ensure that the 2023 forecast appears in the year 2023
    if not latest_data.empty:
        fig.add_trace(go.Scatter(
            x=[latest_data['NU_ANO_CENSO'].values[0] + 1],  # Make sure this reflects 2023
            y=latest_data['MA_yhat_adjusted'],
            mode='markers',
            marker=dict(size=10, color='green'),
            name=f'{uf} Forecast 2023'
        ))

# Create filter buttons for each UF in the dropdown
buttons = [dict(label='All',
                method='update',
                args=[{'visible': [True] * len(uf_dropdown) * 3},
                      {'title': 'Vacancies - Adjusted Forecast and Real Values by UF'}])]
for i, uf in enumerate(uf_dropdown):
    visibility = [False] * len(uf_dropdown) * 3
    visibility[i * 3:(i + 1) * 3] = [True, True, True]  # Visibility for forecast, real, and forecast 2023
    buttons.append(dict(label=uf,
                        method='update',
                        args=[{'visible': visibility},
                              {'title': f'Vacancies - Forecast and Real Values for {uf}'}]))

# Update the graph layout with the dropdown and style details
fig.update_layout(
    title='Vacancies - Adjusted Forecast and Real Values by UF',
    xaxis_title='Year',
    yaxis_title='Values',
    legend_title='Series',
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


# Displaying the plots in Streamlit

st.title('Education Data Dashboard - Medical Courses 🩺')
st.header('Grouped Data Overview - State Vacancies')
st.plotly_chart(fig, use_container_width=True)