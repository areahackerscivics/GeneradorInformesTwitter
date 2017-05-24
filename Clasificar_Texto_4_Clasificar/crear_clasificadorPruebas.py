#!/usr/bin/env python
# encoding: utf-8



import sys, os
parent_dir=os.getcwd()
path= os.path.dirname(parent_dir)
sys.path.append(path)


"""
<<<a.Código de preparación de los datos>>>
En esta parte se realiza el proceso de leer el corpus (a.1)
y de dividirlo(a.2) para tenerlos separados para entrenamiento
y pruebas
"""
try:
    from DAO.LeerArchivo_csv import leer_archivo
    from ValidacionCruzada import validacion_cruzada
    
except ImportError:
    print 'Verificar si en la carpeta Procesar existen los archivos: LeerArchivo_csv y/o ValidacionCruzada'

#a.1----------------------------------------------------------
#Llamando la función de leer archivo para obtener el corpus
import os
import numpy as np

#####a.1----------------------------------------------------------
###Llamando la función de leer archivo para obtener el corpus
datafile="training45000.csv"
##datafile="prueba.csv"
corpus,categorias =leer_archivo(datafile)# Leer el archivo
###----------------------------------------------------------


#a.2---------------------------------------------------------------------------------------
#Llamando la función de dividir dataset para tener los tweets de entrenamiento y de pruebas
entrenar_corpus, prueba_corpus, entrenar_categorias, prueba_categorias = validacion_cruzada(corpus,
                                                                        categorias)
#--------------------------------------------------------------------------------------------
"""
<<<b.Código de normalización del texto>>
En esta parte se realiza el tratamiento de normalización del corpus de entrenamiento (b.1) y
de pruebas (b.2) por separado
"""
try:
    from Clasificar_Texto_2_Normalizar_texto.normalizacion import normalizar_corpus
except ImportError:
    print 'Verificar si en la carpeta Procesar existe el archivo normalizacion'

#b.1---------------------------------------------------------------------------------------
#Hacer el tratamiento de las palabras del corpus de entrenamiento
norm_entrena_corpus = normalizar_corpus(entrenar_corpus)
''.strip()
#print 'Corpus: ', np.shape(norm_entrena_corpus)

#--------------------------------------------------------------------------------------------

#b.2---------------------------------------------------------------------------------------
#Hacer el tratamiento de las palabras del corpus de prueba
norm_prueba_corpus = normalizar_corpus(prueba_corpus)
#--------------------------------------------------------------------------------------------

"""
<<<c.Código de Extracción de características>>
En esta parte se crean las matrices de frecuencia con los 3 algoritmos que tenemos
para crear las bolsas de palabras, modelo de bolsa de palabras (c.1), tfidf(c.2) y tfidf transform
tanto para el corpus de entrenamiento como el de pruebas
"""
try:
    from Clasificar_Texto_3_FrecuenciaTermino.extractor_caracteristicas import mbp_extractor, tfidf_extractor, tfidf_transformar
    from metricas import evaluar_modelo
    from clasificadores import Crear_clasificadorSGD
except ImportError:
    print 'Verificar si en la carpeta Procesar existen los archivos; extractor_caracteristicas,metricas y clasificadores'

#c.1---------------------------------------------------------------------------------------
# modelo bolsa de palabras
mbp_vectorizar, mbp_entrenamiento= mbp_extractor(norm_entrena_corpus)  
mbp_prueba= mbp_vectorizar.transform(norm_prueba_corpus)
SGDmbp=Crear_clasificadorSGD(mbp_entrenamiento,entrenar_categorias)
predecir=SGDmbp.predict(mbp_prueba)
print ''
print 'SGD con mbp'
evaluar_modelo(prueba_categorias, predecir)
#c.2---------------------------------------------------------------------------------------
# tfidf 
tfidf_vectorizar, tfidf_entrenamiento = tfidf_extractor(norm_entrena_corpus) 
tfidf_prueba = tfidf_vectorizar.transform(norm_prueba_corpus)
SGDtfidf=Crear_clasificadorSGD(tfidf_entrenamiento,entrenar_categorias)
predecir=SGDtfidf.predict(tfidf_prueba)
print ''
print 'SGD con tfidf'
evaluar_modelo(prueba_categorias, predecir)
#c.3---------------------------------------------------------------------------------------
# tfidf transform
tfidftr_vectorizar, tfidftr_entrenamiento = tfidf_transformar(mbp_entrenamiento)  
tfidftr_prueba= tfidftr_vectorizar.transform(mbp_prueba)
SGDtfidftr=Crear_clasificadorSGD(tfidftr_entrenamiento,entrenar_categorias)
predecirtfidftr=SGDtfidftr.predict(tfidftr_prueba)
print ''
print 'SGD con tfidftr'
evaluar_modelo(prueba_categorias, predecir)

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
dafile="mbp_vectorizar.dat"
datafile = os.path.join(filePath,dafile)

#1_mbp_vectorizar
fichero = file(datafile, "w")  
pickle.dump(mbp_vectorizar, fichero)
fichero.close()

#1_mbp_SGD
dafile="SGDmbp.dat"
datafile = os.path.join(filePath,dafile)
fichero = file(datafile, "w")  
pickle.dump(SGDmbp, fichero)
fichero.close()

#2_tfidf_vectorizar
dafile="tfidf_vectorizar.dat"
datafile = os.path.join(filePath,dafile)
fichero = file(datafile, "w")
pickle.dump(tfidf_vectorizar, fichero)
fichero.close()

#2_tfidf_SGD
dafile="SGDtfidf.dat"
datafile = os.path.join(filePath,dafile)
fichero = file(datafile, "w")
pickle.dump(SGDtfidf, fichero)
fichero.close()

#3_tfidftr_vectorizar
dafile="vectorizar.pickle"
datafile = os.path.join(filePath,dafile)
fichero = file(datafile, "w")
pickle.dump(tfidftr_vectorizar, fichero)
fichero.close()

#3_tfidftr_SGD
dafile="SGD.pickle"
datafile = os.path.join(filePath,dafile)
fichero = file(datafile, "w")
pickle.dump(SGDtfidftr, fichero)
fichero.close()


