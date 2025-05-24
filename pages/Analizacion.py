import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(   
    page_icon="📌",
    layout="wide"
)

st.title("Analización de Datos")

st.header("Descripción")
st.markdown("""
En este trabajo, se emplearon los conocimientos adquiridos hasta el momento 2 para crear un DataFrame 
utilizando streamlit y la biblioteca pandas. A parte de que se usan graficas para visualizar los resultados 
descargados de una base de datos libre de Colombia.
""")

st.markdown("Primeros pasos de Dataframes")

df = pd.read_csv("static/dataset/Noticias_criminales_Inz__-_Datos_Abiertos_20250524.csv")

if st.checkbox("Mostrar datos completos"):
    st.dataframe(df)

st.sidebar.header("Filtros")

df_filtrado = df.copy()

# Limpiar columnas clave
df["ESTADO_NOTICIA"] = df["ESTADO_NOTICIA"].str.upper().str.strip()
df["ETAPA"] = df["ETAPA"].str.upper().str.strip()
df["DELITO"] = df["DELITO"].str.upper().str.strip()
df["CONDENA"] = df["CONDENA"].str.upper().str.strip()
df["MUNICIPIO"] = df["MUNICIPIO"].str.upper().str.strip()

# Filtro por Estado de la Noticia
estados = df["ESTADO_NOTICIA"].dropna().unique().tolist()
estado_seleccionado = st.sidebar.multiselect("Selecciona Estado de la Noticia", sorted(estados), default=estados)

# Filtro por Etapa
etapas = df["ETAPA"].dropna().unique().tolist()
etapa_seleccionada = st.sidebar.multiselect("Selecciona Etapa", sorted(etapas), default=etapas)

# Filtro por Delito
delitos = df["DELITO"].dropna().unique().tolist()
delito_seleccionado = st.sidebar.multiselect("Selecciona Delitos", sorted(delitos), default=delitos)

# Filtro por Condena
condenas = df["CONDENA"].dropna().unique().tolist()
condena_seleccionada = st.sidebar.multiselect("¿Hubo Condena?", sorted(condenas), default=condenas)

# Filtro por Municipio (opcional si tienes más de uno)
municipios = df["MUNICIPIO"].dropna().unique().tolist()
municipio_seleccionado = st.sidebar.multiselect("Selecciona Municipio", sorted(municipios), default=municipios)

# Asegurarse de que TOTAL_PROCESOS es numérico
df["TOTAL_PROCESOS"] = pd.to_numeric(df["TOTAL_PROCESOS"], errors="coerce")

# Crear slider de rango de procesos
min_procesos = int(df["TOTAL_PROCESOS"].min())
max_procesos = int(df["TOTAL_PROCESOS"].max())

rango_procesos = st.sidebar.slider(
    "Selecciona el rango de Total de Procesos",
    min_value=min_procesos,
    max_value=max_procesos,
    value=(min_procesos, max_procesos)
)

# Filtrar por TOTAL_PROCESOS
df_filtrado = df_filtrado[
    (df_filtrado["TOTAL_PROCESOS"] >= rango_procesos[0]) &
    (df_filtrado["TOTAL_PROCESOS"] <= rango_procesos[1])
]

# Aplicar filtros al DataFrame original
df_filtrado = df[
    (df["ESTADO_NOTICIA"].isin(estado_seleccionado)) &
    (df["ETAPA"].isin(etapa_seleccionada)) &
    (df["DELITO"].isin(delito_seleccionado)) &
    (df["CONDENA"].isin(condena_seleccionada)) &
    (df["MUNICIPIO"].isin(municipio_seleccionado))
]

st.subheader("📊 Procesos por Estado y Condena")

# Asegurar que los textos estén limpios
df["ESTADO_NOTICIA"] = df_filtrado["ESTADO_NOTICIA"].str.upper().str.strip()
df["CONDENA"] = df_filtrado["CONDENA"].str.upper().str.strip()

# Agrupar datos
estado_condena_df = df_filtrado.groupby(["ESTADO_NOTICIA", "CONDENA"]).size().reset_index(name="Cantidad")

# Crear gráfico
fig_estado_condena = px.bar(
    estado_condena_df,
    x="ESTADO_NOTICIA",
    y="Cantidad",
    color="CONDENA",
    barmode="group",
    title="Cantidad de Procesos por Estado y Condena",
    labels={"ESTADO_NOTICIA": "Estado de la Noticia", "Cantidad": "Número de Procesos", "CONDENA": "Condena"}
)

st.plotly_chart(fig_estado_condena)

st.subheader("🔍 Etapas Judiciales por Estado de la Noticia")

# Limpiar texto
etapas = ["CAPTURA", "IMPUTACION", "ACUSACION", "CONDENA"]
df["ESTADO_NOTICIA"] = df_filtrado["ESTADO_NOTICIA"].str.upper().str.strip()
for etapa in etapas:
    df_filtrado[etapa] = df_filtrado[etapa].str.upper().str.strip()

# Reorganizar los datos en formato largo
df_etapas = df_filtrado.melt(id_vars=["ESTADO_NOTICIA"], value_vars=etapas,
                    var_name="Etapa", value_name="Resultado")

# Contar por estado y etapa (solo SI / NO)
etapas_estado_df = df_etapas[df_etapas["Resultado"].isin(["SI", "NO"])].groupby(
    ["ESTADO_NOTICIA", "Etapa", "Resultado"]
).size().reset_index(name="Cantidad")

# Crear gráfico
import plotly.express as px
fig_etapas_estado = px.bar(
    etapas_estado_df,
    x="Etapa",
    y="Cantidad",
    color="Resultado",
    facet_col="ESTADO_NOTICIA",
    barmode="group",
    title="Procesos por Etapa Judicial según Estado de la Noticia",
    labels={"Cantidad": "Número de Procesos", "Resultado": "Resultado de la Etapa"}
)

st.plotly_chart(fig_etapas_estado)

st.subheader("🥧 Distribución de Procesos por Etapa")

# Limpiar texto
df["ETAPA"] = df_filtrado["ETAPA"].str.upper().str.strip()

# Agrupar datos
etapa_counts = df_filtrado["ETAPA"].value_counts().reset_index()
etapa_counts.columns = ["Etapa", "Cantidad"]

# Crear gráfico de pastel
import plotly.express as px
fig_pie_etapa = px.pie(
    etapa_counts,
    names="Etapa",
    values="Cantidad",
    title="Distribución de Procesos por Etapa Judicial",
    hole=0.3  # Si quieres un gráfico tipo 'donut'
)

st.plotly_chart(fig_pie_etapa)

