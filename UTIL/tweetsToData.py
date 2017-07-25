#!/usr/bin/env python
# encoding: utf-8

import sys, os
import numpy as np
import datetime
parent_dir=os.getcwd()
path= os.path.dirname(parent_dir)
sys.path.append(path)

import pickle


from tweetsToText import transTwToTxt
from vectorizador import transformar

def transform(listaTweets, nombre):

    textos, labels = transTwToTxt(listaTweets)

    data = transformar(textos, nombre)

    return data, labels

def transformClas(listaTweets, nombre):

    textos = transTwToTxtClas(listaTweets)

    data = transformar(textos, nombre)

    return data
