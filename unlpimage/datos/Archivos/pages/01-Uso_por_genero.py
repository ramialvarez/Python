from os import path
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def uso_por_genero(logs,perfiles):
    #Intercambio filas y columnas
    perfiles = perfiles.transpose()

    #Fusiono ambos DataFrame usando la columna de Nick
    fusion = pd.merge(perfiles,logs,on='Nick')

    #Cuento los valores en autogenero y los ordeno en orden descendiente
    fusion = fusion.value_counts('autogenero').sort_values(ascending=False)

    #Obtengo los géneros del índice de la Series para usar de etiquetas
    etiquetas = list(fusion.index)

    #Genero los colores a utilizar en el gráfico
    colors = plt.get_cmap('rainbow')(np.linspace(0.2, 0.7, len(fusion)))

    #Genero variables a utilizar para el gráfico
    fig, ax = plt.subplots()

    #Generación del gráfico de torta
    ax.pie(fusion, colors=colors, radius=3, center=(4, 4),wedgeprops={"linewidth": 0, "edgecolor": "white"},labels=etiquetas, autopct='%1.1f%%',shadow=True, startangle=120, labeldistance= 1.1)

    #Colocación de la leyenda a partir de las etiquetas
    ax.legend(etiquetas,loc='upper right')

    #Cambio del tamaño del gráfico
    ax.set(xlim=(0, 8),ylim=(0, 8))

    return fig


#Defino la dirección relativa del archivo de logs
ruta_logs = path.join(path.dirname(path.dirname(__file__)),"Logs.csv")

#Defino la dirección relativa del archivo de perfiles
ruta_json = path.join(path.dirname(path.dirname(__file__)),"Archivo_perfiles.json")

# Leo el archivo de logs con la libreria Pandas y lo transformo en un DataFrame
logs = pd.read_csv(ruta_logs, encoding="UTF-8")

# Leo el archivo de perfiles con la libreria Pandas y lo transformo en un DataFrame
perfiles = pd.read_json(ruta_json)

#  Estilo personalizado para el título
titulo_markdown = '<h1 style="font-family: Arial; text-align: center; color: #1ed6d6;">Uso de la aplicación por género</h1>'

# Mostrar el título de la página con estilo personalizado
st.markdown(titulo_markdown, unsafe_allow_html=True)

# Creo las columnas
c1,c2 = st.columns(2,gap="large")

# Defino el subtitulo de la explicación del análisis con estilo personalizado
subtitulo_analisis_markdown = '<h3 style="font-family: Arial; text-align: left; color: #2b9999;">Pasos del análisis:</h3>'

# Defino los pasos llevamos a cabo para el análisis de los datos del archivo de logs
pasos_analisis = [
    ('Transformación de los datos', 'Transformo el archivo de logs y el archivo de perfiles en un DataFrame. En el archivo de perfiles intercambio las filas por las columnas, para luego poder fusionar ambos DataFrame en uno solo, con la columna de Nick como eje de fusión.'),
    ('Contar valores', 'Una vez que obtengo el DataFrame fusionado, en cada operación que aparece en los logs me va a aparecer el género de quien la realizó. A partir de esto, cuento los valores de la columna "autogenero", que contiene los géneros de las personas que realizaron estas operaciones, utilizando valuecounts.'),
    ('Creación del gráfico de torta', 'A partir de la Series que tiene la cantidad de apariciones de cada género, creo el gráfico de torta. Utilizo el índice de la Series como leyendas del gráfico.')
]

# Mostrar los pasos del análisis en la columna 1
c1.markdown(subtitulo_analisis_markdown, unsafe_allow_html=True)
for i, (paso, descripcion) in enumerate(pasos_analisis):
    paso_html = f'<h6 style="font-family: Arial; text-align: left; color: #1ed6d6;">{i+1}. {paso}</h6>'
    descripcion_html = f'<p style="font-family: Arial; text-align: justify; color: #17202A;">{descripcion}</p>'
    c1.markdown(paso_html, unsafe_allow_html=True)
    c1.markdown(descripcion_html, unsafe_allow_html=True)

# Estilo personalizado para el subtítulo
subtitulo_grafico_markdown = '<h3 style="font-family: Arial; text-align: center; color: #2b9999;">Porcentajes de uso de la aplicación por género</h3>'

# Mostrar el gráfico y el subtitulo del gráfico en la columna 2
c2.markdown(subtitulo_grafico_markdown, unsafe_allow_html=True)
c2.pyplot(uso_por_genero(logs,perfiles),clear_figure=True)