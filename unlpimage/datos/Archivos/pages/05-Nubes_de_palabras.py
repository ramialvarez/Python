from os import path
import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud,STOPWORDS
import pandas as pd

def nube_memes (logs):
    #Leo el archivo de logs donde está la información
    logs = pd.read_csv(ruta_logs, encoding='utf-8')
    #Relleno los espacios que pueden generar problemas con string vacios
    logs = logs.fillna('')
    #Me quedo solo con las generaciones de memes
    memes = logs[logs['Operación'] == 'Nuevo meme']
    #Divido los textos utilizados para la creación de los memes
    memes = memes['Textos'].apply(lambda x: list(map(lambda x: x.split(),x.split(';'))))

    #Verifico si alguna operación no tiene elementos y las agrupo en la variable palabras 
    if type(memes.sum()) == list:
        frases = memes.sum()
    else:
        frases = []

    #Filtro las palabras para deshacerme de las demasiado cortas
    palabras_filtradas = [word for frase in frases for word in frase if len(word) > 2]

    if palabras_filtradas != []:
        #Creo el texto que la wordcloud necesita para ser generada
        texto = str(palabras_filtradas).replace("'","")
        #Genero la wordcloud utilizando WordCloud
        wordcloud = WordCloud(width = 300, height = 200,mode='RGBA', background_color=None,random_state=2, colormap='cool', collocations=False, stopwords = STOPWORDS).generate(texto)
        #Creo la variable de la figura a mostrar
        fig = plt.figure(figsize=(10, 5))
        #Establezco la figura a mostrar enviando la wordcloud
        plt.imshow(wordcloud, interpolation='bilinear')
    else:
        fig = plt.figure(figsize=(10, 5))
    #Saco el axis que no es necesario en este grafico
    plt.axis('off')
    return fig


def nube_collages (logs):
    #Leo el archivo de logs donde está la información
    logs = pd.read_csv(ruta_logs, encoding='utf-8')
    #Relleno los espacios que pueden generar problemas con string vacios
    logs = logs.fillna('')
    #Me quedo solo con las generaciones de collages
    collages = logs[logs['Operación'] == 'Nuevo collage']
    #Divido los textos utilizados para los collages para quedarme solo con las palabras
    collages = collages['Textos'].apply(lambda x: x.split())

    #Verifico si alguna operación no tiene elementos y las agrupo en la variable palabras
    if type(collages.sum()) == list:
        palabras = set(collages.sum())
    else:
        palabras = []

    #Filtro las palabras para deshacerme de las demasiado cortas
    palabras_filtradas = [word for word in palabras if len(word) > 2]
    if palabras_filtradas != []:
        #Creo el texto que la wordcloud necesita para ser generada
        texto = str(palabras_filtradas).replace("'","")
        #Genero la wordcloud utilizando WordCloud
        wordcloud = WordCloud(width = 300, height = 200,mode='RGBA', background_color=None,random_state=2, colormap='cool', collocations=False, stopwords = STOPWORDS).generate(texto)
        #Creo la variable de la figura a mostrar
        fig = plt.figure(figsize=(10, 5))
        #Establezco la figura a mostrar enviando la wordcloud
        plt.imshow(wordcloud, interpolation='bilinear')
    else:
        fig = plt.figure(figsize=(10, 5))
    #Saco el axis que no es necesario en este grafico
    plt.axis('off')
    return fig


# Defino la dirección relativa del archivo de logs
ruta_logs = path.join(path.dirname(path.dirname(__file__)),"Logs.csv")

# Leo el archivo de logs con la libreria Pandas y lo transformo en un DataFrame
logs = pd.read_csv(ruta_logs, encoding="UTF-8")

#  Estilo personalizado para el título
titulo_markdown = '<h1 style="font-family: Arial; text-align: center; color: #502491;">Nubes de palabras</h1>'

# Mostrar el título de la página con estilo personalizado
st.markdown(titulo_markdown, unsafe_allow_html=True)

# Creo las columnas
c1,c2 = st.columns(2,gap="large")

# Defino el subtitulo de la explicación del análisis con estilo personalizado
subtitulo_analisis_markdown = '<h3 style="font-family: Arial; text-align: left; color: #8444e3;">Pasos del análisis:</h3>'

# Defino los pasos llevamos a cabo para el análisis de los datos del archivo de logs
pasos_analisis = [
    ('Transformación de los datos', 'Transformo el archivo de logs en un DataFrame, relleno los espacios vacíos para evitar problemas y genero un DataFrame solo con las filas que contienen "Nuevo meme"  en la columna "Operación" y otro con las filas que contienen "Nuevo collage".'),
    ('División de textos', 'En cada DataFrame utilizó un apply que me permita dividir los textos en las columnas "Textos" de cada DataFrame, en el caso de los collages los divido por espacio y en los memes por punto y coma.'),
    ('Sumatoria de textos', 'Sumo las palabras de la columna de textos en una variable. Para ello verifico que exista contenido de la operación correspondiente. Posteriormente, filtro aquellas palabras que poseen una longitud menor a 2 letras.'),
    ('Creación de la nube de palabras', 'Una vez obtenida la lista de palabras a utilizar, genero un string que luego utilizo para generar la nube de palabras con WordCloud.')
]

# Mostrar los pasos del análisis en la columna 1
c1.markdown(subtitulo_analisis_markdown, unsafe_allow_html=True)
for i, (paso, descripcion) in enumerate(pasos_analisis):
    paso_html = f'<h6 style="font-family: Arial; text-align: left; color: #502491;">{i+1}. {paso}</h6>'
    descripcion_html = f'<p style="font-family: Arial; text-align: justify; color: #17202A;">{descripcion}</p>'
    c1.markdown(paso_html, unsafe_allow_html=True)
    c1.markdown(descripcion_html, unsafe_allow_html=True)

# Estilo personalizado para el subtítulo
subtitulo_grafico_markdown_meme = '<h3 style="font-family: Arial; text-align: center; color: #8444e3;">Palabras utilizadas para generar memes</h3>'
subtitulo_grafico_markdown_collage = '<h3 style="font-family: Arial; text-align: center; color: #8444e3;">Palabras utilizadas para generar collages</h3>'

# Mostrar el gráfico y el subtitulo del gráfico en la columna 2
c2.markdown(subtitulo_grafico_markdown_meme, unsafe_allow_html=True)
c2.pyplot(nube_memes(logs),clear_figure=True)
c2.markdown(subtitulo_grafico_markdown_collage, unsafe_allow_html=True)
c2.pyplot(nube_collages(logs),clear_figure=True)