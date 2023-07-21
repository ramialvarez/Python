import os
from PIL import ImageFont, ImageDraw,Image,ImageTk
import PySimpleGUI as sg
from unlpimage.config.rutas import get_rutas,RUTA_PLANTILLAS_MEMES,RUTA_FUENTES
from unlpimage.config import logs

#Constantes
TAMANIO_TEXTO = 16
TAMANIO_TITULO  = 25

def cargar_imagen(nombre_archivo) :
    """Carga la imagen a ser mostrada en pantalla.

        Args:
            nombre_archivo (str): ruta donde se encuentra la imagen a cargar.
        
        Returns:
            imagen (Image): imagen previa para obtener los datos de la misma.
    """
    
    with open(os.path.join(RUTA_PLANTILLAS_MEMES, nombre_archivo), 'rb') as archivo:
        imagen = Image.open(archivo)
        imagen = imagen.copy()
    return imagen
        

def mostrar_imagen(window,imagen):
    """ Actualiza la pantalla con la imagen actualizada y la muestra.

        Args:
            window (PySimpleGUI.PySimpleGUI.Window): Pantalla de memes para ser actualiza con la imagen.
            imagen (PIL.Image.Image): Imagen actualiza que debe ser mostrada en pantalla.
    """
    imagen_lista = ImageTk.PhotoImage(image=imagen)
    window['-IMAGE-'].update(data= imagen_lista)


def tam_box (x1,y1,x2,y2):
    """ Recibe las coordenadas del textbox y retornar el tamaño que va a ocupar.

    Args:
        x1 (int): Coordenada x de la esquina superior izquierda del textbox.
        y1 (int): Coordenada y de la esquina superior izquierda del textbox.
        x2 (int): Coordenada x de la esquina inferior derecha del textbox.
        y2 (int): Coordenada y de la esquina inferior derecha del textbox.

    Returns:
        tuple: Tupla con el ancho y el alto del textbox.
    """
    return (x2- x1, y2 - y1)


def entra(contenedor, contenido):
    """ Recibe el tamaño del textbox y el tamaño del texto y retorna si el texto entra dentro del textbox.

    Args:
        contenedor (tuple): Tupla con los valores (coordenadas x e y) del tamaño que ocupa el textbox
        contenido (tuple): Tupla con los valores (coordenadas x e y) del tamaño que ocupa el texto que desea insertar el usuario en el textbox.

    Returns:
        boolean: Valor booleano que determina si el texto entra dentro del contenedor (textbox).
    """
    
    return contenido[0] <= contenedor[0] and contenido[1] <= contenedor[1]


def calcular_tam_fuente(draw, texto, path_fuente, box):
    """ Calcula el tamaño de la fuente para que el texto entre correctamente en el textbox.

    Args:
        draw (PIL.ImageDraw.ImageDraw): Imagen del meme que debe ser modificado con el texto.
        texto (str): Texto que se debe agregar a la imagen.
        path_fuente (str): Dirección de la fuente del texto.
        box (dict_values): Coordenadas del textbox.

    Returns:
        str: Fuente con el tamaño adecuado para que entre correctamente en el textbox.
    """
    tam_contenedor = tam_box(*box)
    for tam in range(200, 5, -5):
        fuente = ImageFont.truetype(path_fuente,tam)
        box_texto = draw.textbbox((0,0), texto, font= fuente)
        tam_box_texto = tam_box(*box_texto)
        if entra(tam_contenedor, tam_box_texto):
            return fuente
        
    return fuente


