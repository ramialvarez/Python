from datetime import datetime
import csv
from unlpimage.config.rutas import RUTA_LOGS
import os

def actualizar_logs(nick,operacion,valores=None,textos=None,timestamp=int(datetime.timestamp(datetime.now()))):
    """Actualiza el archivo de logs con la informacion recibida
    Args : 
        nick (str): nick del perfil que realiza la operacion
        operacion (list): operacion a anotar en los logs
    """
    
    #fecha_hora = datetime.fromtimestamp(timestamp)
    #fecha_hora.strftime("%d/%m/%Y ")
    if (os.path.exists(RUTA_LOGS)):
        with open(RUTA_LOGS,'a', newline='', encoding="UTF-8") as archivo:
            writer = csv.writer(archivo)
            if valores == None:
                writer.writerow([timestamp, nick, operacion])
            else:
                writer.writerow([timestamp, nick, operacion,valores,textos])
    else:
         with open(RUTA_LOGS,'x', newline='', encoding="UTF-8") as archivo:
            writer = csv.writer(archivo)
            writer.writerow(['Timestamp','Nick','Operación','Valores','Textos'])
            if valores == None:
                writer.writerow([timestamp, nick, operacion])
            else:
                writer.writerow([timestamp, nick, operacion,valores,textos])

def ver_logs():
    """Imprime los renglones del log para conocer su contenido"""
    try:
        with open(RUTA_LOGS,'r+', encoding="UTF-8") as archivo:
            lector_csv = csv.DictReader(archivo, delimiter=',')
            contenido_csv = list(lector_csv)
            for elem in contenido_csv:
                 print(elem)
    except FileNotFoundError:
        with open(RUTA_LOGS,'x', newline='', encoding="UTF-8") as archivo:
            writer = csv.writer(archivo)
            writer.writerow(['Timestamp','Nick','Operación','Valores','Textos'])
        print('El archivo no existia')