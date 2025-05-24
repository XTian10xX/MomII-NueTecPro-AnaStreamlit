import pandas as pd
import streamlit as st

# Cargar el dataset
df = pd.read_csv("static/datasets/estudiantes_colombia.csv")

# Mostrar las primeras 5 filas
st.subheader("Primeras 5 filas del dataset")
st.write(df.head())

# Mostrar las últimas 3 filas
st.subheader("Últimas 3 filas del dataset")
st.write(df.tail(3))

# Información general del dataset
st.subheader("Información del dataset")
st.text(df.info())  # Nota: .info() imprime en consola, usamos st.text para verlo en Streamlit

# Estadísticas descriptivas
st.subheader("Estadísticas descriptivas")
st.write(df.describe())

# Selección de columnas
st.subheader("Selección de columnas: Ciudad y Edad")
st.write(df[['ciudad', 'edad']])

# Filtrado de filas por edad mayor a 3
st.subheader("Estudiantes mayores de 18 años")
st.write(df[df['edad'] > 18])

# Menú interactivo
opcion = st.selectbox("¿Qué quieres explorar?", 
                      ["Primeras filas", "Estadísticas", "Filtrar por edad"])

if opcion == "Primeras filas":
    st.write(df.head())
elif opcion == "Estadísticas":
    st.write(df.describe())
elif opcion == "Filtrar por edad":
    edad_min = st.slider("Edad mínima", 0, 7, 2)
    st.write(df[df['edad'] >= edad_min])