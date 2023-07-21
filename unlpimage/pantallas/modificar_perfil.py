import json
import os
from PIL import Image, ImageTk
import PySimpleGUI as sg
from unlpimage.config import logs
from unlpimage.config.rutas import RUTA_IMAGENES_USUARIOS, RUTA_JSON
import base64
import io

#Constantes
TAMANIO_TEXTO = 16
TAMANIO_TITULO  = 25
green_pill64 = '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'
button64 = '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'

def image_file_to_bytes(image64, size):
    image_file = io.BytesIO(base64.b64decode(image64))
    img = Image.open(image_file)
    img.thumbnail(size, Image.ANTIALIAS)
    bio = io.BytesIO()
    img.save(bio, format='PNG')
    imgbytes = bio.getvalue()
    return imgbytes

def buscar (nick) :
    """Busca un nick en el archivo json.
        
        Args :
            nick = alias del perfil a buscar.
        
        Returns :
            pos = posicion de la lista de diccionarios del archivo json.
    """
    with open(RUTA_JSON, 'r') as archivo_json:
            buscar = json.load(archivo_json)
            pos = 0
            for elem in buscar :
                if elem ==  nick :
                    break
                pos+=1
    return pos

def cambiar_imagen (ruta_avatar) :
    """Cambia la imagen seleccionada como "foto de perfil" y la retorna.
        
        Args : 
            ruta_avatar = es el valor de ruta de la imagen.
    
        Returns :
            imagen2 =  imagen a mostrar.
    """
    nombre_archivo = os.path.basename(ruta_avatar)
    ruta_destino = os.path.join(os.getcwd(), nombre_archivo)
    ruta_destino = os.path.join(os.getcwd(), RUTA_IMAGENES_USUARIOS, nombre_archivo)
    # Leer el archivo de la imagen y escribirlo en un archivo nuevo en la carpeta de destino
    with open(ruta_avatar, 'rb') as archivo_origen, open(ruta_destino, 'wb') as archivo_destino:
        archivo_destino.write(archivo_origen.read())
        imagen = Image.open(ruta_avatar)
        tamanio = imagen.size
        if (tamanio>(200,200)):
            imagen=imagen.resize((200, 200))
            imagen.save(RUTA_IMAGENES_USUARIOS)
        imagen2 = ImageTk.PhotoImage(imagen)
        
    return imagen2
    
def modificar_json(values, usuario, pos):
    """Modifica los datos de un archivo json que contiene informacion sobre los perfiles previamente registrados.
    
        Args : 
            values = diccionario con los nuevos valores.
            usuario = el perfil con los valores a modificar.
            pos = la posicion donde se encuentra el diccionario dentro del archivo json.
    """
    with open(RUTA_JSON, 'r+') as archivo_json:
            lista_diccionarios = json.load(archivo_json)

            #Si values es distinto de vacio significa que modifico el avatar, lo actualizo
            if (values["-NUEVO_PERFIL-RUTA_AVATAR-"] != '') : 
                lista= values["-NUEVO_PERFIL-RUTA_AVATAR-"].split("/","\\")
                values["-NUEVO_PERFIL-RUTA_AVATAR-"]= lista.pop()
            #Si values es vacio, significa que mantiene el mismo, entonces guardo el nombre de la imagen anterior en values
            else :
                values["-NUEVO_PERFIL-RUTA_AVATAR-"] = usuario["-NUEVO_PERFIL-RUTA_AVATAR-"]
            lista_diccionarios[values["Nick"]] = values
            archivo_json.seek(0)
            json.dump(lista_diccionarios, archivo_json, indent=4)
            archivo_json.truncate()
            usuario = values

def controlar_valores (values) :
    """Controla que todos los campos esten correctamente completos.
    
        Args :
            values = valores del diccionario ingresados por el usuario.
            current_window = ventana actual.
        
        Returns :
            ok (boolean) = si es True, todos los valores son correctos, sino no.
    """
    ok = True
    
    errores = 'Por favor: '

    #Evaluamos nombre este completo con caracteres
    nombre = values["Nombre"]
    if not nombre :
        errores += '\n - Dejar completo el campo del nombre'
        ok = False
    
    #Evaluamos que la edad sea un numero entero y este en un rango
    edad = values["Edad"]
    if  edad.isdigit() :
        edad = int(edad)
        if not 0<= edad <= 150 :
            errores += '\n - Dejar completo el campo de la edad con un numero entero entre 0 y 150'
            ok = False
    else :
        errores += '\n - Dejar completo el campo de la edad con un numero entero entre 0 y 150'
        ok = False    
    
    #Evaluamos que opcion de genero selecciono
    genero = (values["F"], values["M"], values["O"])
    match genero:
        case True, False, False :
            genero = 'Femenino'
            values["autogenero"] = genero
        case False, True, False :
            genero = 'Masculino'
            values["autogenero"] = genero
        case False, False, True :
            if not values["autogenero"] :
                errores += '\n - Complete el campo de genero autopercibido'
                ok = False
    
    if (ok == False) :
        sg.popup (errores, title='-NUEVO_PERFIL-ERROR-', background_color='brown')

    return ok

