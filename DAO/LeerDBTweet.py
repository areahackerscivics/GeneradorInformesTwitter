#!/usr/bin/env python
# encoding: utf-8

import jsonpickle
import tweepy
import time
from pymongo import MongoClient#Libreria Mongodb

#Conexion a MongoDB
cliente = MongoClient()#Inicializar objeto
cliente = MongoClient('127.0.0.1', 27017)#Indicar parametros del servidor
bd = cliente.twitter#Seleccionar Schema
tweetsdb = bd.tweets#Seleccionar Coleccion para buscar

idt=[]
tweet=[]
def leer():
    for text in tweetsdb.find({"idioma":"es","consulta": "@AjuntamentVLC"},{"idt":1,"tweet":1,"_id":0}):
        idt.append(str(text['idt']))
        tweet.append(str(text['tweet'].encode('utf-8')))
    return idt,tweet


