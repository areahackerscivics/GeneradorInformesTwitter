#!/usr/bin/env python
# encoding: utf-8

import sys, os
import time
from pymongo import MongoClient#Libreria Mongodb
parent_dir=os.getcwd()
path= os.path.dirname(parent_dir)
sys.path.append(path)

import operator
from DAO.DBMongoTweet import *
from DAO.DBMongoClasificado import *
from DAO.administrarClasificadoresDAO import *
from UTIL.vectorizador import *
from UTIL.procesopickle import *
from UTIL.normalizacion import *


def generar_clasificacionBLL(fechaini,fechafin):
    #1--------------------cargar el corpus-------------------
    if fechaini==None:
        fechaini= "2017-01-01"
    if fechafin==None:
        fechafin= "2017-05-01"
    idt,corpus,fechaTweet =leer(fechaini,fechafin)
    if len(idt)>0:
        #CONSULTAR EN BASE DE DATOS EL NOMBRE DEL CLASIFICADOR (DAO)
        nombre=getClasiDefecto()
        tfidf=transformar(corpus,nombre)
        SGDtfidf=leer_Pickle('../MODELOS/'+ nombre +'.pickle')

        print 'Se ha usado el vectorizador....'
        clases=SGDtfidf.classes_ #generando las clases
        #CONSULTAR EN BASE DE DATOS EL NOMBRE DEL CLASIFICADOR (DAO)
        puntaje=SGDtfidf.decision_function(tfidf) #generando puntajes
        print 'Se ha usado el clasificador....'
        #4--------------------Guardar  en db Clasificador-------------------
        guardar_textoclasificados(corpus,puntaje,clases,idt,fechaTweet)
        dicc={"fechaini":fechaini, "fechafin":fechafin}
        return dicc

def generar_tabla():
    fechaTweet=[]
    fechaClas=[]
    totalTweet=[]
    faltaTweet=[]
    diccTW=leer_AgrupadoxfechaTW()
    diccCL=leer_Agrupadoxfecha()
    #Compara lo que está en las dos colecciones para determinar si faltan
    #Tweets por clasificar dependiendo de la fecha
    for keyTW, valueTW in diccTW.iteritems():#recorriendo el diccionario de la coll tweets
        for keyCL, valueCL in diccCL.iteritems():#recorriendo el diccionario de la coll clasificado
            if keyTW==keyCL:
                diccTW[keyTW]=[valueTW,valueTW-valueCL[0],valueCL[1]]#añadir al diccionario coll tweets la resta de los totales

    resultado = sorted(diccTW.items(), key=operator.itemgetter(0))
    for i in range (len(resultado)):
        valueTW= resultado[i][1]
        if type(valueTW)==list:
            fechaTweet.append(resultado[i][0])
            totalTweet.append(valueTW[0])
            faltaTweet.append(valueTW[1])
            fechaClas.append(valueTW[2])
        else:
            fechaTweet.append(resultado[i][0])
            totalTweet.append(valueTW)
            faltaTweet.append(valueTW)
            fechaClas.append("Ninguna")

    dicc={"fechaTweet":fechaTweet, "totalTweet":totalTweet,"faltaTweet":faltaTweet,"fechaClas":fechaClas,"fechaini":"2017-01-01", "fechafin":"2017-01-01"}
    return dicc
