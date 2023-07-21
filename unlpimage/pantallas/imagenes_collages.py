import PySimpleGUI as sg
import os
import csv
from PIL import Image, ImageTk, ImageDraw, ImageOps
from unlpimage.config import rutas, logs
import json
import random
import string

#Constantes
TAMANIO_TEXTO = 16
TAMANIO_TITULO  = 25

def generar_cadena_aleatoria(longitud):
    """Genera un String aleatorio para luego ser usado en el titulo del collage.
    
        Args:
            longitud = cantidad de caracteres en la cadena a crear.
        Returns :
            cadena = String generado aleatoriamente.
    """
    caracteres = string.ascii_letters + string.digits + string.punctuation
    cadena = ''.join(random.choice(caracteres) for _ in range(longitud))
    return cadena

def mostrar_imagen(lista_imagenes, nombre_plantilla, lista_posiciones, current_window, lista_tamanios, guardar, texto='Collage'):
    """Agrega imagen en la plantilla del collage.
    
        Args:
            lista_imagenes = lista de str con los nombres de las imagenes seleccionadas por el usuario para utilizar en el collage.
            nombre_plantilla (str) = Nombre de la plantilla elegida previamente.
            lista_coordenadas = lista de listas con las coordenadas [x, y] para posicionar cada imagen en el collage.
            current_window (PySimpleGUI.Window) = Ventana actual.
            texto (str) = texto ingresado por el usuario en el input.
            lista_tamanio = lista de enteros con los tamanios para cada imagen seleccionda por el usuario.
    """
    imagenes = []
    for archivo in lista_imagenes:
        if archivo != ' ':
            ruta_imagen = os.path.join(rutas.get_rutas('repositorio'), archivo)
            imagen = Image.open(ruta_imagen)
            imagenes.append(imagen)
        else :
            imagenes.append(' ')
    plantilla = Image.open(os.path.join(rutas.RUTA_PLANTILLAS_COLLAGES, nombre_plantilla))
    copia_plantilla = plantilla.copy()

    i = 0
    for imagen in imagenes :
        if (imagen != ' ') :
            imagen = ImageOps.fit(imagen,lista_tamanios[i])
            copia_plantilla.paste(imagen, lista_posiciones[i])
        i += 1

    draw = ImageDraw.Draw(copia_plantilla)
    draw.text((10, 10), texto,bold = True, fill= (255, 0, 0))
    
    if (guardar) :
        ruta_guardar = rutas.get_rutas('collages')

        #Si el usuario no ingreso un titulo, se le genera uno aleatorio hasta encontrar uno que no exista
        if texto == 'Collage' :
            texto += generar_cadena_aleatoria(5)
            while (texto in ruta_guardar) :
                texto += generar_cadena_aleatoria(1)

        if (texto in ruta_guardar) :
            sg.Popup('El titulo ingresado ya existe. Por favor, ingrese otro')
        else :
            #chequeamos si el usuario ya le agrego la extension o no
            extensiones = ('png','jepg','jpg','gif')
            if not (texto.endswith(extensiones)) :
                texto+='.png'
            ruta_guardar = os.path.join(os.getcwd(), ruta_guardar, texto)
            copia_plantilla.save(ruta_guardar, format='png')
            sg.Popup('La imagen se guardo exitosamente')

    imagen_mostrar = ImageTk.PhotoImage(copia_plantilla)
    current_window['-IMAGENES-IMAGE-'].update(data=imagen_mostrar, size=(400, 400))

def crear_collage (plantilla, values, current_window, guardar=False) :
    """Abre el archivo json donde se almacenan los datos de cada plantilla para generar el collage: una lista con las posiciones y 
        con los tamanios de cada imagenes. Además, una lista con elementos vacios según la cantidad de espacios que tiene la plantilla 
        para las fotos.
        Luego genera una iteracion según la cantidad de espacios que tiene la plantilla para fotos, en donde se guarda en la lista 
        con valores vacios, previamente creada, los nombres de las imagenes selecciondas por el usuario. 
        Finalmente, llama a otra funcion que pega las imagenes seleccionas por el usuario en la plantilla elegida.

       Args :
            plantilla = cadena de caracteres con la plantilla seleccionada por el usuario.
            values = diccionadio de listas con las imagenes seleccionadas por el usuario para utilizar en el collage.
            current_window (PySimpleGUI.PySimpleGUI.Window) = ventana actual.
    """
    with open(rutas.RUTA_DATOS_COLLAGES, "r") as archivo:
        datos = json.load(archivo)
        lista_posiciones = datos[plantilla]['lista_posiciones']
        lista_tamanios= datos[plantilla]['lista_tamanios']
        lista_imagenes = datos[plantilla]['lista_imagenes']
    
    for i in range(0, int(plantilla[0]), 1) :
        if (values['-IMAGENES-IMAGEN_'+str(i)]) :
            lista_imagenes[i] = values['-IMAGENES-IMAGEN_'+str(i)][0]

    if (values['TEXTO']) :
        mostrar_imagen(lista_imagenes, plantilla, lista_posiciones, current_window, lista_tamanios, guardar, values['TEXTO'])
    else :
        mostrar_imagen(lista_imagenes, plantilla, lista_posiciones, current_window, lista_tamanios, guardar)
    current_window.metadata['imagenes'] = lista_imagenes
    
