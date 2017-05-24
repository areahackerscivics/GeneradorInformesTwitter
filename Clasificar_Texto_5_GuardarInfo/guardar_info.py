#!/usr/bin/env python
# encoding: utf-8


# 1. Datos
#   1.1 Obtener datos
#   1.2 Pretratamiento de datos
# 2. Clasificacion
#   2.1 Clasificar
#   2.2 Conteo de tweets
# 3. Guardar informacion

import pickle
from Procesar.normalizacion import normalizar_corpus # 1.2
from pymongo import MongoClient
import datetime
#from data_base_tweets import mongop



# 1. DATOS ====================================================================
# 1.1 Obtener datos -----------------------------------------------------------
# Este apartado habra que revisar como hacerlo bien.
datos = []
with open('../Clasificar_Texto_4_Clasificar/training.csv', "r") as f:
    header = f.readline().split(";")
    for line in f:
        fields = line.split(";")
        datos.append(fields[3])


# 1.2 Pretratamiento de datos -------------------------------------------------
datos = normalizar_corpus(datos) # Revisar la llamada

with open('../Clasificar_Texto_4_Clasificar/tfidf_vectorizador.pickle', 'rb') as handle:
    tfIdf = pickle.load(handle)
handle.close()
datos = tfIdf.transform(datos)

# 2. CLASIFICACION ============================================================
# 2.1 Clasificar --------------------------------------------------------------
with open('../Clasificar_Texto_4_Clasificar/sgd_tfidf.pickle', 'rb') as handle:
    clasificador = pickle.load(handle)
handle.close()
clasificacion = clasificador.predict(datos)

# 2.2 Conteo de datos ---------------------------------------------------------
with open('../Clasificar_Texto_4_Clasificar/etiquetas.pickle', 'rb') as handle:
    etiquetas = pickle.load(handle)
handle.close()
resultados = {}
for etiqueta in etiquetas:
    resultados[etiqueta] = sum( clasificacion == etiqueta )

now = datetime.datetime.now()
resultados['anyo'] = now.year
resultados['mes'] = now.month
resultados['dia'] = now.day

# 3. GUARDAR INFORMACION ======================================================
#   3.1 Conexion DB -----------------------------------------------------------
print resultados
'''
conexion = datosConexion()
client = MongoClient(conexion)
#db = client['test-database']
coleccion = infColeccion()
informes = db[coleccion]
post_id = informes.insert_one(resultados).inserted_id
'''
