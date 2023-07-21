import os
import json
from PIL import Image, ImageTk
import PySimpleGUI as sg
from unlpimage.config.rutas import get_rutas,RUTA_BOTONES,RUTA_TEMPLATES, RUTA_PLANTILLAS_MEMES
from unlpimage.pantallas import generador_memes as gm

#Constantes
TAMANIO_TEXTO = 16
TAMANIO_TITULO  = 25

def cargar_imagen(nombre_archivo) :
    """Carga la imagen a ser mostrada en pantalla

        Args:
            nombre_archivo (str): ruta donde se encuentra la imagen a cargar
        Returns:
            imagen_lista (ImageTk.PhotoImage): imagen lista para ser mostrada en pantalla
            imagen (Image): imagen previa para obtener los datos de la misma
    """
    
    with open(nombre_archivo, 'rb') as archivo:
        imagen = Image.open(archivo)
        imagen_lista = ImageTk.PhotoImage(image=imagen)
    return imagen_lista


def cargar_archivo():
    """Carga el archivo que contiene la informacion de los templates
        Returns :
            templates (list): lista con la informacion de las plantillas. 
    """
    
    try:
        with open(RUTA_TEMPLATES,'r',newline='') as archivo:
            templates = json.load(archivo)
    except FileNotFoundError:
        templates = []
    return templates


def layout(templates):
    """Crea elementos para la ventana

    Args:
        templates (list): lista con la información de las plantillas de memes
    
    Returns:
        layout (list): Lista con la informacion de la ventana 
    """

    ancho_ventana = 1000
    
    nombres_templates = [name['name'] for name in templates]

    columna_archivos = [[sg.Listbox(values=nombres_templates,no_scrollbar=True, enable_events=True, 
                                    size=(40,15),key='-TEMPLATE-LISTA-')]]
    
    columna_imagenes = [[sg.Frame('',[
              [sg.Text(size=(40,1), key='-NOMBRE-')],
              [sg.Image(filename = os.path.join(RUTA_BOTONES,'Defecto.png'),key='-IMAGE-')]
              ],key='-FRAMEIMG-')
              ]
    ]
    
    encabezado = [
        [
            
            sg.Frame('',
                [[sg.Text("Generar meme", font=('Rockwell', 20),justification= 'left')]], 
                element_justification="left",border_width = 0,size=(ancho_ventana//2,100)),
            sg.Frame('',
                [[sg.Button("Volver",key= '-TEMPLATE-VOLVER-')]], 
                element_justification="right",border_width = 0,size=(ancho_ventana//2,80))
                
        ]
    ]

    return [
    [encabezado],
    [sg.Frame('',
                [[sg.Column(columna_archivos, element_justification='c',size=(ancho_ventana//2,600),key='-COLUMARCH-'), 
                  sg.VSeperator(),
                  sg.Column(columna_imagenes, element_justification='c',key='-COLUMIMG-')
                  ]],border_width = 0,size=(ancho_ventana,500)),

    ],
    [sg.Frame('',
                [[sg.Button("Generar",key= '-TEMPLATE-GENERAR-')]], 
                element_justification="right",border_width = 0,size=(ancho_ventana,80))]
    ]

def crear_ventana(menu,perfil) :
    """Crea la ventana del generador de memes.
    Args:
        menu (PySimpleGUI.PySimpleGUI.Window) = pantalla del menu para luego ser desencondida."""
    
    templates = cargar_archivo()  
    return sg.Window("Generador de memes", layout(templates), margins=(10,10), finalize=True,
                     metadata={'menu':menu,'elegida' : None,'templates':templates,'perfil':perfil})


def procesar_eventos(current_window, event, values) :
    """Procesa los eventos de la ventana generador de memes.
    Args:
        current_window (PySimpleGUI.PySimpleGUI.Window) = Ventana de Generador de memes.
        event (str) = Nombre de el evento producido en la ventana.
        values (dict) = Diccionario con los valores de la ventana."""
    
    match event :
        case 'VOLVER':
            current_window.metadata['menu'].un_hide()
            current_window.close()
        case 'LISTA':
            nombre = values['-TEMPLATE-LISTA-'][0]
            for temp in current_window.metadata['templates']:
                if temp['name'] == nombre:
                    elegida = temp
                    break
            ruta = os.path.join(RUTA_PLANTILLAS_MEMES, elegida['image'])
            current_window.metadata['elegida'] = elegida
            imagen_lista = cargar_imagen(ruta)
            current_window['-IMAGE-'].update(data=imagen_lista)
        case 'GENERAR':
            if current_window.metadata['elegida'] != None:
                gm.crear_ventana(current_window.metadata['menu'],current_window.metadata['elegida'],current_window.metadata['perfil'])
                current_window.close()
            else:
                sg.popup_error("Primero debes seleccionar una imágen")