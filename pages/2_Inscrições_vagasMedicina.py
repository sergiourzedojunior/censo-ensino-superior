import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np  # Required for calculations involving arrays

# Setting the page configuration
st.set_page_config(page_title="Inscrições e vagas de Medicina", layout="wide")

# Function to load data
def load_data(filepath):
    return pd.read_csv(filepath)

# Function to create a plotly graph for grouped data with dual y-axes
def create_grouped_plot(df):
    # Create figure with secondary y-axis
    fig = go.Figure()

    # Add traces
    fig.add_trace(go.Scatter(x=df['NU_ANO_CENSO'], y=df['QT_INSCRITO_TOTAL'],
                             mode='lines+markers',
                             name='Total Inscriptions',
                             marker=dict(color='blue')))

    fig.add_trace(go.Scatter(x=df['NU_ANO_CENSO'], y=df['QT_VG_TOTAL'],
                             mode='lines+markers',
                             name='Total Vacancies',
                             marker=dict(color='red'),
                             yaxis='y2'))  # Set this trace to use the secondary y-axis

    # Layout
    fig.update_layout(
        title='Grouped Data Overview with Dual Axis',
        xaxis_title='Year',
        yaxis=dict(
            title='Total Inscriptions',
            titlefont=dict(color='blue'),
            tickfont=dict(color='blue')
        ),
        yaxis2=dict(
            title='Total Vacancies',
            titlefont=dict(color='red'),
            tickfont=dict(color='red'),
            overlaying='y',
            side='right'
        )
    )
    return fig


# Function to create a plotly graph for predictions with growth rates
def create_prediction_plot(df, title, x_col, y_col='yhat', actual_col='y', growth_rate_col='predicted_growth_rate', actual_growth_rate_col='actual_growth_rate'):
    fig = go.Figure()
    if y_col in df.columns and actual_col in df.columns:
        # Predicted data
        fig.add_trace(go.Scatter(x=df[x_col], y=df[y_col],
                                 mode='lines+markers',
                                 name='Predicted',
                                 customdata=np.stack((df[actual_col], df[growth_rate_col]), axis=-1),
                                 hovertemplate="<b>%{x}</b><br><br>Predicted: %{y:.2f}<br>Actual: %{customdata[0]:.2f}<br>Predicted Growth Rate: %{customdata[1]:.2%}<extra></extra>"))
        
        # Actual data
        fig.add_trace(go.Scatter(x=df[x_col], y=df[actual_col],
                                 mode='lines+markers',
                                 name='Actual',
                                 customdata=np.stack((df[y_col], df[actual_growth_rate_col]), axis=-1),
                                 hovertemplate="<b>%{x}</b><br><br>Actual: %{y:.2f}<br>Predicted: %{customdata[0]:.2f}<br>Actual Growth Rate: %{customdata[1]:.2%}<extra></extra>"))
    else:
        st.error(f"Missing columns in DataFrame for {title}. Expected '{y_col}' and '{actual_col}'.")
    fig.update_layout(title=title,
                      xaxis_title='Year',
                      yaxis_title='Counts',
                      template='plotly_dark')
    return fig


# Load data
df_grouped_reset = load_data('D:/OneDrive/censo ensino superior/df_grouped_reset.csv')
df_insc = load_data('D:/OneDrive/censo ensino superior/forecast_insc.csv')
df_vg = load_data('D:/OneDrive/censo ensino superior/forecast_vg.csv')

# Calculating growth rates for both vacancy and inscription data
df_vg['actual_growth_rate'] = df_vg['y'].pct_change()
df_vg['predicted_growth_rate'] = df_vg['yhat'].pct_change()
df_insc['actual_growth_rate'] = df_insc['y'].pct_change()
df_insc['predicted_growth_rate'] = df_insc['yhat'].pct_change()

# Update selection based on date
df_vg_until_2022 = df_vg[df_vg['ds'] <= '2022-12-31']
df_vg_2023 = df_vg[df_vg['ds'] > '2022-12-31']
df_insc_until_2022 = df_insc[df_insc['ds'] <= '2022-12-31']
df_insc_2023 = df_insc[df_insc['ds'] > '2022-12-31']

# Creating the plots
fig_grouped_reset = create_grouped_plot(df_grouped_reset)
fig_vg = create_prediction_plot(df_vg, 'Vacancy Predictions Overview with Growth Rates', 'ds', 'yhat', 'y')
fig_insc = create_prediction_plot(df_insc, 'Inscription Predictions Overview with Growth Rates', 'ds', 'yhat', 'y')

# Displaying the plots in Streamlit

st.title('Education Data Dashboard - Medical Courses 🩺')
st.header('Grouped Data Overview')
st.plotly_chart(fig_grouped_reset, use_container_width=True)
st.header('Inscription Predictions Overview')
st.plotly_chart(fig_insc, use_container_width=True)
st.header('Vacancy Predictions Overview')
st.plotly_chart(fig_vg, use_container_width=True)
