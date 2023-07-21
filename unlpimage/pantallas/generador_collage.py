import PySimpleGUI as sg
import os
from unlpimage.pantallas import imagenes_collages as imagenes
from unlpimage.config.rutas import RUTA_PLANTILLAS_COLLAGES

#Constantes
TAMANIO_TEXTO = 16
TAMANIO_TITULO  = 25

def layout () :
    """Crea los elementos del generador de collages.
        
        Returns  :
            lista con elementos de la ventana.
    """
    
    encabezado = [
            [sg.Text("Generador de collage", font=('Rockwell', TAMANIO_TITULO), justification="center", pad = (290,1))]
    ]

    columna1 = [
        [
            sg.Image(
                    source= os.path.join(RUTA_PLANTILLAS_COLLAGES, '2fotos.png'),
                    key="-COLLAGE-2fotos",
                    size=(400,400),
                    pad=((50,50),(5,5)),
                    enable_events=True
            ),
            sg.Image(
                    source= os.path.join(RUTA_PLANTILLAS_COLLAGES, '4fotos.png'),
                    key="-COLLAGE-4fotos",
                    size=(400, 400),
                    pad=((50,50),(5,5)),
                    enable_events=True
            )    
        ]
    ]

    columna2 = [
        [
            sg.Image(
                    source= os.path.join(RUTA_PLANTILLAS_COLLAGES, '4arriba.png'),
                    key="-COLLAGE-4arriba",
                    size=(400,400),
                    pad=((50,50),(5,5)),
                    enable_events=True
            ),
            sg.Image(
                    source= os.path.join(RUTA_PLANTILLAS_COLLAGES, '3fotos.png'),
                    key="-COLLAGE-3fotos",
                    size=(400, 400),
                    pad=((50,50),(5,5)),
                    enable_events=True
            ) 
        ]
    ]

    columna3 = [
        [
            sg.Button("Volver",key='-COLLAGE-VOLVER-')
        ]
    ]

    return [
        [sg.Column(layout=encabezado)],
        [
            sg.Column(
                layout=columna1, 
                justification="center", 
            )
        ],
        [
            sg.Column(
                layout=columna2, 
                justification="center", 
            )
        ],
        [sg.Column(
                layout=columna3, 
                justification="center", 
            )
        ]
    ]

def crear_ventana (menu, nick_usuario) :
    """Crea la ventana del generador de collages.
        Args:
            menu (PySimpleGUI.PySimpleGUI.Window) = pantalla del menu para luego ser desencondida.
            nick_usuario = nick del usuario que esta generando un collage.
    """
    
    return sg.Window("Generador de collages", layout(), margins=(2,2), background_color='white', metadata = {'menu':menu, 'nick_usuario':nick_usuario},finalize=True)

def procesar_eventos (current_window, event) :
    """Procesa los eventos de la ventana generador de collages.
        Args:
            current_window (PySimpleGUI.PySimpleGUI.Window) = Ventana de Generador de collages.
            event (str) = Nombre de el evento producido en la ventana.
    """
    match event :
        case 'VOLVER':
            current_window.metadata['menu'].un_hide()
            current_window.close()
        case _ :
            collage = current_window
            collage.hide()
            imagenes.crear_ventana(event, collage, current_window.metadata['nick_usuario'])