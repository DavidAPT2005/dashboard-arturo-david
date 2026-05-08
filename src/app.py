import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Dashboard de Ventas - Arturo y David")

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

col1.metric("Ingresos Totales", f"${df['Ingreso'].sum():,.0f}")
col2.metric("Unidades Vendidas", f"{df['Unidades Vendidas'].sum():,.0f}")
col3.metric("Transacciones", len(df))
col4.metric("Ticket Promedio", f"${df['Ingreso'].mean():,.0f}")

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

ventas_producto = df.groupby("SKU")["Ingreso"].sum().reset_index()

fig1 = px.bar(
    ventas_producto,
    x="SKU",
    y="Ingreso",
    color="Ingreso",
    title="Ingresos por Producto"
)

col1.plotly_chart(fig1, use_container_width=True)

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

tienda_ingreso = df.groupby("IdTienda")["Ingreso"].sum().reset_index()

fig3 = px.bar(
    tienda_ingreso,
    x="IdTienda",
    y="Ingreso",
    color="Ingreso",
    title="Ingresos por Tienda"
)

col3.plotly_chart(fig3, use_container_width=True)

heatmap = df.groupby(["IdTienda", "SKU"])["Ingreso"].sum().reset_index()

fig4 = px.density_heatmap(
    heatmap,
    x="IdTienda",
    y="SKU",
    z="Ingreso",
    title="Relación Tienda - Producto"
)

col4.plotly_chart(fig4, use_container_width=True)

# ======================
# SOLO 4 PRODUCTOS
# ======================
productos_filtrados = [2005, 3006, 6050, 8500]
df_filtrado = df[df["SKU"].isin(productos_filtrados)]

# ======================
# PARETO (SIN LÍNEA)
# ======================
st.markdown("### Análisis de Pareto (Productos)")

pareto = df_filtrado.groupby("SKU")["Ingreso"].sum().reset_index()
pareto = pareto.sort_values(by="Ingreso", ascending=False)

fig_pareto = px.bar(
    pareto,
    x="SKU",
    y="Ingreso",
    title="Diagrama de Pareto"
)

st.plotly_chart(fig_pareto, use_container_width=True)

# ======================
# ABC (SOLO 4 PRODUCTOS)
# ======================
st.markdown("### Clasificación ABC")

pareto["Acumulado"] = pareto["Ingreso"].cumsum()
pareto["% Acumulado"] = 100 * pareto["Acumulado"] / pareto["Ingreso"].sum()

def clasificar(p):
    if p <= 80:
        return "A"
    elif p <= 95:
        return "B"
    else:
        return "C"

pareto["Clase"] = pareto["% Acumulado"].apply(clasificar)

fig_abc = px.bar(
    pareto,
    x="SKU",
    y="Ingreso",
    color="Clase",
    title="Clasificación ABC de Productos"
)

st.plotly_chart(fig_abc, use_container_width=True)

# ======================
# TENDENCIA (ARREGLADA)
# ======================
st.markdown("### Tendencia de Ventas")

df["Fecha"] = pd.to_datetime(df["Fecha"], format="%b-%y", errors="coerce")

tendencia = df.groupby("Fecha")["Ingreso"].sum().reset_index()
tendencia = tendencia.sort_values("Fecha")

fig_tendencia = px.line(
    tendencia,
    x="Fecha",
    y="Ingreso",
    markers=True,
    title="Evolución de Ventas"
)

st.plotly_chart(fig_tendencia, use_container_width=True)

# ======================
# GEOGRÁFICO
# ======================
st.markdown("### Análisis por Región")

geo = df.groupby("IdTienda")["Ingreso"].sum().reset_index()

fig_geo = px.bar(
    geo,
    x="IdTienda",
    y="Ingreso",
    color="Ingreso",
    title="Ventas por Región (Tienda)"
)

st.plotly_chart(fig_geo, use_container_width=True)

# ======================
# TABLA
# ======================
st.markdown("### Tabla de Datos")
st.dataframe(df)

# ======================
# INSIGHT
# ======================
top = pareto.iloc[0]

st.success(
    f"El producto con mayor ingreso es SKU {top['SKU']} con ${top['Ingreso']:,.0f}"
)