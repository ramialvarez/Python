import PySimpleGUI as sg
from datetime import datetime
import os.path
from PIL import Image, ImageTk
from unlpimage.config import logs
from unlpimage.config.rutas import get_rutas, RUTA_DATOS_IMAGENES, RUTA_BOTONES
import csv

def cargar_imagen(nombre_archivo) :
    """Carga la imagen a ser mostrada en pantalla
        Args :
            nombre_archivo (str): ruta donde se encuentra la imagen a cargar
        Returns :
            imagen_lista (ImageTk.PhotoImage): imagen lista para ser mostrada en pantalla
            imagen (Image): imagen previa para obtener los datos de la misma.
    """
    
    with open(nombre_archivo, 'rb') as archivo:
        imagen = Image.open(archivo)
        imagen_redimensionada = imagen
        imagen_redimensionada.thumbnail((450,400))
        imagen_lista = ImageTk.PhotoImage(image=imagen_redimensionada)
    return imagen_lista, imagen


def cargar_archivo():
    """Carga el archivo que contiene la informacion de las imagenes
        Returns :
            imagenes (list): lista con la informacion almacenada por el momento. 
    """
    
    try:
        with open(RUTA_DATOS_IMAGENES,'r',newline='') as archivo:
                imagenes = list(csv.DictReader(archivo))
        for imagen in imagenes:
            if imagen['tags'] == '':
                imagen['tags'] = []
            else:
                imagen['tags'] = list(elem for elem in imagen['tags'].split(";"))
            imagen['nueva'] = False
            imagen['modificada'] = False
    except FileNotFoundError:
        imagenes = []
    return imagenes


def cargar_datos_imagen(window,imagen):
    """Carga los datos de la imagen actual en pantalla.
        Args :
            window(PySimpleGUI.PySimpleGUI.Window): pantalla actual para actualizar la informacion
            imagen(dict): diccionario con los datos de la imagen.
    """
    
    window['-NOMBRE-'].update(imagen['ruta'])
    window['-DATOS-'].update(visible=True)
    window['-TAMANO-'].update(f"{imagen['tamano']} MB")
    window['-RESOLUCION-'].update(imagen['resolucion'])
    window['-TIPO-'].update(imagen['tipo'])
    if imagen['descripcion'] != '':
        window['-DESEN-'].update(visible = True)
    else:
        window['-DESEN-'].update(visible = False)
    window['-DESCRIPCION-'].update(imagen['descripcion'])
    cargar_tags(window,imagen)


def cargar_tags(window,imagen):
    """Carga los tags de la imagen actual en pantalla
        Args :
            window(PySimpleGUI.PySimpleGUI.Window): pantalla actual para actualizar la informacion.
            imagen(dict): diccionario con los datos de la imagen.
    """
    
    for nom in window.metadata['tags']:
        window[nom].update(visible=False)
    window.metadata['tags'].clear()
    if imagen['tags'] != []:
        window['-FRAMETAGS-'].update(visible = True)
        for num,tag in enumerate(imagen['tags']):
            if (num < window.metadata["siguiente"]):
                window[f'CB{num}'].update(text = tag,visible = True)
                window.metadata['tags'].append(f'CB{num}')
            else:
                window.extend_layout(window['-FILATAGS-'],[[sg.pin(sg.CB(tag,key=f'CB{window.metadata["siguiente"]}'))]])
                window.metadata['tags'].append(f'CB{window.metadata["siguiente"]}')
                window.metadata["siguiente"] += 1
    else:
        window['-FRAMETAGS-'].update(visible = False)


