# ... (Partes anteriores de carga de datos y filtros se mantienen igual)

# 5. MÉTRICAS CLAVE
st.subheader('Resultados Generales')
c1, c2, c3 = st.columns(3)
c1.metric('Ventas Totales', f'${filtered_df["Sales"].sum():,.2f}')
c2.metric('Ganancia Total', f'${filtered_df["Profit"].sum():,.2f}')
c3.metric('N° de Pedidos', len(filtered_df))

# --- CAMBIO DE ORDEN: MAPA PRIMERO ---
st.subheader('Mapa de Ventas Regionales')
sales_state = filtered_df.groupby('State')['Sales'].sum().reset_index()
sales_state['State_Code'] = sales_state['State'].map(us_state_to_abbrev).fillna(sales_state['State'])

fig_map = px.choropleth(
    sales_state, 
    locations='State_Code', 
    locationmode='USA-states', 
    color='Sales', 
    scope='usa', 
    # CAMBIO DE COLOR: Escala de rojos a amarillos
    color_continuous_scale='YlOrRd' 
)
st.plotly_chart(fig_map, use_container_width=True)

# --- SEGUNDA FILA: GRÁFICAS DE BARRAS ---
col_a, col_b = st.columns(2)

with col_a:
    st.subheader('Ventas por Región')
    sales_reg = filtered_df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
    fig1, ax1 = plt.subplots()
    # CAMBIO DE COLOR: Paleta personalizada o fija
    sns.barplot(x=sales_reg.index, y=sales_reg.values, palette='Blues_r', ax=ax1)
    st.pyplot(fig1)

with col_b:
    st.subheader('Categorías más vendidas')
    sales_cat = filtered_df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
    fig2, ax2 = plt.subplots()
    # CAMBIO DE COLOR: Paleta 'Greens_d'
    sns.barplot(x=sales_cat.index, y=sales_cat.values, palette='flare', ax=ax2)
    st.pyplot(fig2)

# --- ÚLTIMA FILA: EVOLUCIÓN ---
st.subheader('Ventas a lo largo del tiempo')
sales_time = filtered_df.set_index('Order Date').resample('ME')['Sales'].sum().reset_index()
fig3, ax3 = plt.subplots(figsize=(12,4))
# CAMBIO DE COLOR: Color de línea específico
sns.lineplot(data=sales_time, x='Order Date', y='Sales', marker='o', color='#E67E22', ax=ax3)
st.pyplot(fig3)
