#!/usr/bin/env python
# encoding: utf-8


# 1. Datos
#   1.1 Obtener datos
#   1.2 Pretratamiento de datos
# 2. Clasificacion
#   2.1 Clasificar
# 3. Guardar informacion
#   3.1 Estructurar la informacion
#   3.2 Conexion database

import sys, os
parent_dir = os.getcwd()
path = os.path.dirname(parent_dir)
sys.path.append(path)

import pickle
from Clasificar_Texto_2_Normalizar_texto.normalizacion import normalizar_corpus # 1.2
from pymongo import MongoClient
import datetime
from data_base_tweets.mongop import *
import numpy as np



# 1. DATOS ====================================================================
# 1.1 Obtener datos -----------------------------------------------------------
# Este apartado habra que revisar como hacerlo bien.
print 'Recogiendo datos...\n'
tweets = []
with open('../Clasificar_Texto_4_Clasificar/training.csv', "r") as f:
    header = f.readline().split(";")
    for line in f:
        fields = line.split(";")
        tweets.append(fields[3])

# 1.2 Pretratamiento de datos -------------------------------------------------
print 'Pretratando datos...\n'
datos = normalizar_corpus(tweets) # Revisar la llamada

with open('../Clasificar_Texto_4_Clasificar/vectorizador.pickle', 'rb') as handle:
    tfIdf = pickle.load(handle)
handle.close()
datos = tfIdf.transform(datos)

# 2. CLASIFICACION ============================================================
# 2.1 Clasificar --------------------------------------------------------------
print 'Clasificando...\n'

with open('../Clasificar_Texto_4_Clasificar/clasificador.pickle', 'rb') as handle:
    clasificador = pickle.load(handle)
handle.close()
clasificacion = clasificador.predict(datos)



# 3. GUARDAR INFORMACION ======================================================
# 3.1 Estructurar la informacion ----------------------------------------------
print 'Estructurando informacion...\n'

now = datetime.datetime.now()
anyo = now.year
mes = now.month
dia = now.day

resultados = []
for tweet, etiqueta in zip(tweets, clasificacion):
    aux = {}
    aux['anyo'] = anyo
    aux['mes'] = mes
    aux['dia'] = dia
    aux['tweet'] = tweet
    aux['etiqueta'] = etiqueta

    resultados.append(aux)


# 3.2 Conexion database -------------------------------------------------------
print 'Conectado a la base de datos... \n'

conexion = datosConexion()
client = MongoClient(conexion)
tdb = twDatabase()
db = client[tdb]
coleccion = infColeccion()
informes = db[coleccion]
post_id = informes.insert(resultados)


print 'Tweets clasificados y guardados en la base de datos!'
