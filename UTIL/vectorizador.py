#!/usr/bin/env python
# encoding: utf-8

import sys, os
import numpy as np
import datetime
parent_dir=os.getcwd()
path= os.path.dirname(parent_dir)
sys.path.append(path)

import pickle

from DAO.administrarClasificadoresDAO import getClasiDefecto

from contraerPalabras import CONTRACCION_MAPA
from normalizacion import normalizar_corpus, expandir_contracciones, eliminar_caracteres_especiales

from sklearn.feature_extraction.text import TfidfVectorizer

from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords

stemmer = SnowballStemmer('spanish')
stopwords = set(stopwords.words('spanish'))

'''
def preprocesador(document):
    return document.lower()

def tokenizador(s):
    texto = expandir_contracciones(s, CONTRACCION_MAPA)
    texto = eliminar_caracteres_especiales(texto)
    wordlist = texto.split()
    palabras = [stemmer.stem(w) for w in wordlist if w not in stopwords]

    return palabras
'''

def vectorizar(textos, nombre):
    textosNormalizados = normalizar_corpus(textos)
    #vectorizer = TfidfVectorizer(preprocessor=preprocesador, tokenizer=tokenizador)
    vectorizer = TfidfVectorizer()
    vectorizer = vectorizer.fit(textosNormalizados)
    data = vectorizer.transform(textosNormalizados)
    data = data.toarray()

    print 'Almacenando vectorizer en /VECTORIZER/vectorizer_'+ nombre +'.pickle'
    #vectorizer.preprocessor = None
    #vectorizer.tokenizer = None
    with open('../VECTORIZER/vectorizer_'+ nombre +'.pickle', 'wb') as handle:
        pickle.dump(vectorizer, handle)

    return data

def transformar(textos, nombre):
    textosNormalizados = normalizar_corpus(textos)
    with open('../VECTORIZER/vectorizer_'+ nombre +'.pickle', "rb") as input_file:
        vectorizador = pickle.load(input_file)

    data = vectorizador.transform(textosNormalizados)
    data = data.toarray()

    return data
