import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_icon="📌", layout="wide")
st.title("Analización de Datos")

st.header("Descripción")
st.markdown("""
Este trabajo utiliza Streamlit y Pandas para visualizar datos judiciales de Colombia con filtros dinámicos.
""")

# Cargar datos
df = pd.read_csv("static/dataset/Noticias_criminales_Inz__-_Datos_Abiertos_20250524.csv")

# Limpiar columnas clave
for col in ["ESTADO_NOTICIA", "ETAPA", "DELITO", "CONDENA", "MUNICIPIO"]:
    df[col] = df[col].astype(str).str.upper().str.strip()

# Asegurar que TOTAL_PROCESOS sea numérico
df["TOTAL_PROCESOS"] = pd.to_numeric(df["TOTAL_PROCESOS"], errors="coerce")

# Mostrar datos completos
if st.checkbox("Mostrar datos completos"):
    st.dataframe(df)

# Sidebar - Filtros
st.sidebar.header("Filtros")

estado_seleccionado = st.sidebar.multiselect("Selecciona Estado de la Noticia", sorted(df["ESTADO_NOTICIA"].dropna().unique()), default=df["ESTADO_NOTICIA"].unique())
etapa_seleccionada = st.sidebar.multiselect("Selecciona Etapa", sorted(df["ETAPA"].dropna().unique()), default=df["ETAPA"].unique())
delito_seleccionado = st.sidebar.multiselect("Selecciona Delitos", sorted(df["DELITO"].dropna().unique()), default=df["DELITO"].unique())
condena_seleccionada = st.sidebar.multiselect("¿Hubo Condena?", sorted(df["CONDENA"].dropna().unique()), default=df["CONDENA"].unique())
municipio_seleccionado = st.sidebar.multiselect("Selecciona Municipio", sorted(df["MUNICIPIO"].dropna().unique()), default=df["MUNICIPIO"].unique())

rango_procesos = st.sidebar.slider(
    "Selecciona el rango de Total de Procesos",
    min_value=int(df["TOTAL_PROCESOS"].min()),
    max_value=int(df["TOTAL_PROCESOS"].max()),
    value=(int(df["TOTAL_PROCESOS"].min()), int(df["TOTAL_PROCESOS"].max()))
)

# Aplicar filtros
df_filtrado = df[
    (df["ESTADO_NOTICIA"].isin(estado_seleccionado)) &
    (df["ETAPA"].isin(etapa_seleccionada)) &
    (df["DELITO"].isin(delito_seleccionado)) &
    (df["CONDENA"].isin(condena_seleccionada)) &
    (df["MUNICIPIO"].isin(municipio_seleccionado)) &
    (df["TOTAL_PROCESOS"] >= rango_procesos[0]) &
    (df["TOTAL_PROCESOS"] <= rango_procesos[1])
]

### 📊 Gráfico 1: Procesos por Estado y Condena
st.subheader("📊 Procesos por Estado y Condena")

estado_condena_df = df_filtrado.groupby(["ESTADO_NOTICIA", "CONDENA"]).size().reset_index(name="Cantidad")
fig_estado_condena = px.bar(
    estado_condena_df,
    x="ESTADO_NOTICIA",
    y="Cantidad",
    color="CONDENA",
    barmode="group",
    title="Cantidad de Procesos por Estado y Condena"
)
st.plotly_chart(fig_estado_condena, use_container_width=True)

### 🔍 Gráfico 2: Etapas Judiciales por Estado de la Noticia
st.subheader("🔍 Etapas Judiciales por Estado de la Noticia")

etapas = ["CAPTURA", "IMPUTACION", "ACUSACION", "CONDENA"]
for etapa in etapas:
    if etapa in df_filtrado.columns:
        df_filtrado[etapa] = df_filtrado[etapa].astype(str).str.upper().str.strip()

df_etapas = df_filtrado.melt(id_vars=["ESTADO_NOTICIA"], value_vars=etapas,
                              var_name="Etapa", value_name="Resultado")
etapas_estado_df = df_etapas[df_etapas["Resultado"].isin(["SI", "NO"])].groupby(
    ["ESTADO_NOTICIA", "Etapa", "Resultado"]
).size().reset_index(name="Cantidad")

fig_etapas_estado = px.bar(
    etapas_estado_df,
    x="Etapa",
    y="Cantidad",
    color="Resultado",
    facet_col="ESTADO_NOTICIA",
    barmode="group",
    title="Procesos por Etapa Judicial según Estado de la Noticia"
)
st.plotly_chart(fig_etapas_estado, use_container_width=True)

### 🥧 Gráfico 3: Distribución de Procesos por Etapa
st.subheader("🥧 Distribución de Procesos por Etapa")

etapa_counts = df_filtrado["ETAPA"].value_counts().reset_index()
etapa_counts.columns = ["Etapa", "Cantidad"]

fig_pie_etapa = px.pie(
    etapa_counts,
    names="Etapa",
    values="Cantidad",
    title="Distribución de Procesos por Etapa Judicial",
    hole=0.3
)
st.plotly_chart(fig_pie_etapa, use_container_width=True)

### 📈 Gráfico 4: Top 10 Delitos por Procesos
st.subheader("📈 Top 10 Delitos por Procesos")

delitos_procesos = df_filtrado.groupby("DELITO")["TOTAL_PROCESOS"].sum().reset_index()
delitos_procesos = delitos_procesos.sort_values("TOTAL_PROCESOS", ascending=False).head(10)

fig_delitos = px.bar(
    delitos_procesos,
    x="DELITO",
    y="TOTAL_PROCESOS",
    title="Top 10 Delitos por Cantidad de Procesos",
    color="TOTAL_PROCESOS",
    color_continuous_scale="Reds"
)

st.plotly_chart(fig_delitos, use_container_width=True)