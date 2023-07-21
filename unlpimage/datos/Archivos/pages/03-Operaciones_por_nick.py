from os import path
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

def cantidad_operaciones_por_nick(logs):
    
    # Filtrar el DataFrame para quedarse con las columnas de "Nick" y "Operación"
    operaciones = logs[['Nick', 'Operación']].dropna()

    # Agrupar por nickname y operación y contar la cantidad de veces que aparece cada combinación
    cant_operaciones_por_nick = operaciones.groupby(['Nick', 'Operación']).size().reset_index(name='Cantidad')
    
    # Defino los colores para definir la gama
    color_naranja = "#E64A19"
    color_violeta =  "#4527A0"
    
    # Definir la gama de colores utilizando LinearSegmentedColormap
    colores_gama = LinearSegmentedColormap.from_list('GamaPersonalizada', [color_violeta, color_naranja])

    # Obtener los valores para los colores en la gama
    valores_colores = np.linspace(0, 1, 7)

    # Generar la gama de colores
    colores = colores_gama(valores_colores)
    
    # Crear el gráfico de barras
    fig, ax = plt.subplots()
    
    # Crear una paleta de colores personalizada para identificar cada tipo de operación
    paleta_de_colores = {'Creación de nuevo perfil': colores[0], 'Modificación de perfil': colores[1], 'Modificación de imagen previamente clasificada': colores[2], 'Nueva imagen clasificada': colores[3], 'Cambio en la configuración del sistema': colores[4], 'Nuevo collage' : colores[5], 'Nuevo meme': colores[6]}
    
    
    izquierda = dict.fromkeys(cant_operaciones_por_nick['Nick'].unique(),0)

    # Iterar sobre cada fila del DataFrame para generar el gráfico de barras
    for indice, fila in cant_operaciones_por_nick.iterrows():
        nick = fila['Nick']
        operacion = fila['Operación']
        cantidad = fila['Cantidad']
    
        # Verificar si la cantidad es mayor que cero
        if cantidad > 0:
            # Verificar si la operación está en la paleta de colores
            if operacion in paleta_de_colores:
                # Agregar una barra horizontal al gráfico con el nick, cantidad y color correspondiente
                ax.barh(nick, cantidad, color=paleta_de_colores[operacion],left=izquierda[fila['Nick']])
                izquierda[fila['Nick']] += fila['Cantidad']
    
    # Crear leyenda con los nombres de cada operación y el color que le corresponde
    patchs_leyenda = [mpatches.Patch(color= colores[0], label='Creación de nuevo perfil'), mpatches.Patch(color= colores[1] , label='Modificación de perfil'), mpatches.Patch(color= colores[2], label='Modificación de imagen previamente clasificada'), mpatches.Patch(color= colores[3] , label='Nueva imagen clasificada'), mpatches.Patch(color= colores[4], label='Cambio en la configuración del sistema'), mpatches.Patch(color= colores[5], label='Generacion de collage'), mpatches.Patch(color= colores[6], label='Nuevo meme')]
   
    # Colocar la leyenda fuera del área de las barras
    ax.legend(title='Color de cada operación',handles= [patch for patch in patchs_leyenda],bbox_to_anchor=(1.04, 1), loc='upper left')
    
    # Agregar el título del eje x
    ax.set_xlabel('Cantidad de operaciones')

    # Establecer los límites del eje x
    ax.set_xlim(0, 50)
    ax.set_xticks(range(0, 51, 10))

    # Establecer los ticks y labels del eje y
    ax.set_yticks(range(len(cant_operaciones_por_nick["Nick"].unique())))
    ax.set_yticklabels(cant_operaciones_por_nick["Nick"].unique(), rotation='horizontal')
    
    return fig

# Obtengo la ruta absoluta del archivo de logs
ruta_logs = path.join(path.dirname(path.dirname(__file__)),"Logs.csv")

# Leo el archivo de logs con la libreria Pandas y lo transformo a un DataFrame
logs = pd.read_csv(ruta_logs,encoding= "UTF-8")

# Defino el título de la página con estilo personalizado 
titulo_markdown = '<h1 style="font-family: Arial; text-align: center; color: #E64A19;">Operaciones realizadas por los usuarios</h1>'
    
# Mostrar el título de la página con estilo personalizado
st.markdown(titulo_markdown, unsafe_allow_html=True)

# Creo las columnas
c1,c2 = st.columns(2,gap="large")

# Defino el subtitulo de la explicación del análisis con estilo personalizado
subtitulo_analisis_markdown = '<h3 style="font-family: Arial; text-align: left; color: #4527A0 ;">Pasos del análisis:</h3>'

# Defino los pasos llevados a cabo para el análisis de los datos del archivo de logs
pasos_analisis = [
    ('Transformación de los datos', 'Inicialmente, importamos el archivo de logs y lo convertimos en un DataFrame utilizando la biblioteca Pandas. Luego, seleccionamos las columnas relevantes para nuestro análisis, que en este caso son "Nick" y "Operación".'),
    ('Cálculo de operaciones por usuario', 'A continuación, agrupamos los datos por nickname y operación utilizando la función groupby() de Pandas. Contamos la cantidad de veces que aparece cada combinación de nickname y operación y almacenamos estos valores en una nueva columna. Esto nos permite conocer la cantidad de operaciones realizadas por cada usuario en el conjunto de datos.'),
    ('Creación del gráfico de barras', 'Para visualizar de manera efectiva la información obtenida, creamos un gráfico de barras. En este gráfico, representamos en el eje x la cantidad de operaciones y en el eje y los nombres de los usuarios (nicknames). Cada barra del gráfico representa una operación, y la altura de cada barra indica la frecuencia correspondiente. Además, utilizamos colores diferentes para cada tipo de operación, lo que facilita la interpretación visual de los datos.'),
]

# Mostrar los pasos del análisis en la columna 1
c1.markdown(subtitulo_analisis_markdown, unsafe_allow_html=True)
for i, (paso, descripcion) in enumerate(pasos_analisis):
    paso_html = f'<h6 style="font-family: Arial; text-align: left; color: #FF7043;">{i+1}. {paso}</h6>'
    descripcion_html = f'<p style="font-family: Arial; text-align: justify; color: #17202A;">{descripcion}</p>'
    c1.markdown(paso_html, unsafe_allow_html=True)
    c1.markdown(descripcion_html, unsafe_allow_html=True)
    
# Defino el subtitulo del gráfico con estilo personalizado 
subtitulo_grafico_markdown = '<h3 style="font-family: Arial; text-align: right; color: #4527A0;">Cantidad de operaciones realizadas por cada usuario</h3>'

# Mostrar el gráfico y el subtitulo del gráfico con estilo personalizado en la columna 2
c2.markdown(subtitulo_grafico_markdown, unsafe_allow_html=True)
grafico_cantidad_operaciones_por_nick = cantidad_operaciones_por_nick(logs)
c2.pyplot(grafico_cantidad_operaciones_por_nick)


