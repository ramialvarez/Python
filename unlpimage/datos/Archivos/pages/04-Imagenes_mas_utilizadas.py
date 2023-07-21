from os import path
import streamlit as st
import pandas as pd


def imagenes_collage(logs):   
    
    # Se filtran las filas del DataFrame logs que corresponden a la operación "Generacion de collage" que son las que me interesan
    imagenes_collage = logs[logs["Operación"] == "Nuevo collage"]
    
    # Dividir las listas de nombres de imágenes en una única Serie utilizando el separador ";"
    imagenes_collage_serie = imagenes_collage["Valores"].str.split(";", expand=True).stack()

    # Eliminar los espacios en blanco y reiniciar el índice de la Serie
    imagenes_collage_serie = imagenes_collage_serie.str.strip().reset_index(drop=True)

    # Se crea una Serie de pandas (frecuencias) a partir de la lista imagenes_collage_serie, donde cada elemento es un nombre de imagen. 
    # Luego se cuenta la frecuencia de cada nombre de imagen utilizando el método value_counts()
    frecuencias = pd.Series(imagenes_collage_serie).value_counts()

    # Se obtienen los 5 nombres de imágenes más comunes seleccionando los primeros 5 elementos de la Serie frecuencias utilizando el método head(5).
    top_5 = frecuencias.head(5)
    
    # Se crea un DataFrame grafico_collage con dos columnas: "Imágenes" y "Usos". 
    # La columna "Imágenes" contiene los nombres de las imágenes obtenidos en top_5.index, y la columna "Usos" contiene la frecuencia de uso de cada imagen obtenida en top_5.values. 
    # Se establece un índice personalizado utilizando range(1, len(top_5) + 1).
    grafico_collage = pd.DataFrame({"Imágenes": top_5.index, "Usos": top_5.values}, index=range(1, len(top_5) + 1))
    
    # Mostrar el gráfico en la columna correspondiente (columna 1) en la app de Streamlit
    return c1.table(grafico_collage)

def imagenes_memes(logs):
    
    # Se filtran las filas del DataFrame logs que corresponden a la operación "Generacion de collage" que son las que me interesan
    imagenes_memes = logs[logs["Operación"] == "Nuevo meme"]
    
    # Me quedo solo con la columna Valores (Serie de pandas) que contiene los nombres de las imagenes utilizadas para crear los memes
    imagenes_memes = imagenes_memes["Valores"]
    
    # Se crea una Serie de pandas (frecuencias) a partir de la lista imagenes_collage_plana, donde cada elemento es un nombre de imagen. 
    # Luego se cuenta la frecuencia de cada nombre de imagen utilizando el método value_counts()
    frecuencias = pd.Series(imagenes_memes).value_counts()

    # Se obtienen los 5 nombres de imágenes más comunes seleccionando los primeros 5 elementos de la Serie frecuencias utilizando el método head(5).
    top_5 = frecuencias.head(5)
    
    # Se crea un DataFrame grafico_collage con dos columnas: "Imágenes" y "Usos". 
    # La columna "Imágenes" contiene los nombres de las imágenes obtenidos en top_5.index, y la columna "Usos" contiene la frecuencia de uso de cada imagen obtenida en top_5.values. 
    # Se establece un índice personalizado utilizando range(1, len(top_5) + 1).
    grafico_memes = pd.DataFrame({"Imágenes" : top_5.index, "Usos": top_5.values}, index=range(1, len(top_5) + 1))
    
    # Mostrar el gráfico en la columna correspondiente (columna 2) en la app de Streamlit
    return c2.table(grafico_memes)