def layout():
    """Crea elementos para la ventana
    Returns :
        layout (list): Lista con la informacion de la ventana.
    """

    ancho_ventana = 1100
    
    Ruta_repositorio = get_rutas('repositorio')
    try:
        imagenes = os.listdir(Ruta_repositorio)         
    except:
        imagenes = []
    nombres_imagenes = [im for im in imagenes if os.path.isfile(
    os.path.join(Ruta_repositorio, im)) and im.lower().endswith((".png", ".jpg", "jpeg", ".tiff", ".bmp")) 
    and (not('meme' in im.lower()))]

    columna_archivos = [[sg.Listbox(values=nombres_imagenes, enable_events=True, size=(40,15),key='-ETIQUETAR-LISTA-')],
                    [sg.Text('Tag',justification='left')],
                    [sg.In(key='-TAGIN-',tooltip='Ingrese un tag, evite usar el caracter ;',do_not_clear=False),
                     sg.Button('Agregar',key='-ETIQUETAR-GUARDARTAG-')],
                    [sg.Text('Texto descriptivo',justification='left')],
                    [sg.In(key='-DESCRIPCIONIN-',tooltip='Ingrese una descripcion de la imagen actual',do_not_clear=False),
                     sg.Button('Agregar',key='-ETIQUETAR-GUARDARDES-')]
            ]
    columna_imagenes = [[sg.Frame('',[
              [sg.Text(size=(40,1), key='-NOMBRE-')],
              [sg.Image(filename = os.path.join(RUTA_BOTONES,'Defecto.png'),key='-IMAGE-')],
              [sg.Column([[sg.Text(key='-TIPO-',),sg.VerticalSeparator(),
                           sg.Text(key='-TAMANO-'),sg.VerticalSeparator(),sg.Text(key='-RESOLUCION-')],
              [sg.Text('Descripcion',size=(40,1), key='-DESEN-',visible=False)],
              [sg.Text(size=(40,1), key='-DESCRIPCION-')],
              ],key='-DATOS-',visible=False)]
              ],key='-FRAMEIMG-')
              ]
    ]
    
    columna_tags = [[sg.Frame('',[
              [sg.Text('Tags',size=(40,1), key='-TAGSEN-')],
              [sg.Col([],key='-FILATAGS-')],
              [sg.Button('Borrar',k='-ETIQUETAR-BORRARTAG-')]
              ],visible=False,k='-FRAMETAGS-')
              ]
    ]

    encabezado = [
        [
            
            sg.Frame('',
                [[sg.Text("Etiquetar imagenes", font=('Rockwell', 20),justification= 'left')]], 
                element_justification="left",border_width = 0,size=(ancho_ventana//2,100)),
            sg.Frame('',
                [[sg.Button("Volver",key= '-ETIQUETAR-VOLVER-')]], 
                element_justification="right",border_width = 0,size=(ancho_ventana//2,80))
                
        ]
    ]

    return [
    [encabezado],
    [sg.Frame('',
                [[sg.Column(columna_archivos, element_justification='c',size=(ancho_ventana//2.5,600),key='-COLUMARCH-'), 
                  sg.VSeperator(),
                  sg.Column(columna_imagenes, element_justification='c',key='-COLUMIMG-'),
                  sg.Column(columna_tags, element_justification='c')
                  ]],border_width = 0,size=(ancho_ventana,500)),

    ],
    [sg.Frame('',
                [[sg.Button("Guardar",key= '-ETIQUETAR-GUARDAR-')]], 
                element_justification="right",border_width = 0,size=(ancho_ventana,80))]
    ]

def crear_ventana(menu,perfil):
    """Crea la ventana de etiquetar imagen
    Args :
        menu (PySimpleGUI.PySimpleGUI.Window): pantalla del menu para luego ser desencondida
        perfil (dict): diccionario con los datos del perfil actual.
    Returns :
        ventana de etiquetar imagenes.
    """
    
    return sg.Window('Etiquetar imagenes', layout(),finalize=True,metadata=
                     {'tags' : [],'siguiente': 0,'imagen_actual': None,'menu' : menu,'imagenes': cargar_archivo(),'perfil': perfil})


def procesar_eventos(current_window,event,values):
    """Procesa los eventos de la pantalla de etiquetar imagenes
        Args :
            current_window (PySimpleGUI.PySimpleGUI.Window): Ventana de Etiquetar.
            event (str): Nombre del evento producido en la ventana.
            values (dict): Diccionario con los valores de la ventana.
    """
    
    match event:

        case 'VOLVER':
            current_window.metadata['menu'].un_hide()
            current_window.close()

        case 'LISTA':
            nombre = values['-ETIQUETAR-LISTA-'][0]
            ruta = os.path.join(get_rutas('repositorio'), nombre)
            imagen_lista,imagen_pil = cargar_imagen(ruta)
            current_window.metadata['imagen_actual'] = None
            timestamp = int(datetime.timestamp(datetime.now()))
            for numero,img in enumerate(current_window.metadata['imagenes']):
                if (nombre == img['ruta']):
                    current_window.metadata['imagen_actual'] = numero
                    imagen = img
                    imagen['ultimo_perfil'] = current_window.metadata['perfil']['Nick']
                    imagen['ultima_actualizacion'] = timestamp
                    break
            if current_window.metadata['imagen_actual'] == None:
                imagen = {'ruta' : nombre,
                    'descripcion' : '',
                    'resolucion' : f'{imagen_pil.size[0]}x{imagen_pil.size[1]}',
                    'tamano': round(os.path.getsize(ruta)/1024/1024,2),
                    'tipo' : imagen_pil.format,
                    'tags': [],
                    'ultimo_perfil': current_window.metadata['perfil']['Nick'],
                    'ultima_actualizacion': timestamp,
                    'nueva': True,
                    'modificada': False
                    }
                current_window.metadata['imagen_actual'] = len(current_window.metadata['imagenes'])
                current_window.metadata['imagenes'].append(imagen)
            current_window['-IMAGE-'].update(data=imagen_lista)
            cargar_datos_imagen(current_window,imagen)

        case 'GUARDARTAG':
            numero = current_window.metadata['imagen_actual']
            if numero != None and values['-TAGIN-'] != '':
                current_window['-FRAMETAGS-'].update(visible = True)
                imagen = current_window.metadata['imagenes'][current_window.metadata['imagen_actual']]
                imagen['tags'].append(values['-TAGIN-'])
                imagen['modificada'] = True
                cargar_tags(current_window,imagen)

        case 'BORRARTAG':
            imagen = current_window.metadata['imagenes'][current_window.metadata['imagen_actual']]
            borrar_tags = []
            for nom,tag in zip(current_window.metadata['tags'],imagen['tags']):
                if values[nom]:
                    borrar_tags.append(tag)
            for tag in borrar_tags:
                imagen['tags'].remove(tag)
            imagen['modificada'] = True
            cargar_tags(current_window,imagen)

        case 'GUARDARDES':
            numero = current_window.metadata['imagen_actual']
            if numero != None and values['-DESCRIPCIONIN-'] != '':
                current_window['-DESEN-'].update(visible = True)
                current_window.metadata['imagenes'][numero]['descripcion'] = values['-DESCRIPCIONIN-']
                current_window['-DESCRIPCION-'].update(values['-DESCRIPCIONIN-'])
                current_window.metadata['imagenes'][numero]['modificada'] = True

        case 'GUARDAR':
            with open(RUTA_DATOS_IMAGENES,'w',newline='') as archivo:
                fieldnames = ['ruta','descripcion','resolucion','tamano','tipo','tags','ultimo_perfil','ultima_actualizacion']
                writer = csv.DictWriter(archivo, fieldnames=fieldnames)
                writer.writeheader()
                for imagen in current_window.metadata['imagenes']:
                    if((imagen['nueva']) and imagen['modificada']) or not(imagen['nueva']):
                        tags = ''
                        for num,elem in enumerate(imagen['tags']):
                            if num == 0:
                                tags = elem
                            else:
                                tags = tags + f';{elem}'
                        imagen['tags'] = tags
                        if (imagen['modificada']):
                            if(imagen['nueva']):
                                logs.actualizar_logs(imagen['ultimo_perfil'],'Nueva imagen clasificada',timestamp=imagen['ultima_actualizacion'])
                            else:
                                logs.actualizar_logs(imagen['ultimo_perfil'],'Modificación de imagen previamente clasificada',timestamp=imagen['ultima_actualizacion'])
                        del imagen['nueva']
                        del imagen['modificada']
                        writer.writerow(imagen)
            current_window.metadata['menu'].un_hide()
            current_window.close()