import PySimpleGUI as sg
import os
import json
from unlpimage.config import rutas, logs

def guardar(nick,values):
    """Guarda los valores de las rutas a utilizar para las otras pantallas en un json
    
        Args :
            nick (str): nombre del usuario que realiza los cambios
            values (list): lista de los valores que almacenan las nuevas rutas
    """
    
    with open(rutas.RUTA_DIRECTORIOS,'w',encoding= "UTF-8") as archivo:
        direcciones = {'Repositorio' : values['REPOSITORIO'],'Collages' : values['COLLAGES'],'Memes' : values['MEMES']}
        direcciones = dict(map(lambda x: (x[0], rutas.convertir_para_guardar(x[1])), direcciones.items()))
        json.dump(direcciones,archivo)
    logs.actualizar_logs(nick,'Cambio en la configuración del sistema')

def layout():
    """Crea elementos para la ventana.
        
        Returns :
            layout (list): Lista con la informacion de la ventana.
    """
    
    Ruta_repositorio, Ruta_collages, Ruta_memes = rutas.get_rutas()

    columna1 = [
        [sg.Frame('',[
            [sg.Text("Configuracion",text_color = "Black",size = (500,500))]
        ],size = (200,600),border_width = 0,element_justification = "left")]
    ]

    columna2 = [
        [sg.Frame('',[
            [sg.Column([[sg.Text('Repositorio de imagenes')],
            [sg.Input(default_text= Ruta_repositorio,key= 'REPOSITORIO',readonly= True),sg.FolderBrowse("Seleccionar")],
            [sg.Text('Directorio de collages')],
            [sg.Input(default_text= Ruta_collages,key= 'COLLAGES',readonly= True),sg.FolderBrowse("Seleccionar")],
            [sg.Text('Directorio de memes')],
            [sg.Input(default_text= Ruta_memes,key= 'MEMES',readonly= True),sg.FolderBrowse("Seleccionar")]
    ],size=(500,450), pad=(0,0),justification = "center")]],
    element_justification = "center",border_width = 0)]]

    columna3 = [
        [sg.Frame('',[
            [sg.Button("Volver",key = '-CONFIGURACION-VOLVER-')]
    ],border_width = 0,size = (200,500),element_justification = "right")],
        [sg.Frame('',[
            [sg.Button("Guardar",key = '-CONFIGURACION-GUARDAR-')]
    ],border_width = 0,size = (200,100),element_justification = "right")]
    ]

    return [[sg.Column(columna1),sg.Column(columna2),sg.Column(columna3)]]


def crear_ventana(menu,perfil):
    """Crea y devuelve la ventana de configuracion.
    
        Args :
            menu (PySimpleGUI.PySimpleGUI.Window): pantalla del menu para luego ser desencondida.
            perfil (dict): diccionario con los datos del perfil actual.
    """

    return sg.Window('Configuracion',layout(),metadata = {'menu' : menu, 'perfil': perfil},finalize = True)


def procesar_eventos(current_window,event,values):
    """Procesa los eventos de la ventana de configuracion.
        
        Args :
            current_window (PySimpleGUI.PySimpleGUI.Window): Ventana de Configuracion.
            event (str): Nombre del evento producido en la ventana.
            values (dict): Diccionario con los valores de la ventana.
    """

    match event:
        case 'VOLVER':
            current_window.metadata['menu'].un_hide()
            current_window.close()
        case 'GUARDAR':
            guardar(current_window.metadata['perfil']['Nick'],values)
            current_window.metadata['menu'].un_hide()
            current_window.close()