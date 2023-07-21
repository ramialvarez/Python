import PySimpleGUI as sg
import re
from unlpimage.pantallas import generador_memes,menu_principal, configuracion,etiquetar_imagenes,inicio, nuevo_perfil, modificar_perfil,generador_collage,seleccionar_template, imagenes_collages

sg.ChangeLookAndFeel('Light blue')

inicio.crear_ventana()

while True:
    current_window, event, values = sg.read_all_windows()
    if event == sg.WIN_CLOSED or event == '-SALIR-':
        current_window.close()
        break
    else:
        lista = event.replace('-',' ').split()
        if len(lista) == 3:
            pantalla,event,usuario = lista
            # Formateo el nombre del usuario 
            usuario = re.sub(r'(?<=\w)([A-Z])', r' \1', usuario)
        else:
            pantalla,event = lista
            usuario = None
        match pantalla:
            case "PRINCIPAL":
                menu_principal.procesar_eventos(current_window,event, values)
            case "CONFIGURACION":
                configuracion.procesar_eventos(current_window,event, values)
            case "ETIQUETAR":
                etiquetar_imagenes.procesar_eventos(current_window,event,values)
            case "INICIO":
                inicio.procesar_eventos(current_window,event,usuario)
            case "NUEVO_PERFIL" :
                nuevo_perfil.procesar_eventos_nuevo_perfil(current_window,event,values)
            case "MODIFICAR_PERFIL" :
                modificar_perfil.procesar_eventos(current_window, event, values)
            case "COLLAGE":
                generador_collage.procesar_eventos(current_window,event)
            case "IMAGENES" :
                imagenes_collages.procesar_eventos(current_window,event,values)
            case "TEMPLATE":
                seleccionar_template.procesar_eventos(current_window,event,values)
            case 'MEME':
                generador_memes.procesar_eventos(current_window,event,values)
                