def layout(usuario) :
    """Crea elementos para la ventana.
        
        Args : 
            usuario = diccionario con datos del perfil cargado.
        
        Returns  :
            lista con elementos de la ventana.
    """
    encabezado = [
        [
            sg.Column(
                [[sg.RButton('Volver', image_data=image_file_to_bytes(button64, (100, 50)), 
             font='Rockwell', pad=(0, 0), key="-MODIFICAR_PERFIL-VOLVER-")]]
            ),
            sg.Text("Modificar Perfil", font=('Rockwell', TAMANIO_TITULO), justification="center", pad = (290,1))
        ]
    ]

    columna1 = [
        [sg.Text("Nick (No se puede modificar)", background_color='brown')],
        [sg.InputText(usuario.get("Nick"), key="Nick", disabled=True)],
        [sg.Text("Nombre", background_color='brown')],
        [sg.InputText(usuario.get("Nombre"), key="Nombre")],
        [sg.Text("Edad", background_color='brown')], 
        [sg.InputText(usuario.get("Edad"), key="Edad")],
        [sg.Text("Genero",background_color='brown')], 
        [sg.Radio("Femenino", "RADIO1", key = "F",background_color='pink', default=usuario.get("F")), 
         sg.Radio("Masculino", "RADIO1", key = "M", background_color='blue', default=usuario.get("M")), 
         sg.Radio("Otro", "RADIO1", key = "O", background_color='green', default=usuario.get("O"))],
        [sg.Text("Ingrese su genero autopercibido", key='texto_genero', background_color='brown')],
        [sg.InputText(usuario.get("Nick"), key='autogenero')]
    ]
    columna2 = [
        [sg.Image(
            source = os.path.join(RUTA_IMAGENES_USUARIOS, usuario.get("-NUEVO_PERFIL-RUTA_AVATAR-")),
            key="imagen_mostrar",
            size=(300,300),
            pad=((125,125),(10,10))
        )],
        [sg.FileBrowse(
            "Seleccionar imagen",
            key="-NUEVO_PERFIL-RUTA_AVATAR-",
            enable_events=True,
            change_submits=True,
            size=(20,2),
            pad=(200,1),
            file_types = (("PNG", "*.png"),('GIF Files', '*.gif'))
        )]
    ]

    columnas = [
        [
            sg.Column(columna1),
            sg.Column(
                columna2,
                element_justification="left",
                size=(450, 400)
            )
        ]
    ]

    columna_boton = [
        [sg.RButton("Guardar", image_data=image_file_to_bytes(green_pill64, (100, 50)),
         font='Rockwell', pad=(0, 0), key="-MODIFICAR_PERFIL-GUARDAR-")]
    ]



    return [
        [sg.Column(layout=encabezado, expand_x=True)],
        [
            sg.Column(
                layout=columnas, 
                justification="center", 
                key="llave_columnas",
                expand_y=True, #Expande el tamaño de la columna para que la ocupe entera
                pad=(50, 50) #Deja espacio entre las columnas y con el titulo
            )
        ],
        [sg.Column(layout=columna_boton, expand_x=True, element_justification="right")]
    ]   

def crear_ventana (menu,usuario) :
    """Crea y devuelve la ventana del modificar perfil.
        
        Args:
            menu = pantalla del menu para luego ser desencondida.
            usuario = diccionario con los datos alias del perfil actual.
        
        Returns:
            window (PySimpleGUI.PySimpleGUI.Window) = ventana de modificicar perfil.
    """
    return sg.Window("Nuevo Perfil", layout(usuario), margins=(10,10), background_color='white',finalize=True,metadata = {'perfil':usuario,'menu':menu},resizable=True)

def procesar_eventos (current_window, event, values) :
    """Procesa los eventos de la ventana modificar perfil.
    
        Args: 
            current_window (PySimpleGUI.PySimpleGUI.Window): Ventana de modificar perfil.
            event (str): Nombre de el evento producido en la ventana.
            values (dict): Diccionario con los valores de la ventana.
    """
    pos = buscar(current_window.metadata['perfil']["Nick"])
    match event :
        case "RUTA_AVATAR" :
            imagen = cambiar_imagen(values)
            current_window ["imagen_mostrar"].update(data=imagen, size=(300,300), subsample=3)
        
        case 'GUARDAR' :
            ok = controlar_valores(values)
            
            #Si los valores estan completos, carga el archivo json y abre el menu principal
            if ok :
                modificar_json(values, current_window.metadata['perfil'], pos)
                
                #Actualizar logs
                logs.actualizar_logs(current_window.metadata['perfil']['Nick'],'Modificación de perfil')

                #Cierra la ventana de modificar perfil, vuelve al menu pricipal
                current_window.metadata['menu'].un_hide()
                current_window.metadata['menu']['-PRINCIPAL-IMAGEN-'].update(filename = os.path.join(RUTA_IMAGENES_USUARIOS,values['-NUEVO_PERFIL-RUTA_AVATAR-']),subsample=2)
                current_window.metadata['menu'].metadata['perfil'] = values
                current_window.close()

        case "VOLVER" :
            current_window.metadata['menu'].un_hide()
            current_window.close()
            
        case _ :
            controlar_valores(values, current_window)

            