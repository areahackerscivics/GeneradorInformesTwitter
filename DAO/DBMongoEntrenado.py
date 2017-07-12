#!/usr/bin/env python
# encoding: utf-8

u"""Módulo de Acceso a datos de los textos usados de Entrenamiento.

Este módulo contiene los métodos que permiten consultar e Insertar
campos de la colección que contiene los textos usados de Entrenamiento
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
    """Método que permite leer un archivo csv.

    Para que el archivo pueda ser leido debe existir dentro de la carpeta DAO una carpeta input con el archivo
    que se necesita leer.
    El proceso es simple. Se lee el archivo,linea a linea se va almacenando en un diccionario que va guardando
    uno a uno en la colección

    Args:
    fecha: Toma la fecha de hoy
    idt (list):Se espera una lista de N textos que estan en la  posicion 0 del archivo csv.
    texto (list): Se espera una lista de N textos que estan en la posicion 2 del archivo csv.
    categoria (list): Se espera una lista de N categorias que estan en la posicion 1 del archivo csv.
    Nota: No se está usando
    """
    datafile = os.path.join(path2,dfile)

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
    #fechat=datetime.strptime(fechat,"%Y-%m-%d")
    #print fechat
    guardar={
        "idt":idt,
        "categoria":categoria,
        "texto":texto,
        "fecha":today,
        "reentreno":True,
        "fechaTweet":fechat #lo ingresa como sstring VERIFICAR
        };
    print 'guardar',guardar
    try:
        tweetsdb.insert_one(guardar)#Almacenar #1
    except:
        print "No se pudo guardar"
    print 'Tweets guardado exitosamente'

def leer_textoentrenado():
    """Método que permite leer  la colección de textos entrenados.

    Se  consulta  la colección utilizando un find sin condiciones para que muestre
    todos los registros.

    Resultado:
    texto (list): Se espera una lista de N textos que estan en la posicion 2 del archivo csv.
    categoria (list): Categoía que se le ha asignado a los textos de forma manual.
    Nota: Se está usando para la ventana xxxxx
    """
    categoria=[]
    texto=[]
    for text in tweetsdb.find({},{"categoria":1,"texto":1,"_id":0}):
        categoria.append(str(text['categoria'].encode('utf-8')))
        texto.append(str(text['texto'].encode('utf-8')))
    if len(texto)>0:#validación
        return categoria,texto
        print ' Los tweets han sido cargados'
    else:
        return -1,-1
