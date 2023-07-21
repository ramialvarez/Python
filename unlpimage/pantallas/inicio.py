import os
import PySimpleGUI as sg
import json
from unlpimage.pantallas import menu_principal as mp
from unlpimage.pantallas import nuevo_perfil as np
from unlpimage.config.rutas import RUTA_BOTONES, RUTA_IMAGENES_USUARIOS, RUTA_JSON

def cargar_perfiles():
    """Esta función abre el archivo json donde se encuentran los perfiles si es posible, y los retorna como una lista de diccionarios.

        Returns :
            perfiles (dict): Diccionario de diccionarios con los datos de cada perfil.
    """
    try:
         with open(RUTA_JSON,'r') as archivo:
             perfiles = json.load(archivo)
    except FileNotFoundError: 
        perfiles = {} 
    return perfiles

def crear_layout(perfiles,boton_ver_mas):
    """Esta funcion crea el layout con las imagenes y los nombres de cada perfil, el nombre de la app, el botón de agregar, y el botón de ver más.

        Args :
            perfiles (dict): Lista de diccionarios con la información de los perfiles.
            boton_ver_mas (list): Lista con el botón ver más.

        Returns :
            layout (list): Lista con el layout de la ventana de inicio.
    """
    images = [sg.Image(source= os.path.join(RUTA_IMAGENES_USUARIOS,perfil.get("-NUEVO_PERFIL-RUTA_AVATAR-")), size=(200, 200), metadata= perfil,key=f"-INICIO-ABRIR-{perfil.get('Nick').replace(' ', '')}", enable_events= True,pad=((0,0),(0,10))) for perfil in perfiles.values() ] + [sg.Button(image_filename=os.path.join(RUTA_BOTONES,'boton_agregar.png'), button_color=(None, None), image_size=(200,200),pad=((0,0),(0,10)), key='-INICIO-AGREGAR-')],
    names = [sg.Text(perfil.get("Nick"), font=('Rockwell', 15),size= (17,17),justification='center') for perfil in perfiles.values()]
    layout = [
        [sg.Text('UNLPImage', font=('Rockwell', 25), text_color='purple', justification='left')],
        [sg.Push(),sg.Text('Perfiles', font=('Rockwell', 20), text_color='#FFFF66'),sg.Push()],
        [images],
        [names],
        [boton_ver_mas],
        [sg.VPush()],
    ]
    
    return layout

def crear_ventana(ver_mas = None):
    """Crea la ventana de Inicio.
    
        Args :
            ver_mas (boolean): Valor booleano para crear la ventana con todos los perfiles y sin el boton ver más en caso de que el usuario aprete este botón.

        Returns :
            window (PySimpleGUI.PySimpleGUI.Window): Ventana de Inicio.
    """
    perfiles = cargar_perfiles()
    if len(perfiles) < 3 or ver_mas == True:
        perfiles_mostrados = list(perfiles.items())[3:]
        boton_ver_mas = []
    elif len(perfiles) >= 3:
        perfiles_mostrados = list(perfiles.items()) [:3]
        boton_ver_mas = [sg.Push(),sg.Button('Ver más', key='-INICIO-VER_MAS-'),sg.Push()],
    
    perfiles_mostrados = dict(perfiles_mostrados)
    layout = crear_layout(perfiles_mostrados,boton_ver_mas)
    
    return sg.Window('Inicio', layout,size=(1000, 800),finalize= True,resizable=True)
    
def procesar_eventos(current_window,event,usuario):
    """Abre la ventana de inicio y controla sus eventos.

        Args :
            current_window (PySimpleGUI.PySimpleGUI.Window): Ventana de Inicio.
            event (str): Nombre del evento producido en la ventana.
            usuario (str): Nick del usuario, utilizado como clave para pasarle la información del perfil seleccionado a la pantalla del Menú Principal.
    """  
    perfiles = cargar_perfiles()
            
    match event:
        case 'AGREGAR':
            inicio = current_window
            inicio.hide()
            np.crear_ventana(inicio)
        case "ABRIR":
            current_window.close()    
            usuario_seleccionado = perfiles[usuario]         
            mp.crear_ventana(usuario_seleccionado)
        case 'VER_MAS':
            current_window.close()
            crear_ventana(True)
