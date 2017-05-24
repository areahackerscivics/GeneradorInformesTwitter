#!/usr/bin/env python
# encoding: utf-8
"""
<<<f.modelos>>
"""
from sklearn.linear_model import SGDClassifier
from sklearn.svm import LinearSVC


def Crear_clasificadorSGD(bdp_entenamiento, Cat_entrenamiento):
    SGD= SGDClassifier(loss='hinge', n_iter=100)
    SGD.fit(bdp_entenamiento, Cat_entrenamiento)# construir el  model  
    return SGD

def Crear_clasificadores(clasificador, bdp_entenamiento, Cat_entrenamiento,bdp_pruebas):
    clasificador.fit(bdp_entenamiento, Cat_entrenamiento)# construir el  model  
    predecir=svm.predict(bdp_pruebas)# predecir usando el modelo
    return clasificador, predecir
    

