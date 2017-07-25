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

def convNumToNom(num):
    dicNumToNom={
    0:'Ciencia y tecnología',
    1:'Comercio',
    2:'Cultura y ocio',
    3:'Demografía',
    4:'Deporte',
    5:'Economía',
    6:'Educación',
    7:'Empleo',
    8:'Energía',
    9:'Hacienda',
    10:'Industria',
    11:'Legislación y justicia',
    12:'Medio ambiente',
    13:'Medio Rural',
    14:'Salud',
    15:'Sector público',
    16:'Seguridad',
    17:'Sociedad y bienestar',
    18:'Transporte',
    19:'Turismo',
    20:'Urbanismo e infraestructuras',
    21:'Vivienda'
    }

    categoria=dicNumToNom[num]
    return categoria
