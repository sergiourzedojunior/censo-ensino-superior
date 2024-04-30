import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set the page title and layout
st.set_page_config(page_title="Vagas de Medicina por UF", layout="wide")


# Load the forecast data directly using pandas read_csv
final_forecast = pd.read_csv(r'D:\OneDrive\censo ensino superior\final_forecast.csv')

# Initialize a figure for Plotly
fig = go.Figure()

# Add the traces for each UF
for uf in final_forecast['SG_UF'].unique():
    filtered_forecast = final_forecast[final_forecast['SG_UF'] == uf]
    forecast_2023 = filtered_forecast[filtered_forecast['NU_ANO_CENSO'] == 2023]

    fig.add_trace(go.Scatter(
        x=filtered_forecast['NU_ANO_CENSO'],
        y=filtered_forecast['yhat_adjusted'].round(2),
        mode='lines+markers',
        name=f'{uf} Prediction'
    ))
    
    fig.add_trace(go.Scatter(
        x=filtered_forecast['NU_ANO_CENSO'],
        y=filtered_forecast['QT_VG_TOTAL'].round(2),
        mode='lines+markers',
        name=f'{uf} Actual'
    ))
    
    # Add a trace for the 2023 prediction
    if not forecast_2023.empty:
        fig.add_trace(go.Scatter(
            x=forecast_2023['NU_ANO_CENSO'],
            y=forecast_2023['yhat_adjusted'],
            mode='markers+text',
            text="Previsão 2023",
            textposition="top center",
            marker=dict(size=10, color='green'),
            name=f'{uf} Prediction 2023'
        ))

# Update the layout to include a dropdown for selecting UFs
button_layer_1_height = 1.12
uf_dropdown = final_forecast['SG_UF'].unique()
fig.update_layout(
    updatemenus=[
        go.layout.Updatemenu(
            buttons=list([
                dict(
                    args=[{"visible": [uf == k for uf in uf_dropdown for k in uf_dropdown]}],
                    label=f"{k}",
                    method="update"
                ) for k in uf_dropdown
            ]),
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0,
            xanchor="left",
            y=button_layer_1_height,
            yanchor="top"
        ),
    ]
)

# Configure the rest of the layout
fig.update_layout(
    title='Adjusted Prediction and Real Values by UF',
    xaxis_title='Year',
    yaxis_title='Values',
    legend_title='Series',
    hovermode='closest'
)

# Remove the deprecated caching message
st.set_option('deprecation.showPyplotGlobalUse', False)

# Display the figure in the Streamlit app
st.plotly_chart(fig, use_container_width=True)
