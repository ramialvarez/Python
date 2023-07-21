from os import path
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np


def cambios_por_dia(logs):

        # La columna "Timestamp" del DataFrame logs se convierte a formato de fecha y hora utilizando pd.to_datetime. 
        # Se utiliza el argumento unit="s" para indicar que los valores en la columna representan timestamps en segundos.
        fechas = pd.to_datetime(logs["Timestamp"], unit="s")
        
        # Se utiliza el atributo dt.weekday de las fechas para obtener el índice numérico del día de la semana para cada fecha. 
        # Luego, se utiliza el método value_counts para contar la cantidad de ocurrencias de cada índice. 
        # El resultado se ordena por índice utilizando sort_index. 
        # La Serie resultante, cant_cambios_dia , ahora contiene la cantidad de cambios por día de la semana.
        
        cant_cambios_dia = fechas.dt.weekday.value_counts().sort_index()
        
        # Creo el gráfico de barras.
        fig, ax = plt.subplots()
        
        # Defino los labels horizontales del gráfico
        labels = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        
        # Definir los colores base para la gama
        color_azul = '#1A5276'
        color_marron = '#B03A2E'

        # Definir la gama de colores utilizando LinearSegmentedColormap
        colores_gama = LinearSegmentedColormap.from_list('GamaPersonalizada', [color_azul, color_marron])

        # Obtener los valores para los colores en la gama
        valores_colores = np.linspace(0, 1, len(cant_cambios_dia))

        # Generar la gama de colores
        colores = colores_gama(valores_colores)

        # Creo el grafico con sus respectivos labels, valores y colores
        bars = ax.bar(labels, cant_cambios_dia.values, color=colores)

        # Establezco el nombre del eje y
        ax.set_ylabel('Número de Cambios')
        
        # Establecer límites del eje y
        ax.set_ylim(0, 100)
        ax.set_yticks(range(0, 101, 10))
        
        # Coloca las etiquetas de las barras
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height, str(height), ha='center', va='bottom')

        return fig  
    

# Defino el estilo personalizado para el título de la página
titulo_markdown = '<h1 style="font-family: Arial; text-align: center; color: #1A5276;">Usos de la aplicación por día</h1>'

# Mostrar el título de la página con estilo personalizado
st.markdown(titulo_markdown, unsafe_allow_html=True)

# Creo las columnas
c1,c2 = st.columns(2,gap="large")

# Defino la dirección absoluta del archivo de logs
ruta_logs = path.join(path.dirname(path.dirname(__file__)),"Logs.csv")

# Leo el archivo de logs con la libreria Pandas y lo transformo a un DataFrame
logs = pd.read_csv(ruta_logs, encoding="UTF-8")

# Defino el subtitulo de la explicación del análisis con estilo personalizado
subtitulo_analisis_markdown = '<h3 style="font-family: Arial; text-align: left; color: #B03A2E;">Pasos del análisis:</h3>'

# Defino los pasos llevamos a cabo para el análisis de los datos del archivo de logs
pasos_analisis = [
    ('Transformación de los datos', 'Transformo el archivo de logs en un DataFrame, me quedo solo con la columna "Timestamp" y convierto los valores a formato de fecha y hora.'),
    ('Cálculo de cambios por día', 'Obtengo el índice numérico correspondiente a cada día de la semana y cuento la cantidad de cambios realizados por día, es decir, la cantidad de ocurrencias de cada índice.'),
    ('Creación del gráfico de barras', 'Para visualizar de manera efectiva la información obtenida, creamos un gráfico de barras. En este gráfico, representamos en el eje x los nombres de los días de la semana y en el eje y la cantidad de usos de la aplicación que hubo en cada día respectivamente. Cada barra del gráfico representa un día y su altura indica la frecuencia correspondiente. Además, agregamos etiquetas en las barras para mostrar el valor exacto de cada frecuencia.')
]

# Mostrar los pasos del análisis en la columna 1
c1.markdown(subtitulo_analisis_markdown, unsafe_allow_html=True)
for i, (paso, descripcion) in enumerate(pasos_analisis):
    paso_html = f'<h6 style="font-family: Arial; text-align: left; color: #2980B9;">{i+1}. {paso}</h6>'
    descripcion_html = f'<p style="font-family: Arial; text-align: justify; color: #17202A;">{descripcion}</p>'
    c1.markdown(paso_html, unsafe_allow_html=True)
    c1.markdown(descripcion_html, unsafe_allow_html=True)

# Defino el subtitulo del gráfico con estilo personalizado
subtitulo_grafico_markdown = '<h3 style="font-family: Arial; text-align: right; color: #B03A2E;">Cambios hechos en la aplicación por día</h3>'

# Mostrar el gráfico y el subtitulo del gráfico en la columna 2
c2.markdown(subtitulo_grafico_markdown, unsafe_allow_html=True)
grafico_dias = cambios_por_dia(logs)
c2.pyplot(grafico_dias,clear_figure=True)