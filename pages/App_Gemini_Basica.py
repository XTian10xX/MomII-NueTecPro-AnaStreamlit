# import streamlit as st
# import google.generativeai as genai
# import pandas as pd
# from datetime import datetime, timedelta

# genai.configure(api_key="AIzaSyAcKoa5G10uwHLc1zR-IUkTomOOAdg3_kE")

# st.set_page_config(page_title="📅 Asistente Personal con Agenda", layout="centered")
# st.title("🧠 Tu Asistente con Gemini")
# st.markdown("Puedes escribir cualquier cosa: preguntas generales, pedir consejos o que te organice tu semana.")

# #Entrada del usuario
# modo = st.selectbox("Selecciona el modo de asistencia:", ["Chat General", "Organizar mi semana"])
# entrada = st.text_area("💭 Escribe tu mensaje o actividades:", height=200)
# generar = st.button("Generar Respuesta")

# # Funciones

# def generar_chat(prompt):
#     model = genai.GenerativeModel("gemini-1.5-flash")
#     respuesta = model.generate_content(prompt)
#     return respuesta.text

# def generar_agenda(actividades):
#     prompt = (
#         f"Tengo estas actividades esta semana: {actividades}. "
#         "Organiza mi semana de lunes a domingo con horarios aproximados y descansos. "
#         "Devuélvemelo como lista estructurada."
#     )
#     respuesta = generar_chat(prompt)
#     return respuesta

# def extraer_eventos_a_dataframe(respuesta_texto):
#     dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
#     eventos = []
#     dia_actual = ""

#     for linea in respuesta_texto.splitlines():
#         linea = linea.strip()
#         if any(dia in linea.lower() for dia in dias):
#             dia_actual = linea.strip(":")
#         elif linea:
#             eventos.append({"Día": dia_actual.capitalize(), "Actividad": linea})

#     return pd.DataFrame(eventos)

# # Mostrar resultado
# if generar and entrada:
#     with st.spinner("Generando con Gemini..."):
#         if modo == "Chat General":
#             respuesta = generar_chat(entrada)
#             st.subheader("🔊 Respuesta:")
#             st.markdown(respuesta)
#         elif modo == "Organizar mi semana":
#             respuesta = generar_agenda(entrada)
#             st.subheader("🗓️ Agenda Generada:")
#             st.markdown(respuesta)
#             st.subheader("Calendario Interactivo:")
#             df_eventos = extraer_eventos_a_dataframe(respuesta)
#             st.dataframe(df_eventos, use_container_width=True)
# else:
#     st.info("Escribe lo que necesites y elige el modo de asistencia.")

import streamlit as st
import google.generativeai as genai
import pandas as pd
from datetime import datetime, timedelta

# Configurar Gemini
genai.configure(api_key="AIzaSyAcKoa5G10uwHLc1zR-IUkTomOOAdg3_kE")

# Configurar Streamlit
st.set_page_config(page_title="📅 Asistente Personal con Agenda", layout="centered")
st.title("🧠 Tu Asistente con Gemini")
st.markdown("Puedes escribir cualquier cosa: preguntas generales, pedir consejos o que te organice tu semana.")

# Modo de asistencia
modo = st.selectbox("Selecciona el modo de asistencia:", ["Chat General", "Plan de Estudio"])
entrada = st.text_area("💭 Escribe tu mensaje o actividades:", height=200)
generar = st.button("Generar Respuesta")

# Función para generar respuesta general
def generar_chat(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    respuesta = model.generate_content(prompt)
    return respuesta.text

# Función para generar agenda semanal
def generar_plan(actividades):
    prompt = (
        f"""
        Genera un texto explicativo y práctico dirigido a estudiantes de todas las edades que han tenido dificultades y han reprobado algunas asignaturas con notas inferiores a 3.0. 
        El texto debe describir cómo la entidad educativa puede diseñar un plan de estudios efectivo para que estos estudiantes puedan recuperar sus materias y mejorar sus calificaciones a través de {actividades}. 
        Explica de manera clara y sencilla los pasos que se deben seguir, las estrategias de estudio recomendadas, y cómo organizar el tiempo para lograr el éxito académico. 
        Usa un lenguaje accesible para que cualquier estudiante pueda entenderlo.

        Además, incluye una tabla que detalle el contenido del plan de estudio, organizada por asignaturas, actividades específicas para recuperar la materia, y el tiempo recomendado para cada actividad.
        """
    )
    respuesta = generar_chat(prompt)
    return respuesta

# Extraer eventos a DataFrame para vista interactiva
def extraer_eventos_a_dataframe(respuesta_texto):
    dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    eventos = []
    dia_actual = ""

    for linea in respuesta_texto.splitlines():
        linea = linea.strip()
        if any(dia in linea.lower() for dia in dias):
            dia_actual = linea.strip(":")
        elif linea:
            eventos.append({"Día": dia_actual.capitalize(), "Actividad": linea})

    return pd.DataFrame(eventos)

# Mostrar resultado
if generar and entrada.strip():
    with st.spinner("Generando con Gemini..."):
        if modo == "Chat General":
            respuesta = generar_chat(entrada)
            st.subheader("🔊 Respuesta:")
            st.markdown(respuesta)
        elif modo == "Plan de Estudio":
            respuesta = generar_plan(entrada)
            st.subheader("🗓️ Plan de Estudio generado:")
            st.markdown(respuesta)
else:
    st.info("✍️ Escribe lo que necesites y elige el modo de asistencia.")