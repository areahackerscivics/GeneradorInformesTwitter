#!/usr/bin/env python
# encoding: utf-8

import sys, os
import numpy as np
import datetime
parent_dir=os.getcwd()
path= os.path.dirname(parent_dir)
sys.path.append(path)

from vectorizador import vectorizar

def transTwToTxt(listaTweets):
    labels = []
    textos = []
    for tw in listaTweets:
        etiqueta = (str(tw['categoria'].encode('utf-8')))

        if etiqueta == 'Ciencia y tecnología':
            etq = 0
        elif etiqueta == 'Comercio':
            etq = 1
        elif etiqueta == 'Cultura y ocio':
            etq = 2
        elif etiqueta == 'Demografía':
            etq = 3
        elif etiqueta == 'Deporte':
            etq = 4
        elif etiqueta == 'Economía':
            etq = 5
        elif etiqueta == 'Educación':
            etq = 6
        elif etiqueta == 'Empleo':
            etq = 7
        elif etiqueta == 'Energía':
            etq = 8
        elif etiqueta == 'Hacienda':
            etq = 9
        elif etiqueta == 'Industria':
            etq = 10
        elif etiqueta == 'Legislación y justicia':
            etq = 11
        elif etiqueta == 'Medio ambiente':
            etq = 12
        elif etiqueta == 'Medio Rural':
            etq = 13
        elif etiqueta == 'Salud':
            etq = 14
        elif etiqueta == 'Sector público':
            etq = 15
        elif etiqueta == 'Seguridad':
            etq = 16
        elif etiqueta == 'Sociedad y bienestar':
            etq = 17
        elif etiqueta == 'Transporte':
            etq = 18
        elif etiqueta == 'Turismo':
            etq = 19
        elif etiqueta == 'Urbanismo e infraestructuras':
            etq = 20
        #elif etiqueta == 'Vivienda':
        else:
            etq = 21

        labels.append(etq)

        texto = (str(tw['texto'].encode('utf-8')))


        textos.append(texto)


    return textos, labels

def transTwToTxtClas(listaTweets):
    textos = []
    for tw in listaTweets:
        texto = tw['texto']
        textos.append(texto)
    return textos