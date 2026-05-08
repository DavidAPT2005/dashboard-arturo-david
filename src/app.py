import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Dashboard Arturo y David")

# ======================
# DATA
# ======================
df = pd.read_csv("public/ventas.csv")

df["Ingreso"] = pd.to_numeric(df["Ingreso"], errors="coerce")
df["Unidades Vendidas"] = pd.to_numeric(df["Unidades Vendidas"], errors="coerce")

# ======================
# KPIs
# ======================
col1, col2, col3, col4 = st.columns(4)

col1.metric(" Ingresos Totales", f"${df['Ingreso'].sum():,.0f}")
col2.metric(" Unidades", f"{df['Unidades Vendidas'].sum():,.0f}")
col3.metric(" Transacciones", len(df))
col4.metric(" Ticket Promedio", f"${df['Ingreso'].mean():,.0f}")

st.markdown("---")

# ======================
# FILTRO
# ======================
tienda = st.sidebar.multiselect(
    "Filtrar por tienda",
    df["IdTienda"].unique(),
    default=df["IdTienda"].unique()
)

df = df[df["IdTienda"].isin(tienda)]

# ======================
# FILA 1
# ======================
col1, col2 = st.columns(2)

# INGRESO POR PRODUCTO
ventas_producto = df.groupby("SKU")["Ingreso"].sum().reset_index()

fig1 = px.bar(
    ventas_producto,
    x="SKU",
    y="Ingreso",
    color="Ingreso",
    title="Ingresos por Producto",
)

col1.plotly_chart(fig1, use_container_width=True)

# TIPOS DE VENTA
tipo = df["Tipo de venta"].value_counts().reset_index()
tipo.columns = ["Tipo", "Cantidad"]

fig2 = px.pie(
    tipo,
    names="Tipo",
    values="Cantidad",
    title="Distribución de Tipos de Venta"
)

col2.plotly_chart(fig2, use_container_width=True)

# ======================
# FILA 2
# ======================
col3, col4 = st.columns(2)

# INGRESO POR TIENDA
tienda_ingreso = df.groupby("IdTienda")["Ingreso"].sum().reset_index()

fig3 = px.bar(
    tienda_ingreso,
    x="IdTienda",
    y="Ingreso",
    color="Ingreso",
    title="Ingresos por Tienda"
)

col3.plotly_chart(fig3, use_container_width=True)

# HEATMAP TIENDA vs SKU
heatmap = df.groupby(["IdTienda", "SKU"])["Ingreso"].sum().reset_index()

fig4 = px.density_heatmap(
    heatmap,
    x="IdTienda",
    y="SKU",
    z="Ingreso",
    title="Relación Tienda - Producto (Heatmap)"
)

col4.plotly_chart(fig4, use_container_width=True)

# ======================
# FILA 3
# ======================
col5, col6 = st.columns(2)

# TOP PRODUCTOS
top_productos = ventas_producto.sort_values(by="Ingreso", ascending=False).head(10)

fig5 = px.bar(
    top_productos,
    x="SKU",
    y="Ingreso",
    title="Top 10 Productos"
)

col5.plotly_chart(fig5, use_container_width=True)

# UNIDADES POR PRODUCTO
unidades_producto = df.groupby("SKU")["Unidades Vendidas"].sum().reset_index()

fig6 = px.line(
    unidades_producto,
    x="SKU",
    y="Unidades Vendidas",
    markers=True,
    title="Unidades Vendidas por Producto"
)

col6.plotly_chart(fig6, use_container_width=True)

# ======================
# TABLA
# ======================
st.markdown("### 📋 Tabla de Datos")

st.dataframe(df)

# ======================
# INSIGHT AUTOMÁTICO
# ======================
top = ventas_producto.sort_values(by="Ingreso", ascending=False).iloc[0]

st.success(
    f"El producto más rentable es SKU {top['SKU']} con ingresos de ${top['Ingreso']:,.0f}"
)