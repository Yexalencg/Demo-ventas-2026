import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# 1. CONFIGURACIÓN DE LA PÁGINA (Debe ser lo primero)
st.set_page_config(layout='wide', page_title="Dashboard Estratégico de Ventas")

# 2. DICCIONARIO DE ESTADOS (Para que el mapa funcione con nombres completos o códigos)
us_state_to_abbrev = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO",
    "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
    "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
    "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"
}

# 3. CARGA DE DATOS
@st.cache_data
def load_data():
    # Ruta relativa para que funcione en GitHub/Streamlit Cloud
    file_path = 'datosII/SalidaVentas.xlsx' 
    df = pd.read_excel(file_path)
    if 'Order Date' in df.columns:
        df['Order Date'] = pd.to_datetime(df['Order Date'])
    # Limpiamos espacios en blanco en los nombres de estados
    if 'State' in df.columns:
        df['State'] = df['State'].str.strip()
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error al cargar el archivo: {e}")
    st.stop()

# 4. TÍTULO Y FILTROS EN SIDEBAR
st.title('📊 Dashboard de Análisis de Ventas')

st.sidebar.header('Filtros de Control')

# Filtro de Región
all_regions = ['Todas'] + list(df['Region'].unique())
selected_region = st.sidebar.selectbox('Selecciona una Región', all_regions)

filtered_df = df.copy()
if selected_region != 'Todas':
    filtered_df = df[df['Region'] == selected_region]

# Filtro de Fechas
min_date = df['Order Date'].min().to_pydatetime()
max_date = df['Order Date'].max().to_pydatetime()
start_date, end_date = st.sidebar.date_input('Rango de fechas', [min_date, max_date])

filtered_df = filtered_df[(filtered_df['Order Date'].dt.date >= start_date) & 
                           (filtered_df['Order Date'].dt.date <= end_date)]

# Filtro de Categoría (Multiselect)
all_cats = df['Category'].unique().tolist()
selected_cats = st.sidebar.multiselect('Categorías', options=all_cats, default=all_cats)
if selected_cats:
    filtered_df = filtered_df[filtered_df['Category'].isin(selected_cats)]

# 5. MÉTRICAS CLAVE
st.subheader('Resultados Generales')
c1, c2, c3 = st.columns(3)
c1.metric('Ventas Totales', f'${filtered_df["Sales"].sum():,.2f}')
c2.metric('Ganancia Total', f'${filtered_df["Profit"].sum():,.2f}')
c3.metric('N° de Pedidos', len(filtered_df))

# 6. GRÁFICAS (3 gráficas requeridas)
col_a, col_b = st.columns(2)

with col_a:
    st.subheader('Ventas por Región')
    sales_reg = filtered_df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
    fig1, ax1 = plt.subplots()
    sns.barplot(x=sales_reg.index, y=sales_reg.values, palette='viridis', ax=ax1)
    st.pyplot(fig1)

with col_b:
    st.subheader('Ventas por Categoría')
    sales_cat = filtered_df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
    fig2, ax2 = plt.subplots()
    sns.barplot(x=sales_cat.index, y=sales_cat.values, palette='magma', ax=ax2)
    st.pyplot(fig2)

# Gráfica 3: Evolución Temporal (Corregido 'ME')
st.subheader('📈 Evolución de Ventas Mensuales')
sales_time = filtered_df.set_index('Order Date').resample('ME')['Sales'].sum().reset_index()
fig3, ax3 = plt.subplots(figsize=(12,4))
sns.lineplot(data=sales_time, x='Order Date', y='Sales', marker='o', ax=ax3)
st.pyplot(fig3)

# 7. MAPA (Requisito)
st.subheader('🌍 Distribución Geográfica por Estado')
sales_state = filtered_df.groupby('State')['Sales'].sum().reset_index()

# Convertimos nombres a códigos de 2 letras para que Plotly los reconozca
sales_state['State_Code'] = sales_state['State'].map(us_state_to_abbrev).fillna(sales_state['State'])

fig_map = px.choropleth(
    sales_state, 
    locations='State_Code', 
    locationmode='USA-states', 
    color='Sales', 
    scope='usa', 
    color_continuous_scale='YlGnBu'
)
st.plotly_chart(fig_map, use_container_width=True)

# 8. DATAFRAME CON FILTRO (Requisito)
st.write("### Tabla de Datos Detallada")
st.dataframe(filtered_df)
