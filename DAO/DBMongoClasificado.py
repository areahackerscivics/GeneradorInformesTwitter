#!/usr/bin/env python
# encoding: utf-8
u"""Módulo de Acceso a datos de los textos Clasificados.

Este módulo contiene los métodos que permiten  consultar, Insertar y Actualizar
campos de la colección que contiene los textos clasificados
"""
import sys, os
import random
import datetime
from pymongo import MongoClient#Libreria Mongodb
parent_dir=os.getcwd()
path= os.path.dirname(parent_dir)
sys.path.append(path)
from UTIL.tweetsToText import *



from conexionMongo import *

#Conexion a MongoDB
conexion = getConexion()
client = MongoClient(conexion)
tdb = getDB()
db = client[tdb]
coleccion = getCollTweetsClas()
tweetsdb = db[coleccion]

#Declaración de variables

dicc={}

def actualizar_textoclasificados(idt,estado):
    try:
        tweetn=tweetsdb.find_one({'idt':idt})
        reg_id=tweetn['_id']
        result = tweetsdb.update_one({'_id':reg_id},
                                     {'$set':{'estado':estado}})
        print "Registros actualizados: ", result.matched_count
    except:
        print "No se pudo actualizar"

def guardar_textoclasificados(corpus,puntaje,clases,idt,fechaTweet):
    today=datetime.datetime.now()
    #y_pred=[]
    for i in range(len(corpus)):
        lista= sorted(zip(puntaje[i],  clases), reverse=True)
        categoria=convNumToNom(lista[0][1])
        #y_pred.append(lista[0][1])#lista de las categorias predicas, acertadas y erradas
        guardar={
            "categoria":categoria.decode('utf-8'),#Pru
            #"categoria":lista[0][1].decode('utf-8'),
            "puntaje":lista[0][0],
            "idt":idt[i], #1
            "texto":corpus[i].decode('utf-8'),
            "fecha":today,
            "fechaTweet":fechaTweet[i]
            };
        try:
            tweetsdb.insert_one(guardar)#Almacenar #1
        except:
                print "No se pudo guardar"
    print 'Han sido clasificados ',len(corpus),'tweets'


def leer_ClasificadosconEstado(cat, fechaini, fechafin):

    fechaini = fechaini + ' 00:00:00'
    fechaini=datetime.strptime(fechaini,"%Y-%m-%d %H:%M:%S")
    fechafin = fechafin + ' 23:59:59'
    fechafin=datetime.strptime(fechafin,"%Y-%m-%d %H:%M:%S")
    # fechaini=datetime.strptime(fechaini,"%Y-%m-%d")
    # fechafin=datetime.strptime(fechafin,"%Y-%m-%d")
    reentre= tweetsdb.find({"estado": {"$exists":True},"categoria":cat,"fecha":{ "$gte" :fechaini ,"$lt" :fechafin}}).count()
    return reentre #no es necesario ponerle la validación

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
    if len(idt)>0: #validación
        return idt,categoria,texto
    else:
        return -1,-1,-1

def leer_textoclasificadoTodo(cat, num, fechaini, fechafin):
    #para la ventana Revision

    idt=[]
    categoria=[]
    texto=[]
    fechaTweet=[]
    fechaini = fechaini + ' 00:00:00'
    fechaini=datetime.strptime(fechaini,"%Y-%m-%d %H:%M:%S")
    fechafin = fechafin + ' 23:59:59'
    fechafin=datetime.strptime(fechafin,"%Y-%m-%d %H:%M:%S")
    # fechaini=datetime.strptime(fechaini,"%Y-%m-%d")
    # fechafin=datetime.strptime(fechafin,"%Y-%m-%d")
    for text in tweetsdb.find({"estado": {"$exists":False},"categoria":cat,"fecha":{ "$gte" :fechaini ,"$lt" :fechafin}},
                              {"idt":1,"categoria":1,"texto":1,"fechaTweet":1,"_id":0}).limit(int(num)):
        idt.append(str(text['idt']))
        categoria.append(str(text['categoria'].encode('utf-8')))
        texto.append(str(text['texto'].encode('utf-8')))
        fechaTweet.append(text['fechaTweet'])
    if len(idt)>0: #validación
        return idt,categoria,texto,fechaTweet
    else:
        return -1,-1,-1,-1


def leer_Agrupadoxfecha():#para la ventana Clasificar
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
