#!/usr/bin/env python
# encoding: utf-8

import time
from datetime import datetime
from pymongo import MongoClient#Libreria Mongodb

from conexionMongo import *

#Conexion a MongoDB
conexion = getConexion()
client = MongoClient(conexion)
tdb = getDB()
db = client[tdb]
coleccion = getCollTweets()
tweetsdb = db[coleccion]

#Conexion a MongoDB
cliente = MongoClient()#Inicializar objeto
cliente = MongoClient('127.0.0.1', 27017)#Indicar parametros del servidor
bd = cliente.twitter#Seleccionar Schema
tweetsdb = bd.tweets#Seleccionar Coleccion para buscar

idt=[]
tweet=[]
def leer(fechaini,fechafin):
    fechaini=datetime.strptime(fechaini,"%Y-%m-%d")
    fechafin=datetime.strptime(fechafin,"%Y-%m-%d")
    #for text in tweetsdb.find({"idioma":"es","consulta": "@AjuntamentVLC", "fechaDescarga":"22-03-17"},{"idt":1,"tweet":1,"_id":0}) :
    for text in tweetsdb.find({"idioma":"es","consulta": "@AjuntamentVLC", "fecha":{ "$gt" :fechaini ,"$lt" :fechafin}},{"idt":1,"tweet":1,"_id":0}) :
        idt.append(str(text['idt']))
        tweet.append(str(text['tweet'].encode('utf-8')))
    return idt,tweet
