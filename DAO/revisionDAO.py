#!/usr/bin/env python
# encoding: utf-8
u"""Módulo de Acceso a datos de los textos descargados de Twitter.

Este módulo contiene los métodos que permiten consultar
campos de la colección que contiene los textos descargados de Twitter
"""
import sys, os
from datetime import datetime
from pymongo import MongoClient#Libreria Mongodb
parent_dir=os.getcwd()
path= os.path.dirname(parent_dir)
sys.path.append(path)


#REAL
from conexionMongo import *

#Conexion a MongoDB
conexion = getConexion()
client = MongoClient(conexion)
tdb = getDB()
db = client[tdb]
coleccion = getCollTweetsClas()
tweetsdb = db[coleccion]

def getreentre(cat, fechaini, fechafin):

    fechaini = fechaini + ' 00:00:00'
    fechaini=datetime.strptime(fechaini,"%Y-%m-%d %H:%M:%S")
    fechafin = fechafin + ' 23:59:59'
    fechafin=datetime.strptime(fechafin,"%Y-%m-%d %H:%M:%S")
    # fechaini=datetime.strptime(fechaini,"%Y-%m-%d")
    # fechafin=datetime.strptime(fechafin,"%Y-%m-%d")
    reentre= tweetsdb.find({"estado": {"$exists":True},"categoria":cat,
    "fecha":{ "$gte" :fechaini ,"$lt" :fechafin}}).count()
    return reentre #no es necesario ponerle la validación

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

def actualizar_textoclasificados(idt,estado):
    try:
        tweetn=tweetsdb.find_one({'idt':idt})
        reg_id=tweetn['_id']
        result = tweetsdb.update_one({'_id':reg_id},
                                     {'$set':{'estado':estado}})
        print "Registros actualizados: ", result.matched_count
    except:
        print "No se pudo actualizar"

def guardar_textoreentrenado(texto,categoria,idt, fechat):
    """Método que permite Insertar textos en el momento de hacer reentrenamiento.
    #
    # Se consulta  la colección utilizando un find sin condiciones para que muestre
    # todos los registros.
    # que se necesite leer.
    #
    # Resultado:
    # texto (list): Se espera una lista de N textos que estan en la posicion 2 del archivo csv.
    # categoria (list): Categoía que se le ha asignado a los textos de forma manual.
    # Nota:Se está usando para la ventana revision, a través de la llamada desde revisionBLL
    """

    coleccion = getCollEntrenado()
    tweetsdb = db[coleccion]
    guardar={
        "idt":idt,
        "categoria":categoria,
        "texto":texto,
        "fecha":datetime.now(),
        "reentreno":True,
        "fechaTweet":fechat #lo ingresa como sstring VERIFICAR
        };
    try:
        tweetsdb.insert_one(guardar)#Almacenar #1
    except:
        print "No se pudo guardar"
    print 'Tweets guardado exitosamente'
