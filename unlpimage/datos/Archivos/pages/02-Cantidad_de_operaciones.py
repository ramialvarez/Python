from os import path
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np 

def cantidad_operaciones(logs):
    
    # Filtro las filas del DataFrame y me quedo solo con aqueelas que en la columna operaciones no tienen valor None
    operaciones = logs[logs["Operación"].notnull()]
    
    # Elimino de la Serie todas las columnas menos la de Operación, que es la única que me interesa
    operaciones = operaciones.drop(columns= ["Timestamp","Nick","Valores","Textos"], axis=1)
    
    # Reseteo el índice de la Serie y cuento la cantidad de veces que aparece cada operación con value_counts
    cant_apariciones = operaciones.reset_index()["Operación"].value_counts()
    
    # Creo el gráfico de barras.
    
    fig, ax = plt.subplots()
    
    # Definir los colores base para la gama
    color_amarillo = '#FDD835'
    color_rosa = '#C2185B'

    # Definir la gama de colores utilizando LinearSegmentedColormap
    colores_gama = LinearSegmentedColormap.from_list('GamaPersonalizada', [color_amarillo, color_rosa])

    # Obtener los valores para los colores en la gama
    valores_colores = np.linspace(0, 1, len(cant_apariciones))

    # Generar la gama de colores
    colores = colores_gama(valores_colores)
    
    bars = ax.bar(cant_apariciones.index, cant_apariciones.values,color=colores)

    # Establece el label del eje y
    ax.set_ylabel('Número de veces que se realizó cada operación')
    
    # Establece los límites del eje y
    ax.set_ylim(0, 100)
    ax.set_yticks(range(0, 101, 10))
    
    # Establece los labels en forma vertical
    ax.set_xticks(range(len(cant_apariciones.index)))
    ax.set_xticklabels(cant_apariciones.index, rotation='vertical')

    # Coloca las etiquetas de las barras
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, str(height), ha='center', va='bottom')

    return fig


# Defino el estilo personalizado para el título de la página de operaciones
titulo_markdown = '<h1 style="font-family: Arial; text-align: center; color: #FDD835;">Operaciónes realizadas en la aplicación</h1>'

# Mostrar el título de la página con estilo personalizado
st.markdown(titulo_markdown, unsafe_allow_html=True)

# Creo las columnas
c1,c2 = st.columns(2,gap="large")

# Obtengo la ruta absoluta del archivo de logs.
ruta_logs = path.join(path.dirname(path.dirname(__file__)),"Logs.csv")

# Leo el archivo de logs con la libreria Pandas y lo transformo a un DataFrame
logs = pd.read_csv(ruta_logs, encoding= "UTF-8")

# Defino el subtitulo de la explicación del análisis con estilo personalizado
subtitulo_analisis_markdown = '<h3 style="font-family: Arial; text-align: left; color: #C2185B ;">Pasos del análisis:</h3>'

# Defino los pasos llevados a cabo para el análisis de los datos del archivo de logs
pasos_analisis = [
    ('Transformación de los datos', 'En primer lugar, transformamos el archivo de logs en un DataFrame utilizando la librería Pandas. Luego, seleccionamos únicamente la columna "Operación" ya que es la que nos interesa para nuestro análisis posterior.'),
    ('Cálculo de operaciones', 'Una vez que tenemos el DataFrame con la columna "Operación", realizamos el cálculo para determinar la cantidad de veces que se realizó cada operación en el conjunto de datos. Utilizamos la función value_counts() de Pandas para contar la frecuencia de cada operación.'),
    ('Creación del gráfico de barras', 'Para visualizar de manera efectiva la información obtenida, creamos un gráfico de barras. En este gráfico, representamos en el eje x los nombres de las operaciones y en el eje y la cantidad de veces que se realizaron. Cada barra del gráfico representa una operación y su altura indica la frecuencia correspondiente. Además, agregamos etiquetas en las barras para mostrar el valor exacto de cada frecuencia.'),
]

# Mostrar los pasos del análisis en la columna 1
c1.markdown(subtitulo_analisis_markdown, unsafe_allow_html=True)
for i, (paso, descripcion) in enumerate(pasos_analisis):
    paso_html = f'<h6 style="font-family: Arial; text-align: left; color: #FFEE58;">{i+1}. {paso}</h6>'
    descripcion_html = f'<p style="font-family: Arial; text-align: justify; color: #17202A;">{descripcion}</p>'
    c1.markdown(paso_html, unsafe_allow_html=True)
    c1.markdown(descripcion_html, unsafe_allow_html=True)

# Defino el subtitulo del gráfico con estilo personalizado 
subtitulo_grafico_markdown = '<h3 style="font-family: Arial; text-align: right; color: #C2185B;">Cantidad de veces que se realizó cada operación</h3>'
    
# Mostrar el gráfico y el subtitulo del gráfico con estilo personalizado en la columna 2
c2.markdown(subtitulo_grafico_markdown, unsafe_allow_html=True)
grafico_cantidad_operaciones = cantidad_operaciones(logs)
c2.pyplot(grafico_cantidad_operaciones)