def cargar_colores():
    """Carga y ordena los colores a utilizar en la generación de memes.

        Returns:
            colores_ordenados (dict): cada clave es nombre del color y cada valor, el valor del color en hexadecimal.
    """
    colores = {
    'Azul Alicia': '#F0F8FF',
    'Blanco anticuado': '#FAEBD7',
    'Aguamarina': '#7FFFD4',
    'Azur': '#F0FFFF',
    'Beige': '#F5F5DC',
    'Bizcocho': '#FFE4C4',
    'Negro': '#000000',
    'Almendra blanqueada': '#FFEBCD',
    'Azul': '#0000FF',
    'Azul violaceo': '#8A2BE2',
    'Marrón': '#A52A2A',
    'Burlywood': '#DEB887',
    'Azul cadete': '#5F9EA0',
    'Cartujo': '#7FFF00',
    'Chocolate': '#D2691E',
    'Coral': '#FF7F50',
    'Azul maíz': '#6495ED',
    'Cornsilk': '#FFF8DC',
    'Cian': '#00FFFF',
    'Azul oscuro': '#00008B',
    'Cian oscuro': '#008B8B',
    'Dorado oscuro': '#B8860B',
    'Verde oscuro': '#006400',
    'Gris oscuro': '#A9A9A9',
    'Caqui oscuro': '#BDB76B',
    'Magenta oscuro': '#8B008B',
    'Verde oliva oscuro': '#556B2F',
    'Naranja oscuro': '#FF8C00',
    'Orquidia oscuro': '#9932CC',
    'Rojo oscuro': '#8B0000',
    'Salmón oscuro': '#E9967A',
    'Verde marino oscuro': '#8FBC8F',
    'Azul pizarra oscuro': '#483D8B',
    'Gris pizarra oscuro': '#2F4F4F',
    'Turquesa oscuro': '#00CED1',
    'Violeta oscuro': '#9400D3',
    'Rosa fuerte': '#FF1493',
    'Celeste fuerte': '#00BFFF',
    'Gris apagado': '#696969',
    'Azul dodger': '#1E90FF',
    'Ladrillo': '#B22222',
    'Blanco Floral': '#FFFAF0',
    'Verde bosque': '#228B22',
    'Gainsboro': '#DCDCDC',
    'Blanco fantasma': '#F8F8FF',
    'Dorado': '#FFD700',
    'Verde': '#00FF00',
    'Verde amarillento': '#ADFF2F',
    'Gris': '#BEBEBE',
    'Miel': '#F0FFF0',
    'Rosa caliente': '#FF69B4',
    'Rojo indio': '#CD5C5C',
    'Marfil': '#FFFFF0',
    'Caqui': '#F0E68C',
    'Lavanda': '#E6E6FA',
    'Lavanda brilloso': '#FFF0F5',
    'Verde pasto': '#7CFC00',
    'Limón chiffon': '#FFFACD',
    'Azul claro': '#ADD8E6',
    'Coral claro': '#F08080',
    'Cian claro': '#E0FFFF',
    'Dorado claro': '#EEDD82',
    'Gris claro': '#D3D3D3',
    'Verde claro': '#90EE90',
    'Rosa claro': '#FFB6C1',
    'Salmón claro': '#FFA07A',
    'Verde marino claro': '#20B2AA',
    'Celeste claro': '#87CEFA',
    'Azul pizarra claro': '#8470FF',
    'Gris pizarra claro': '#778899',
    'Azul metálico claro': '#B0C4DE',
    'Amarillo claro': '#FFFFE0',
    'Verde lima': '#32CD32',
    'Lino': '#FAF0E6',
    'Magenta': '#FF00FF',
    'Granate': '#B03060',
    'Aguamarina medio': '#66CDAA',
    'Azul medianoche': '#191970',
    'Menta cremoso': '#F5FFFA',
    'Rosa mentolado': '#FFE4E1',
    'Mocasín': '#FFE4B5',
    'Blanco navajo': '#FFDEAD',
    'Azul marino': '#000080',
    'Lazo antiguo': '#FDF5E6',
    'Oliva': '#6B8E23',
    'Naranja': '#FFA500',
    'Naranja rojo': '#FF4500',
    'Orquidia': '#DA70D6',
    'Papaya': '#FFEFD5',
    'Durazno': '#FFDAB9',
    'Peru': '#CD853F',
    'Rosa': '#FFC0CB',
    'Ciruela': '#DDA0DD',
    'Azul polvo': '#B0E0E6',
    'Purpura': '#A020F0',
    'Rojo': '#FF0000',
    'Marron rosado': '#BC8F8F',
    'Azul real': '#4169E1',
    'Marrón montura': '#8B4513',
    'Salmón': '#FA8072',
    'Marrón arena': '#F4A460',
    'Verde agua': '#2E8B57',
    'Caracol': '#FFF5EE',
    'Siena': '#A0522D',
    'Celeste': '#87CEEB',
    'Azul pizarra': '#6A5ACD',
    'Gris pizarra': '#708090',
    'Nieve': '#FFFAFA',
    'Verde primavera': '#00FF7F',
    'Azul metálico': '#4682B4',
    'Bronceado': '#D2B48C',
    'Thistle': '#D8BFD8',
    'Tomate': '#FF6347',
    'Turquesa': '#40E0D0',
    'Violeta': '#EE82EE',
    'Violeta rojizo': '#D02090',
    'Maíz': '#F5DEB3',
    'Blanco': '#FFFFFF',
    'Blanco humo': '#F5F5F5',
    'Amarillo': '#FFFF00',
    'Amarillo verdoso': '#9ACD32',
    }

    claves = sorted(colores.keys())
    colores_ordenados = {clave:colores[clave] for clave in claves}

    return colores_ordenados


