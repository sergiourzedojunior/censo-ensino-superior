import streamlit as st
import pandas as pd
import plotly.graph_objects as go


st.set_page_config(page_title="Inscrições e vagas de Medicina", layout="wide")
# Function to load data
def load_data(filepath):
    return pd.read_csv(filepath)

# Function to create a plotly graph for grouped data reset
def create_grouped_plot(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['NU_ANO_CENSO'], y=df['QT_VG_TOTAL'],
                             mode='lines+markers',
                             name='Total Vacancies'))
    fig.add_trace(go.Scatter(x=df['NU_ANO_CENSO'], y=df['QT_INSCRITO_TOTAL'],
                             mode='lines+markers',
                             name='Total Inscriptions'))
    fig.update_layout(title='Grouped Data Overview',
                      xaxis_title='Year',
                      yaxis_title='Counts')
    return fig

# Function to create a plotly graph for predictions
def create_prediction_plot(df, title, x_col, y_col='yhat', actual_col='y'):
    fig = go.Figure()
    if y_col in df.columns and actual_col in df.columns:
        fig.add_trace(go.Scatter(x=df[x_col], y=df[y_col],
                                 mode='lines+markers',
                                 name='Predicted'))
        fig.add_trace(go.Scatter(x=df[x_col], y=df[actual_col],
                                 mode='lines+markers',
                                 name='Actual'))
    else:
        st.error(f"Missing columns in DataFrame for {title}. Expected '{y_col}' and '{actual_col}'.")
    fig.update_layout(title=title,
                      xaxis_title='Year',
                      yaxis_title='Counts')
    return fig

# Streamlit layout
st.title('Education Data Dashboard')

# Load the data
df_grouped_reset = load_data(r'D:\OneDrive\censo ensino superior\df_grouped_reset.csv')
df_insc = load_data(r'D:\OneDrive\censo ensino superior\forecast_insc.csv')
df_vg = load_data(r'D:\OneDrive\censo ensino superior\forecast_vg.csv')

# Creating the plots
fig_grouped_reset = create_grouped_plot(df_grouped_reset)
fig_insc = create_prediction_plot(df_insc, 'Inscription Predictions Overview', x_col='ds', y_col='yhat', actual_col='y')
fig_vg = create_prediction_plot(df_vg, 'Vacancy Predictions Overview', x_col='ds', y_col='yhat', actual_col='y')

# Displaying the plots in Streamlit
st.header('Grouped Data Overview')
st.plotly_chart(fig_grouped_reset, use_container_width=True)

st.header('Inscription Predictions Overview')
st.plotly_chart(fig_insc, use_container_width=True)

st.header('Vacancy Predictions Overview')
st.plotly_chart(fig_vg, use_container_width=True)