def evaluar_plantilla (plantilla) :
    """Devuelve una cadena de caracteres con la imagen a mostrar segun la plantilla que haya seleccionado el usuario.
    
        Args :
            plantilla = string, llave de la imagen seleccionada.
        Returns :
            string con el nombre de la imagen a mostrar.
    """
    match plantilla :
        case "2fotos" :
            return "2fotos.png"
        case "4fotos" :
            return "4fotos.png"
        case "3fotos" :
            return "3fotos.png"
        case _:
            return "4arriba.png" 

def tiene_tags(im):
    """Chequea si la imagen enviada por parámetro tiene o no tags
    
        Args: 
            im (str) = Nombre de la imagen a mostrar
        Returns:
            ok (bool) = Booleano que termina en verdadero en caso de que la imagen tenga tags y falso en caso contrario.
    """
    ok = False
    try:
        with open(rutas.RUTA_DATOS_IMAGENES, 'r', encoding="UTF-8") as archivo:
            imagenes = list(csv.DictReader(archivo))
            imagenes_filtradas = list(filter(lambda x: x["ruta"] == im, imagenes))
            if imagenes_filtradas and imagenes_filtradas[0]["tags"] != '':
                ok = True
    except FileNotFoundError:
        return ok
    return ok

def layout (plantilla) :
    """Crea los elementos del generador de collages.
            
        Args :
            plantilla = diccionario con el tipo de plantilla del collage.
        Returns  :
            lista con elementos de la ventana.
    """
    imagen_plantilla = evaluar_plantilla(plantilla)

    Ruta_repositorio = rutas.get_rutas('repositorio')
    try:
        imagenes = os.listdir(Ruta_repositorio)         
    except:
        imagenes = []
    
    nombres_imagenes = [im for im in imagenes if os.path.isfile(
    os.path.join(Ruta_repositorio, im)) and im.lower().endswith((".png", ".jpg", "jpeg", ".tiff", ".bmp")) and tiene_tags(im)]

    encabezado = [
            [sg.Button("Volver",key='-IMAGENES-VOLVER-'),
            sg.Text("Generador de collage", font=('Rockwell', TAMANIO_TITULO), justification="center", pad = (290,1))],
    ]

    columna1 = [
        [sg.Listbox(values=nombres_imagenes, enable_events=True, size=(10,10),key=f"-IMAGENES-IMAGEN_{i}") for i in range(0,int(plantilla[0]),1)]   
    ]

    columna2 = [
            [sg.Image(filename=os.path.join(rutas.RUTA_PLANTILLAS_COLLAGES,imagen_plantilla),key='-IMAGENES-IMAGE-')]
    ]

    columna3 = [
        [sg.Button("Generar collage",key='-IMAGENES-GENERAR-')]
    ]

    columna4 = [
    [sg.Text('Titulo:', font=('Rockwell', TAMANIO_TEXTO))],
    [sg.InputText(key='TEXTO')]
   ]

    return [
    [sg.Column(layout=encabezado)],
    [
        sg.Column(
            layout=columna1, 
            justification="center", 
        ),
        sg.Column(
            layout=columna2, 
            justification="center", 
        ),
        sg.Column(
            layout=columna4, 
            justification="center", 
        )
    ],
    [sg.Column(
            layout=columna3, 
            justification="center", 
        )
    ]
    ]

def crear_ventana (plantilla, collage, nick_usuario) :
    """Crea la ventana del generador de collages.
        
        Args :
            plantilla = diccionario con el tipo de plantilla del collage.
            collage (PySimpleGUI.PySimpleGUI.Window) = pantalla del collage para luego ser desencondida.
            nick_usuario = nick que esta generando un collage.
    """
    return sg.Window("Generador de collages", layout(plantilla), margins=(100,100), background_color='white', metadata = {'collage':collage, 'nick_usuario':nick_usuario, 'plantilla':plantilla+'.png', 'imagenes':' '},finalize=True, resizable=True)

def procesar_eventos (current_window, event, values) :
    """Procesa los eventos de la ventana generador de collages.
        
        Args :
            current_window (PySimpleGUI.PySimpleGUI.Window) = Ventana de Generador de collages.
            event (str) = Nombre de el evento producido en la ventana.
            values (dict) = Diccionario con los valores de la ventana.
    """
    match event :
        case 'VOLVER':
            current_window.metadata['collage'].un_hide()
            current_window.close()
        case 'GENERAR' :
            crear_collage(current_window.metadata['plantilla'], values, current_window, True)

            separador = ';'
            cadena = separador.join(current_window.metadata['imagenes'])
            logs.actualizar_logs(current_window.metadata['nick_usuario'],'Nuevo collage', cadena, values['TEXTO'])

        case _ :
            crear_collage(current_window.metadata['plantilla'], values, current_window)