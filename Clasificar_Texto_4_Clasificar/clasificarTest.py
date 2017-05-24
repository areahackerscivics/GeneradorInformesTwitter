#!/usr/bin/env python
# encoding: utf-8

import sys, os
import time
from pymongo import MongoClient#Libreria Mongodb
parent_dir=os.getcwd()
path= os.path.dirname(parent_dir)
sys.path.append(path)

#Conexion a MongoDB
cliente = MongoClient()#Inicializar objeto
cliente = MongoClient('127.0.0.1', 27017)#Indicar parametros del servidor
bd = cliente.twitter#Seleccionar Schema
tweetsdb = bd.PruebaClasificador#Seleccionar Coleccion
"""
<<<a.Código de preparación de los datos>>>
En esta parte se realiza el proceso de leer el corpus (a.1)
y de dividirlo(a.2) para tenerlos separados para entrenamiento
y pruebas
"""
try:
    from DAO.LeerArchivo_csv import leer_archivo
    from DAO.LeerDB_Mongo import leer
    from Clasificar_Texto_2_Normalizar_texto.normalizacion import normalizar_corpus
    
except ImportError:
    print 'Verificar si en la carpeta Procesar existen los archivos: LeerArchivo_csv y/o normalización'

#a--------------------Llamando la función de leer archivo para obtener el corpus-------------------
try:
    import os
except ImportError:
    print 'Verifique si tiene instalada la librería os'

datafile = "DataTaller.csv" #archivo que contiene el corpus
prueba_corpus,prueba_categorias =leer_archivo(datafile)# Leer el archivo

##datafile="DBtweetClasificados18"
##idt,prueba_categorias,prueba_corpus =leer()

#b--------------Hacer el tratamiento de las palabras del corpus de prueba------------------------
norm_prueba_corpus = normalizar_corpus(prueba_corpus)

"""
<<<c.Código de Extracción de características>>
En esta parte se crean las matrices de frecuencia con los 3 algoritmos que tenemos
para crear las bolsas de palabras, modelo de bolsa de palabras (c.1), tfidf(c.2) y tfidf transform
tanto para el corpus de entrenamiento como el de pruebas
"""
try:
    import cPickle as pickle
except ImportError:
    print 'Verifique si tiene instalada la librería cPickle'

#c.1---------------modelo bolsa de palabras---------------------------------------------------

def leerDat(dafilevect, dafileclas):
    filePath = os.path.abspath('output')
    datafile = os.path.join(filePath,dafilevect)
    fichero = file(datafile)
    vectorizar = pickle.load(fichero)
    datafile = os.path.join(filePath,dafileclas)
    fichero = file(datafile)
    SGD = pickle.load(fichero)
    return vectorizar, SGD


try:
    from Clasificar_Texto_3_FrecuenciaTermino.extractor_caracteristicas import mbp_extractor, tfidf_extractor, tfidf_transformar
    from metricas import evaluar_modelo
except ImportError:
    print 'Verificar si en la carpeta Procesar existen los archivos; extractor_caracteristicas,metricas'

##mbp_vectorizar, SGDmbp=leerDat("mbp_vectorizar.dat", "SGDmbp.dat")
##mbp_prueba= mbp_vectorizar.transform(norm_prueba_corpus)
##predecir=SGDmbp.predict(mbp_prueba)
##print ''
##print 'SGD con mbp'
##evaluar_modelo(prueba_categorias, predecir)


#c.2---------------------------------------------------------------------------------------
# tfidf 
tfidf_vectorizar, SGDtfidf=leerDat("vectorizar.pickle", "SGD.pickle")
tfidf_prueba = tfidf_vectorizar.transform(norm_prueba_corpus)
predecir=SGDtfidf.predict(tfidf_prueba)
clases=SGDtfidf.classes_
puntaje=SGDtfidf.decision_function(tfidf_prueba)
print ''
print 'SGD con tfidf'
ex, pr, re, fm=evaluar_modelo(prueba_categorias, predecir)
print 'Accuracy:', ex
print 'Precision:', pr
print 'Recall:', re
print 'F1 Score:', fm
y_pred=[]
for i in range(len(prueba_corpus)):
    lista= sorted(zip(puntaje[i],  clases), reverse=True)
    y_pred.append(lista[0][1])#lista de las categorias predicas, acertadas y erradas
    if prueba_categorias[i] == lista[0][1]:
        guardar={
            "evaluacion":'Bien',
            "categoriaPredicha":lista[0][1].decode('utf-8'),
            "categoriaReal":prueba_categorias[i],
            "archivo":datafile,
            "puntaje":lista[0][0],
            "Accuracy":ex,
            "Precision":pr,
            "Recall":re,
            "F1 Score":fm,
            "texto":prueba_corpus[i].decode('utf-8'),
            "fecha":time.strftime("%d-%m-%y")
            };
        try:
             tweetsdb.insert_one(guardar)#Almacenar
        except:
            print "No se pudo guardar evaluación ok" 
    else:
        guardar={
            "evaluacion":'Mal',
            "categoriaPredicha":lista[0][1].decode('utf-8'),
            "categoriaReal":prueba_categorias[i],
            "archivo":datafile,
            "puntaje":lista[0][0],
            "Accuracy":ex,
            "Precision":pr,
            "Recall":re,
            "F1 Score":fm,
            "texto":prueba_corpus[i].decode('utf-8'),
            "fecha":time.strftime("%d-%m-%y")
            };
        try:
             tweetsdb.insert_one(guardar)#Almacenar
        except:
            print "No se pudo guardar evaluación mal" 
        