def layout(template,colores):
    """Crea elementos para la ventana.

        Args:
            template (dict) = Datos del template elegido para generar las multilineas.
            colores (dict) = Colores para las fuentes que se usan para ser cargados en el combo de la ventana.

        Returns:
            layout (list): Lista con la informacion de la ventana. 
    """

    ancho_ventana = 1100

    fuentes = [fuente.replace('.ttf','') for fuente in os.listdir(RUTA_FUENTES)]

    columna_archivos = [[sg.Text('Fuente:'),sg.Combo(values=fuentes, size=(40,15),default_value=fuentes[0],
                                                     enable_events=True,readonly=True, key='-MEME-COMBO-')],
                        [sg.Text('Color:'),sg.Combo(values=list(colores.keys()), size=(30,15),default_value=list(colores.keys())[0],
                                                     enable_events=True,readonly=True, key='-MEME-COLOR-'),
                                                     sg.Text('  ',background_color=colores[list(colores.keys())[0]],key='-PREVIEW-')]]
    
    for num,textbox in enumerate(template['text_boxes']):
        columna_archivos.append([sg.Text(f'Texto {num+1}')])
        columna_archivos.append([sg.Multiline(size= (50,3),font= (fuentes[0],10),no_scrollbar=True,
                                              k=f'-MEME-MULTI{num}-',metadata=textbox,tooltip='Escriba el texto como quiere que aparezca en la imagen')])
        
    columna_archivos.append([sg.Button("Actualizar", size=(25,2),k='-MEME-ACTUALIZAR-')])

    columna_imagenes = [[sg.Frame('',[
              [sg.Text(size=(40,1), key='-NOMBRE-')],
              [sg.Image(key='-IMAGE-')],
              [sg.Text('Nombre del meme')],
              [sg.Column([[sg.In(k='-NOMBREMEME-'),sg.Combo(readonly=True,values=['.png','.jpg'],default_value='.png',k='-FORMATO-')]])]
              ],key='-FRAMEIMG-')
              ]
    ]

    encabezado = [
        [
            
            sg.Frame('',
                [[sg.Text("Generar meme", font=('Rockwell', 20),justification= 'left')]], 
                element_justification="left",border_width = 0,size=(ancho_ventana//2,100)),
            sg.Frame('',
                [[sg.Button("Volver",key= '-MEME-VOLVER-')]], 
                element_justification="right",border_width = 0,size=(ancho_ventana//2,80))
                
        ]
    ]

    return [
    [encabezado],
    [sg.Frame('',
                [[sg.Column(columna_archivos, element_justification='c',size=(ancho_ventana//2,600),key='-COLUMARCH-'), 
                  sg.VSeperator(),
                  sg.Column(columna_imagenes, element_justification='c',key='-COLUMIMG-'),
                  ]],border_width = 0,size=(ancho_ventana,500)),

    ],
    [sg.Frame('',
                [[sg.Button("Guardar",key= '-MEME-GUARDAR-')]], 
                element_justification="right",border_width = 0,size=(ancho_ventana,80))]
    ]

def crear_ventana(menu,template,perfil) :
    """Crea la ventana del generador de memes.
        
        Args:
            menu (PySimpleGUI.PySimpleGUI.Window) = pantalla del menu para luego ser desencondida.
            template (dict) = Datos del template elegido.
            perfil (dict) = Datos del perfil que accede a la ventana.

        Returns:
            window (PySimpleGUI.PySimpleGUI.Window): Ventana del generador de memes.
    """
    colores = cargar_colores()
    window = sg.Window("Generador de memes", layout(template,colores), margins=(10,10), finalize=True,
                       metadata={'menu':menu,'template':template,'perfil':perfil,'colores':colores})
    window.metadata['meme_original'] = cargar_imagen(template['image'])
    mostrar_imagen(window,window.metadata['meme_original'])
    return window


def procesar_eventos(current_window, event, values) :
    """Procesa los eventos de la ventana generador de memes.
    
        Args:
            current_window (PySimpleGUI.PySimpleGUI.Window) = Ventana de Generador de memes.
            event (str) = Nombre de el evento producido en la ventana.
            values (dict) = Diccionario con los valores de la ventana.
    """
    
    match event :
        case 'VOLVER':
            current_window.metadata['menu'].un_hide()
            current_window.close()
        case 'ACTUALIZAR' | 'COMBO' | 'COLOR':
            current_window.metadata['meme'] = current_window.metadata['meme_original'].copy()
            meme = current_window.metadata['meme']
            draw = ImageDraw.Draw(meme)
            ruta_fuente = os.path.join(RUTA_FUENTES,f"{values['-MEME-COMBO-']}.ttf")
            current_window['-PREVIEW-'].update(background_color=current_window.metadata['colores'][values['-MEME-COLOR-']])
            for num,textbox in enumerate(current_window.metadata['template']['text_boxes']):
                valores_textbox = textbox.values()
                texto = values[f'-MEME-MULTI{num}-']
                fuente = calcular_tam_fuente(draw, texto, ruta_fuente, valores_textbox)
                draw.text((textbox['top_left_x'],textbox['top_left_y']), texto, font= fuente, fill= current_window.metadata['colores'][values['-MEME-COLOR-']])
            mostrar_imagen(current_window,meme)
        case 'GUARDAR':
            nombre = values['-NOMBREMEME-']
            if nombre != '':
                meme = current_window.metadata['meme']
                ruta_guardado = os.path.join(get_rutas('memes'), f"{nombre}{values['-FORMATO-']}")
                pop_up = 'Yes'
                if (os.path.exists(ruta_guardado)):
                    pop_up = sg.popup_yes_no("Ya existe un meme con ese nombre en el repositorio, ¿deseas reemplazarlo?")
                if pop_up != "No":
                    meme.convert(mode='RGB').save(ruta_guardado)
                    for num,textbox in enumerate(current_window.metadata['template']['text_boxes']):
                        if num == 0:
                            texto = values[f'-MEME-MULTI{num}-'].replace('\n',' ')
                        else:
                            texto = texto + ';' + values[f'-MEME-MULTI{num}-'].replace('\n',' ')
                    logs.actualizar_logs(current_window.metadata['perfil']['Nick'],'Nuevo meme',valores=current_window.metadata['template']['image'],textos=texto)
                    current_window.metadata['menu'].un_hide()
                    current_window.close()
            else:
                sg.popup('Ningun nombre fue ingresado, intentelo de vuelta',title='Error')