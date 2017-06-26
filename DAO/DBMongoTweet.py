#!/usr/bin/env python
# encoding: utf-8

import time
from datetime import datetime
from pymongo import MongoClient#Libreria Mongodb

#REAL
from conexionMongo import *

#Conexion a MongoDB
conexion = getConexion()
client = MongoClient(conexion)
tdb = getDB()
db = client[tdb]
coleccion = getCollTweets()
tweetsdb = db[coleccion]

#Declaración de variables
dicc={}
def leer(fechaini,fechafin):
    idt=[]
    tweet=[]
    fechaTweet=[]
    fechaini=datetime.strptime(fechaini,"%Y-%m-%d")
    fechafin=datetime.strptime(fechafin,"%Y-%m-%d")
    #for text in tweetsdb.find({"idioma":"es","consulta": "@AjuntamentVLC", "fechaDescarga":"22-03-17"},{"idt":1,"tweet":1,"_id":0}) :
    for text in tweetsdb.find({"idioma":"es","consulta": "@AjuntamentVLC", "fechaTweet":{ "$gt" :fechaini ,"$lt" :fechafin}},{"idt":1,"tweet":1,"fechaTweet":1,"_id":0}) :
        idt.append(str(text['idt']))
        tweet.append(str(text['tweet'].encode('utf-8')))
        fechaTweet.append(text['fechaTweet'])
    return idt,tweet,fechaTweet

def leer_AgrupadoxfechaTW():#para la ventana Clasificar
    dicc={}
    pipeline=[{"$match":{"consulta": "@AjuntamentVLC", "idioma":"es",}},
              {"$project": {"_id":0,
                            "fechaTweet": { "$dateToString": { "format": "%Y-%m-%d", "date": "$fechaTweet" } } }},
              {"$group":{"_id":{"fechaTweet":"$fechaTweet"},"total":{"$sum":1}}},
              {"$project": {"_id":0,"fechaTweet":"$_id.fechaTweet", "Total_Tweets":"$total"}},
              {"$sort":{"fechaTweet":1}}]
    for text in tweetsdb.aggregate(pipeline):
        dicc[text['fechaTweet']]=text['Total_Tweets']
    return dicc
    
