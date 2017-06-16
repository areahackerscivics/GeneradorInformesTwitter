#!/usr/bin/env python
# encoding: utf-8

#import jsonpickle
#import tweepy
import random
#import datetime
from datetime import datetime
from pymongo import MongoClient#Libreria Mongodb

from conexionMongo import *

#Conexion a MongoDB
conexion = getConexion()
client = MongoClient(conexion)
tdb = getDB()
db = client[tdb]
coleccion = getCollTweetsClas()
tweetsdb = db[coleccion]

def actualizar_textoclasificados(idt,estado):
    try:
        tweetn=tweetsdb.find_one({'idt':idt})
        reg_id=tweetn['_id']
        result = tweetsdb.update_one({'_id':reg_id},
                                     {'$set':{'estado':estado}})
        print "Registros actualizados: ", result.matched_count
    except:
        print "No se pudo actualizar"

def guardar_textoclasificados(corpus,puntaje,clases,idt):
    y_pred=[]
    today=datetime.now()
    for i in range(len(corpus)):
        lista= sorted(zip(puntaje[i],  clases), reverse=True)
        y_pred.append(lista[0][1])#lista de las categorias predicas, acertadas y erradas
        guardar={
            "categoria":lista[0][1].decode('utf-8'),
            "puntaje":lista[0][0],
            "idt":idt[i], #1
            "texto":corpus[i].decode('utf-8'),
            "fecha":today
            };
        try:
            tweetsdb.insert_one(guardar)#Almacenar #1
        except:
                print "No se pudo guardar"
    print 'Han sido clasificados ',len(corpus),'tweets'


def leer_ClasificadosconEstado(cat, fechaini, fechafin):
    fechaini=datetime.strptime(fechaini,"%Y-%m-%d")
    fechafin=datetime.strptime(fechafin,"%Y-%m-%d")
    reentre= tweetsdb.find({"estado": {"$exists":True},"categoria":cat,"fecha":{ "$gt" :fechaini ,"$lt" :fechafin}}).count()
    return reentre

def leer_textoclasificadoUno():
    idt=[]
    categoria=[]
    texto=[]
    contar=tweetsdb.find({"estado": {"$exists":False}}).count()
    randomico=random.randint(0,contar)
    for text in tweetsdb.find({"estado": {"$exists":False}},{"idt":1,"categoria":1,"texto":1,"_id":0}).limit(1).skip(randomico):
        idt.append(str(text['idt']))
        categoria.append(str(text['categoria'].encode('utf-8')))
        texto.append(str(text['texto'].encode('utf-8')))
    return idt,categoria,texto

def leer_textoclasificadoTodo(cat, num, fechaini, fechafin):
    idt=[]
    categoria=[]
    texto=[]
    fechaini=datetime.strptime(fechaini,"%Y-%m-%d")
    fechafin=datetime.strptime(fechafin,"%Y-%m-%d")
    for text in tweetsdb.find({"estado": {"$exists":False},"categoria":cat,"fecha":{ "$gt" :fechaini ,"$lt" :fechafin}},
                              {"idt":1,"categoria":1,"texto":1,"_id":0}).limit(int(num)):
        idt.append(str(text['idt']))
        categoria.append(str(text['categoria'].encode('utf-8')))
        texto.append(str(text['texto'].encode('utf-8')))
    return idt,categoria,texto

def leer_textoclasificadoxfecha():#para la pantalla clasificar
    fechaClasificacion=[]
    fechaTweet=[]
    total=[]

    pipeline=[{
      "$lookup":
        {
          "from": "tweets",
          "localField": "idt",
          "foreignField": "idt",
          "as": "tweets_docs"
        }
   },
   {"$project":
       {
           "fechaTweet": "$tweets_docs.fechaDescarga" ,"_id":0,
           "fechaClasificacion": { "$dateToString": { "format": "%Y-%m-%d", "date": "$fecha" } } }
   },
  {"$group":{"_id":{"fechaClasificacion":"$fechaClasificacion","fechaTweet":"$fechaTweet"},"total":{"$sum":1}}},
  {"$project":
       {
           "fechaClasificacion":"$_id.fechaClasificacion",
           "fechaTweet":"$_id.fechaTweet",
           "total":"$total",
           "_id":0
           }}]
    for text in tweetsdb.aggregate(pipeline):
        fechaClasificacion.append(text['fechaClasificacion'])
        fechaTweet.append(text['fechaTweet'][0])
        total.append(text['total'])