def estructura_columna1(c1):
    # Defino el estilo personalizado para el subtítulo del gráfico de collages
    subtitulo_collages_markdown = '<h3 style="font-family: Arial; text-align: right; color: #45B39D;">Imágenes más utilizadas para crear los collages</h3>'
    
    # Mostrar el subtítulo y el gráfico de collages con estilo personalizado
    c1.markdown(subtitulo_collages_markdown, unsafe_allow_html=True)
    imagenes_collage(logs)
    
    # Defino el subtitulo de la explicación del análisis de collages con estilo personalizado
    subtitulo_analisis_markdown = '<h3 style="font-family: Arial; text-align: left; color: #8E44AD;">Pasos para el análisis de los collages:</h3>'

    # Defino los pasos llevados a cabo para el análisis del uso de las imagenes para crear los collages 
    pasos_analisis = [
        ('Transformación de los datos', 'En primer lugar, transformamos el archivo de logs en un DataFrame utilizando la librería Pandas. Luego, se filtran las filas que corresponden a la operación de "Nuevo Collage" para obtener solo esas entradas.'),
        ('Obtención de los nombres de las imágenes', 'Se extraen los valores de la columna "Valores" de las filas filtradas, que representan los nombres de las imágenes utilizadas en la generación de collages. Se realiza un conteo de la frecuencia de aparición de cada nombre de imagen.'),
        ('Cálculo de uso de cada imágen', 'Se identifican los 5 nombres de imágenes más utilizados, basándose en la frecuencia de aparición. Estos nombres representan las imágenes más frecuentes en la generación de collages.'),
        ('Creación del gráfico de tabla', 'Se crea un gráfico de tabla que muestra los nombres de las imágenes en la columna "Imágenes" y la cantidad de usos correspondiente en la columna "Usos". Esta tabla proporciona una visualización clara de las imágenes más utilizadas en la generación de collages.')
    ]

    # Mostrar los pasos del análisis de collage en la columna 1
    c1.markdown(subtitulo_analisis_markdown, unsafe_allow_html=True)
    for i, (paso, descripcion) in enumerate(pasos_analisis):
        paso_html = f'<h6 style="font-family: Arial; text-align: left; color: #BB8FCE;">Paso {i+1}: {paso}</h6>'
        descripcion_html = f'<p style="font-family: Arial; text-align: justify;">{descripcion}</p>'
        c1.markdown(paso_html, unsafe_allow_html=True)
        c1.markdown(descripcion_html, unsafe_allow_html=True)

def estructura_columna2(c2):
    # Defino el estilo personalizado para el subtítulo del gráfico de memes
    subtitulo_memes_markdown = '<h3 style="font-family: Arial; text-align: right; color: #45B39D;">Imágenes más utilizadas para crear los memes</h3>'
    
    # Mostrar el subtítulo y el gráfico de memes con estilo personalizado
    c2.markdown(subtitulo_memes_markdown, unsafe_allow_html=True)
    imagenes_memes(logs)
    
    # Defino el subtitulo de la explicación del análisis de memes con estilo personalizado
    subtitulo_analisis_markdown = '<h3 style="font-family: Arial; text-align: left; color: #8E44AD;">Pasos para el análisis de los memes:</h3>'

    # Defino los pasos llevados a cabo para el análisis del uso de las imagenes para crear los memes 
    pasos_analisis = [
        ('Transformación de los datos', 'Al igual que en el análisis de los collages, en primer lugar, transformamos el archivo de logs en un DataFrame utilizando la librería Pandas. Luego, se filtran las filas que corresponden a la operación de "Nuevo Meme" para quedarse solo con esas entradas.'),
        ('Obtención de los nombres de las imágenes', 'A partir de las filas filtradas, se extraen los valores de la columna "Valores", que representan los nombres de las imágenes utilizadas para crear los memes. Se realiza un conteo de la frecuencia de aparición de cada nombre de imagen.'),
        ('Cálculo de uso de cada imágen', 'Se seleccionan los 5 nombres de imágenes más utilizados, basándose en la frecuencia de aparición. Estos nombres representan las imágenes más populares para la creación de memes.'),
        ('Creación del gráfico de tabla', 'Se genera un gráfico de tabla que muestra los nombres de las imágenes en la columna "Imágenes" y la cantidad de usos correspondiente en la columna "Usos". Esta tabla proporciona una visualización clara de las imágenes más utilizadas en la creación de memes.')
    ]

    # Mostrar los pasos del análisis en la columna 1
    c2.markdown(subtitulo_analisis_markdown, unsafe_allow_html=True)
    for i, (paso, descripcion) in enumerate(pasos_analisis):
        paso_html = f'<h6 style="font-family: Arial; text-align: left; color: #BB8FCE;">{i+1}. {paso}</h6>'
        descripcion_html = f'<p style="font-family: Arial; text-align: justify;">{descripcion}</p>'
        c2.markdown(paso_html, unsafe_allow_html=True)
        c2.markdown(descripcion_html, unsafe_allow_html=True)


# Defino el estilo personalizado para el título de la página de imagenes 
titulo_markdown = '<h1 style="font-family: Arial; text-align: center; color: #138D75;">Imágenes más utilizadas para crear los memes y los collages</h1>'

# Mostrar el título de la página con estilo personalizado
st.markdown(titulo_markdown, unsafe_allow_html=True)

# Obtengo la ruta absoluta del archivo de logs
ruta_logs = path.join(path.dirname(path.dirname(__file__)),"Logs.csv")

# Leo el archivo de logs con la libreria Pandas y lo transformo a un DataFrame
logs = pd.read_csv(ruta_logs, encoding='UTF-8')
    
# Se crean las columnas
c1, c2 = st.columns(2,gap= "large")

# Se establecen las estructuras de ambas columnas

estructura_columna1(c1)
estructura_columna2(c2)
        
    
    
    
