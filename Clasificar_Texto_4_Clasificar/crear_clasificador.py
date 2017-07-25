#!/usr/bin/env python
# encoding: utf-8



import sys, os
import numpy as np
parent_dir=os.getcwd()
path= os.path.dirname(parent_dir)
sys.path.append(path)

try:
    from DAO.LeerArchivo_csv import leer_archivo #a.1
    from DAO.LeerDB_Mongo import leer

except ImportError:
    print 'Verificar si en la carpeta Procesar existen los archivos: LeerArchivo_csv y/o ValidacionCruzada'

try:
    from Clasificar_Texto_2_Normalizar_texto.normalizacion import normalizar_corpus #b.1
except ImportError:
    print 'Verificar si en la carpeta Procesar existe el archivo normalizacion'

try:
    from Clasificar_Texto_3_FrecuenciaTermino.extractor_caracteristicas import mbp_extractor, tfidf_extractor, tfidf_transformar#c.2
    from clasificadores import Crear_clasificadorSGD #c.2
except ImportError:
    print 'Verificar si en la carpeta Procesar existen los archivos; extractor_caracteristicas,metricas y clasificadores'



"""
<<<a.Código de preparación de los datos>>>
En esta parte se realiza el proceso de leer el corpus (a.1)
y de dividirlo(a.2) para tenerlos separados para entrenamiento
y pruebas
"""
#####a.1----------------------------------------------------------
###Llamando la función de leer archivo para obtener el corpus
datafile="DataJose.csv"
corpus,categorias =leer_archivo(datafile)# Leer el archivo
###----------------------------------------------------------


#idt,categorias,corpus =leer()# Leer el archivo
print 'corpus',len(corpus)
print'categoria',len(categorias)



"""
<<<b.Código de normalización del texto>>
En esta parte se realiza el tratamiento de normalización del corpus de entrenamiento (b.1) y
de pruebas (b.2) por separado
"""

#b.1---------------------------------------------------------------------------------------
#Hacer el tratamiento de las palabras del corpus de entrenamiento
norm_entrena_corpus = normalizar_corpus(corpus)
#--------------------------------------------------------------------------------------------



"""
<<<c.Código de Extracción de características>>
En esta parte se crean las matrices de frecuencia con los 3 algoritmos que tenemos
para crear las bolsas de palabras, modelo de bolsa de palabras (c.1), tfidf(c.2) y tfidf transform
tanto para el corpus de entrenamiento como el de pruebas
"""

#c.2---------------------------------------------------------------------------------------
# tfidf
vectorizar, entrenamiento = tfidf_extractor(norm_entrena_corpus)
print 'vector'
SGDtfidf=Crear_clasificadorSGD(entrenamiento,categorias)
print SGDtfidf




"""
<<<d.Generar archivos>>
En esta parte se generan los archivos de vectorización y de clasificación
"""
#Generar archivos
try:
    import cPickle as pickle
except ImportError:
    print 'Verifique si tiene instalada la librería cPickle'

filePath = os.path.abspath('output')
dafile="vectorizador.pickle"
dafileclasif="clasificador.pickle"


#2_tfidf_vectorizar
datafile = os.path.join(filePath,dafile)
fichero = file(datafile, "w")
pickle.dump(vectorizar, fichero)
fichero.close()
print 'Creado ' + dafile

#2_tfidf_SGD
datafile = os.path.join(filePath,dafileclasif)
fichero = file(datafile, "w")
pickle.dump(SGDtfidf, fichero)
fichero.close()
print 'Creado ' + dafileclasif
