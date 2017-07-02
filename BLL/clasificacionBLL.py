#!/usr/bin/env python
# encoding: utf-8

import sys, os, io
import time
from datetime import datetime
from pymongo import MongoClient#Libreria Mongodb
parent_dir=os.getcwd()
path= os.path.dirname(parent_dir)
sys.path.append(path)

import operator
from DAO.clasificacionDAO import *
from UTIL.vectorizador import *
from UTIL.procesopickle import *
from UTIL.normalizacion import *



def generar_clasificacionBLL(fechaTw):
    #1--------------------cargar el corpus-------------------

    idt,corpus,fechaTweet =leer(fechaTw)#DBMongoTweet
    if idt!=-1:#validación del método leer, por si no hay registros
        #CONSULTAR EN BASE DE DATOS EL NOMBRE DEL CLASIFICADOR (DAO)
        nombre=getClasiDefecto()

        if nombre!=-1:#validación de vacion
            tfidf=transformar(corpus,nombre)
            SGDtfidf=leer_Pickle('../MODELOS/'+ nombre +'.pickle')

            print 'Se ha usado el vectorizador....'
            clases=SGDtfidf.classes_ #generando las clases

            puntaje=SGDtfidf.decision_function(tfidf) #generando puntajes
            print 'Se ha usado el clasificador....'
            #4--------------------Guardar  en db Clasificador-------------------
            guardar_textoclasificados(corpus,puntaje,clases,idt,fechaTweet)

def generar_tabla():
    fechaTweet=[]
    fechaClas=[]
    totalTweet=[]
    faltaTweet=[]
    diccTW=leer_AgrupadoxfechaTW()#DBMongoTweet
    diccCL=leer_Agrupadoxfecha()#DBMongoClasificado
    if len(diccTW)>0:#validación
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
    else:
        dato=["No hay datos"]
        dicc={"fechaTweet":dato, "totalTweet":dato,"faltaTweet":dato,"fechaClas":dato,"fechaini":"2017-01-01", "fechafin":"2017-01-01"}
        return dicc
