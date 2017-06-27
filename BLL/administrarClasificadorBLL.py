#!/usr/bin/env python
# encoding: utf-8

import sys, os
import numpy as np
import datetime
parent_dir=os.getcwd()
path= os.path.dirname(parent_dir)
sys.path.append(path)

import pickle

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.linear_model import SGDClassifier

from DAO.administrarClasificadoresDAO import *
from UTIL.tweetsToData import transform
from UTIL.tweetsToText import *

import multiprocessing


def reentrenarClasificadorBLL(nombre, entrena_ini, entrena_fin):
    tweets = getTweetsClasificados(entrena_ini, entrena_fin)

    data, labels = transform(tweets, nombre)

    #nombre = getClasiDefecto()

    nCores = multiprocessing.cpu_count()

    with open('../MODELOS/'+ nombre +'.pickle', 'rb') as input_file:
         clasificador = pickle.load(input_file)

    scores = cross_val_score(clasificador, data, labels, cv=4, n_jobs=nCores)
    accMedio = scores.mean()
    desviacion = scores.std() * 2

    clasificador = clasificador.partial_fit(data, labels)

    with open('../MODELOS/'+ nombre +'.pickle', 'wb') as handle:
        pickle.dump(clasificador, handle)

    updateClasificador(nombre, accMedio, desviacion, entrena_ini, entrena_fin)


def crearClasificador(nombre, entrena_ini, entrena_fin):

    #Llamar a DAO para conseguir los Tweets
    tweets = getTweetsClasificados(entrena_ini, entrena_fin)
    #textos, labels =getTweetsClasificadosMM(entrena_ini, entrena_fin) #MM
    print 'fin extracción DB'
    #data, labels, vectorizer = transform(tweets)

    textos, labels = transTwToTxt(tweets)

    data = vectorizar(textos, nombre)
    print 'fin vectorizador'

    nCores = multiprocessing.cpu_count()
    print 'fin multiproceso'

    print 'Calculando la precision de ' + nombre + ' desde ' + entrena_ini + ' hasta ' + entrena_fin
    clasificador = SGDClassifier(loss='hinge', n_iter=100)
    print 'fin clasificador'
    scores = cross_val_score(clasificador, data, labels, cv=4, n_jobs=nCores)
    print 'fin scores'
    accMedio = scores.mean()
    desviacion = scores.std() * 2

    print 'Entrenando el modelo...'
    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.25, random_state=0, stratify=labels)
    clasificador = SGDClassifier(loss='hinge', n_iter=100, n_jobs=nCores)
    clasificador = clasificador.fit(X_train, y_train)

    print 'Almacenando modelo en /MODELOS/' + nombre + '.pickle'
    with open('../MODELOS/'+ nombre +'.pickle', 'wb') as handle:
        pickle.dump(clasificador, handle)


    #Llamar a DAO para que guarde el nombre, ACC, DESV
    addClasificador(nombre, accMedio, desviacion, entrena_ini, entrena_fin)



def getClasificadoresBLL():
    return getClasificadores()



def eliminarClasificador(nombre):

    eliminarClasificadorDAO(nombre)

    modelo = os.path.abspath('../MODELOS/'+ nombre +'.pickle')
    os.remove(modelo)
    vector = os.path.abspath('../VECTORIZER/vectorizer_'+ nombre +'.pickle')
    os.remove(vector)

    # Como mandarle un alert al tpl con el error ?
    # Si view recibe una excepcion, redirecciona a un tpl de error pasandole:
    # 1. la pagina donde estaba
    # 2. el mensaje de error
    # tras pulsar en el aceptar del alert, envia por POST la pagina donde estaba y redireccion
