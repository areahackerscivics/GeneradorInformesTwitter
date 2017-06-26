#!/usr/bin/env python
# encoding: utf-8

"""
<<<a.Código de preparación de los datos>>>
@author: Marylin Mattos
"""
import os, sys, io
import time
from datetime import datetime
from pymongo import MongoClient#Libreria Mongodb
parent_dir=os.getcwd()
path= os.path.dirname(parent_dir)
path2=path+"\DAO\input\\"


#REAL
from conexionMongo import *

#Conexion a MongoDB
conexion = getConexion()
client = MongoClient(conexion)
tdb = getDB()
db = client[tdb]
coleccion = getCollEntrenado()
tweetsdb = db[coleccion]

#Declaración de variables
dfile="DataTodo.csv"
today=datetime.now()


def guardar_DataArchivo(dfile):
    datafile = os.path.join(path2,dfile)
    """lee un archivo csv.
             Args:
            texto (list): Se espera una lista de N textos que estan en la 3ra posicion del archivo csv.
            cat (list): Se espera una lista de N categorias que estan en la 4ta posicion del archivo csv.
        Nota:
            
    """
    with open(datafile, "r") as f:
        header = f.readline().split(";")
        for line in f:
            fields = line.split(";")
            tweetdb={
                "fecha":today,
                "idt":fields[0],
                "categoria":fields[1],
                "texto":fields[2].decode('utf-8')
                };
            try:
                tweetsdb.insert_one(tweetdb)#Almacenar tweet
            except:
                print "No se pudo insertar"
    print ' Los tweets han sido insertados satisfactoriamente'

def leer_textoentrenado():
    categoria=[]
    texto=[]
    for text in tweetsdb.find({},{"categoria":1,"texto":1,"_id":0}):
        categoria.append(str(text['categoria'].encode('utf-8')))
        texto.append(str(text['texto'].encode('utf-8')))
    return categoria,texto
    print ' Los tweets han sido cargados'

def guardar_textoreentrenado(texto,categoria,idt, fechat):
    guardar={
        "idt":idt,
        "categoria":categoria,
        "texto":texto,
        "fecha":today,
        "reentreno":True,
        "fechaTweet":fechat
        };
    try:
        tweetsdb.insert_one(guardar)#Almacenar #1
    except:
        print "No se pudo guardar"
    print 'Tweets guardado exitosamente'

