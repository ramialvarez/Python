import PySimpleGUI as sg
import os
from unlpimage.pantallas import configuracion, etiquetar_imagenes, generador_collage, modificar_perfil, seleccionar_template
from unlpimage.config.rutas import RUTA_BOTONES, RUTA_IMAGENES_USUARIOS

def layout(perfil):
    """Crea elementos para la ventana.

        Args : 
            perfil: diccionario con datos del perfil cargado.
        
        Returns :
            layout (list): Lista con la informacion de la ventana.
    """
    tam_bot = 20 
    Columna1 = [
        [sg.Frame('',[
        [sg.Image(filename=os.path.join(RUTA_IMAGENES_USUARIOS,perfil.get("-NUEVO_PERFIL-RUTA_AVATAR-")),
                  subsample=2,key='-PRINCIPAL-IMAGEN-',enable_events=True)],
        [sg.Text(perfil.get("Nick"), text_color='black')]
    ],size = (200,600),border_width = 0,element_justification = "left")
    ]
    ]

    Columna2 = [
        [sg.Frame('',[
        [sg.Button('Etiquetar imagenes',size = tam_bot,key = '-PRINCIPAL-ETIQUETAR-')], 
        [sg.Button('Generar Meme',size = tam_bot,key = '-PRINCIPAL-MEME-')],
        [sg.Button("Generar Collage",size = tam_bot,key = '-PRINCIPAL-COLLAGE-')],
        [sg.Button("Salir",size = tam_bot,key = '-SALIR-')]
    ], element_justification = "center",border_width = 0, size = (600,200))
    ]
    ]

    Columna3 = [
        [sg.Frame('',[
        [sg.Button(image_filename = os.path.join(RUTA_BOTONES,'C.png'),
                   image_subsample = 3,button_color = 'Light gray',key = '-PRINCIPAL-CONFIGURACION-'), 
         sg.Button(image_filename = os.path.join(RUTA_BOTONES,'Ayuda.png'),
                   image_subsample = 3,button_color = 'Light gray',key = '-PRINCIPAL-AYUDA-')]
    ],border_width = 0,size = (200,500),element_justification = "right")
    ]
    ]
    return [[sg.Column(Columna1),sg.Column(Columna2),sg.Column(Columna3)]]


def crear_ventana(perfil):
    """Crea la ventana del menu principal.

        Args :
            perfil (dict): Diccionario con los datos del perfil seleccionado.
        
        Returns :
            window (PySimpleGUI.PySimpleGUI.Window): Ventana de Menu Principal.
    """
    return sg.Window("Menu Principal", layout(perfil),metadata = {'perfil':perfil},finalize = True,resizable=True)

def procesar_eventos(current_window,event,values):
    """Maneja los eventos del menu principal.
        
        Args :
            current_window (PySimpleGUI.PySimpleGUI.Window): Ventana de Menu Principal.
            event (str): Nombre del evento producido en la ventana.
            values (dict): Diccionario con los valores de la ventana.
    """
    match event:
        case 'CONFIGURACION':
            menu = current_window
            menu.hide()
            configuracion.crear_ventana(menu,current_window.metadata['perfil'])
        case 'AYUDA':
            sg.Popup('Configuracion - Puede cambiar las rutas de los repositorios de imagenes.' +
            '\nPerfil - Le permite cambiar la configuracion del perfil'+
            '\nEtiquetar imagenes - Le permite etiquetar las imagenes para clasificarlas mejor y conocer sus metadatos'+
            '\nGenerar Memes - Le permite crear sus memes personalizados a partir de las imagenes clasificadas'+
            '\nGenerar Collages - Le permite crear collages a partir de las imagenes clasificadas'+
            '\nSalir - Le permite salir del programa')
        case 'ETIQUETAR':
            menu = current_window
            menu.hide()
            etiquetar_imagenes.crear_ventana(menu,current_window.metadata['perfil'])
        case 'MEME':
            menu = current_window
            menu.hide()
            seleccionar_template.crear_ventana(menu,current_window.metadata['perfil'])
        case 'COLLAGE':
            menu = current_window
            menu.hide()
            generador_collage.crear_ventana(menu, current_window.metadata['perfil']['Nick'])
        case 'IMAGEN':
            menu = current_window
            menu.hide()
            modificar_perfil.crear_ventana(menu,current_window.metadata['perfil'])
