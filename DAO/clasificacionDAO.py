#!/usr/bin/env python
# encoding: utf-8
u"""Módulo de Acceso a datos de los textos descargados de Twitter.

Este módulo contiene los métodos que permiten consultar
campos de la colección que contiene los textos descargados de Twitter
"""
import sys, os
import datetime
from pymongo import MongoClient#Libreria Mongodb
parent_dir=os.getcwd()
path= os.path.dirname(parent_dir)
sys.path.append(path)
from UTIL.tweetsToText import *

#REAL
from conexionMongo import *

#Conexion a MongoDB
conexion = getConexion()
client = MongoClient(conexion)
tdb = getDB()
db = client[tdb]


def leer(fechaTw):#modificado fecha_creacion
    """Método que permite leer  la colección de textos descargados de Twitter.

    Se  consulta la colección utilizando un find con varias condiciones, como son:
        El idioma debe estar en español
        Los tweets deben ser aquellos que se refieran a @AjuntamentVLC
        La fecha en la que se descargó el tweet sea mayor o igual a la fecha inicial
        y menor que la fecha final.

    Arg:
    fechaini: Fecha inicial
    fechafin: Fecha final

    Resultado:
    idt (list): .
    categoria (list): Categoía que se le han asignados a los textos de forma manual.
    Nota: Se está usando para la ventana xxxxx
    """
    coleccion = getCollTweets()
    tweetsdb = db[coleccion]
    idt=[]
    tweet=[]
    fechaTweet=[]
    pipeline=[{ "$match": { "idioma":"es","consulta": "@AjuntamentVLC"}},
              {"$project": {"idt":1,"tweet":1,"_id":0,"fecha_creacion":1,
              "fechaTw":
                        { "$dateToString": { "format": "%Y-%m", "date": "$fecha_creacion" } }}},
              { "$match": { "fechaTw":fechaTw} }]
    for text in tweetsdb.aggregate(pipeline):
        idt.append(str(text['idt']))
        tweet.append(str(text['tweet'].encode('utf-8')))
        fechaTweet.append(text['fecha_creacion'])
    if len(idt)>0:
        return idt,tweet,fechaTweet
    else:
        return -1, -1, -1

def leer_AgrupadoxfechaTW():#modificado fecha_creacion
    coleccion = getCollTweets()
    tweetsdb = db[coleccion]
    dicc={}
    pipeline=[{"$match":{"consulta": "@AjuntamentVLC", "idioma":"es",}},#cambiar por"es"
              {"$project": {"_id":0,
                            "fechaTweet": { "$dateToString": { "format": "%Y-%m", "date": "$fecha_creacion" } } }},
              {"$group":{"_id":{"fechaTweet":"$fechaTweet"},"total":{"$sum":1}}},
              {"$project": {"_id":0,"fechaTweet":"$_id.fechaTweet", "Total_Tweets":"$total"}},
              {"$sort":{"fechaTweet":1}}]
    for text in tweetsdb.aggregate(pipeline):
        dicc[text['fechaTweet']]=text['Total_Tweets']
    if len(dicc)>0:#validación
        return dicc
    else:
        return {}

############Con la data de clasificación#########################
def leer_Agrupadoxfecha():#modificado fecha_creacion=fechaTweet
    coleccion = getCollTweetsClas()
    tweetsdb = db[coleccion]

    dicc={}
    pipeline=[{"$project": {"_id":0,
                            "fecha":1,
                            "fechaTweet": { "$dateToString": { "format": "%Y-%m", "date": "$fechaTweet" } } }},
              {"$group":{"_id":{"fechaTweet":"$fechaTweet"},"total":{"$sum":1},"fechaDescargaMax": {"$max":"$fecha"}}},
              {"$project": {"_id":0,"fechaTweet":"$_id.fechaTweet","fechaDescargaMax":1, "Total_Tweets":"$total"}},
              {"$sort":{"fechaTweet":1}}]
    for text in tweetsdb.aggregate(pipeline):
         dicc[text['fechaTweet']]=[text['Total_Tweets'],text['fechaDescargaMax']]
    if len(dicc)>0:#validación
        return dicc
    else:
        return {}

def guardar_textoclasificados(corpus,puntaje,clases,idt,fechaTweet):
    coleccion = getCollTweetsClas()
    tweetsdb = db[coleccion]
    today=datetime.datetime.now()
    for i in range(len(corpus)):
        lista= sorted(zip(puntaje[i],  clases), reverse=True)
        categoria=convNumToNom(lista[0][1])
        guardar={
            "categoria":categoria.decode('utf-8'),
            "puntaje":lista[0][0],
            "idt":idt[i], #1
            "texto":corpus[i].decode('utf-8'),
            "fecha":today,
            "fechaTweet":fechaTweet[i]
            };
        try:
            tweetsdb.insert_one(guardar)#MIRAR SI SE PUEDE MEJORAR EL INSERT (INSERT MANY)
        except:
                print "No se pudo guardar"
    print 'Han sido clasificados ',len(corpus),'tweets'

############Con la data de clasificadores#########################
def getClasiDefecto():
    nombre=[]
    coleccion = getCollClasificadores()
    cursor = db[coleccion]

    # comienzo agregado por MM
    for text in cursor.find({'predeterminado': True},{"nombre":1,"_id":0}).limit(1):
        nombre.append(str(text['nombre']))
    if len(nombre)>0: #validación
        return nombre[0]
    else:
        return -1
    # fin agregado por MM
