import os
import json

RUTA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_ANTERIOR = os.path.dirname(RUTA)
RUTA_DATOS = os.path.join(RUTA,'datos')
RUTA_BOTONES = os.path.join(RUTA_DATOS,'imagenes')
RUTA_ARCHIVOS = os.path.join(RUTA_DATOS,"Archivos")
RUTA_DIRECTORIOS = os.path.join(RUTA_ARCHIVOS,"Directorios.json")
RUTA_LOGS = os.path.join(RUTA_ARCHIVOS,"Logs.csv")
RUTA_DATOS_IMAGENES = os.path.join(RUTA_ARCHIVOS,"Datos_imagenes.csv")
RUTA_IMAGENES_USUARIOS = os.path.join(RUTA_DATOS,'imagenes_perfiles')
RUTA_JSON = os.path.join(RUTA_ARCHIVOS, "Archivo_Perfiles.json")
RUTA_PLANTILLAS_COLLAGES = os.path.join(RUTA_DATOS, 'plantillas_collages')
RUTA_DATOS_COLLAGES = os.path.join(RUTA_ARCHIVOS, "Datos_plantillas_collage.json")
RUTA_TEMPLATES = os.path.join(RUTA_ARCHIVOS, "Templates.json")
RUTA_PLANTILLAS_MEMES = os.path.join(RUTA_DATOS, "plantillas_memes")
RUTA_FUENTES = os.path.join(RUTA_DATOS,"fuentes")

def convertir_para_guardar(path):
    path_relativo = os.path.relpath(path, start=RUTA_ANTERIOR)
    return path_relativo.replace(os.path.sep, "/")

def convertir_guardado(path):
    path_del_sistema = path.replace("/",os.path.sep)
    return os.path.abspath(os.path.join(RUTA_ANTERIOR,path_del_sistema))


def get_rutas(ruta='todas'):
    """Devuelve la ruta o rutas deseadas para el uso de imagenes

        Args:
            ruta (str): nombre del repositorio deseado (opcional)
        Returns:
            Ruta_repositorio (str): ruta del repositorio de imagenes. (en caso de enviar 'repositorio')
            Ruta_collages (str): ruta donde se almacenan los collages. (en caso de enviar 'collages')
            Ruta_memes (str): ruta donde se almacenan los memes. (en caso de enviar 'memes')
            Ruta_repositorio,Ruta_collages,Ruta_memes (en caso de no especificarse un parametro)
    """
    try:
        with open(RUTA_DIRECTORIOS,'r',encoding= "UTF-8") as archivo:
            Direcciones = json.load(archivo)
            Ruta_repositorio = convertir_guardado(Direcciones['Repositorio'])
            Ruta_collages = convertir_guardado(Direcciones['Collages'])
            Ruta_memes = convertir_guardado(Direcciones['Memes'])
    except FileNotFoundError:
        with open(RUTA_DIRECTORIOS,'x',encoding="UTF-8") as archivo:
            json.dump({'Repositorio' : 'Repositorio','Collages' : 'Collages','Memes' : 'Memes'},archivo)
        Ruta_repositorio = os.path.join(RUTA_ANTERIOR,'Repositorio')
        if (not os.path.exists(Ruta_repositorio)):
            os.mkdir(Ruta_repositorio)
        Ruta_collages = os.path.join(RUTA_ANTERIOR,'Collages')
        if (not os.path.exists(Ruta_collages)):
            os.mkdir(Ruta_collages)
        Ruta_memes = os.path.join(RUTA_ANTERIOR,'Memes')
        if (not os.path.exists(Ruta_memes)):
            os.mkdir(Ruta_memes)
    
    match ruta:
        case 'repositorio':
            return Ruta_repositorio
        case 'collages':
            return Ruta_collages
        case 'memes':
            return Ruta_memes
        case _:
            return Ruta_repositorio,Ruta_collages,Ruta_memes
