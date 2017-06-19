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

import multiprocessing



def crearClasificador(nombre, entrena_ini, entrena_fin):

    #Llamar a DAO para conseguir los Tweets
    tweets = getTweetsClasificados(entrena_ini, entrena_fin)

    data, labels, vectorizer = transform(tweets)

    nCores = multiprocessing.cpu_count()

    print 'Calculando la precision de ' + nombre + ' desde ' + entrena_ini + ' hasta ' + entrena_fin
    clasificador = SGDClassifier(loss='hinge', n_iter=100)
    scores = cross_val_score(clasificador, data, labels, cv=4, n_jobs=nCores)
    accMedio = scores.mean()
    desviacion = scores.std() * 2

    print 'Entrenando el modelo...'
    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.25, random_state=0, stratify=labels)
    clasificador = SGDClassifier(loss='hinge', n_iter=100)
    clasificador = clasificador.fit(X_train, y_train)

    print 'Almacenando modelo en /MODELOS/' + nombre + '.pickle'
    with open('../MODELOS/'+ nombre +'.pickle', 'wb') as handle:
        pickle.dump(clasificador, handle)
    handle.close()

    print 'Almacenando vectorizer en /VECTORIZER/vectorizer_'+ nombre +'.pickle'
    with open('../VECTORIZER/vectorizer_'+ nombre +'.pickle', 'wb') as handle:
        pickle.dump(vectorizer, handle)
    handle.close()

    #Llamar a DAO para que guarde el nombre, ACC, DESV
    addClasificador(nombre, accMedio, desviacion, entrena_ini, entrena_fin)



def getClasificadoresBLL():
    return getClasificadores()
