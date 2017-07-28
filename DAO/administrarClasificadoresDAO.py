#!/usr/bin/env python
# encoding: utf-8
import sys, os
import numpy as np
parent_dir=os.getcwd()
path= os.path.dirname(parent_dir)
sys.path.append(path)

from pymongo import MongoClient
from conexionMongo import *

from datetime import datetime
import dateutil.parser

def getTweetsClasificados(entrena_ini, entrena_fin):

    conexion = getConexion()
    client = MongoClient(conexion)
    tdb = getDB()
    db = client[tdb]
    coleccion = getCollEntrenado()
    tweetsEntrenados = db[coleccion]

    entrena_ini = entrena_ini + ' 00:00:00'
    entrena_ini=datetime.strptime(entrena_ini,"%Y-%m-%d %H:%M:%S")

    entrena_fin = entrena_fin + ' 23:59:59'
    entrena_fin=datetime.strptime(entrena_fin,"%Y-%m-%d %H:%M:%S")

    tw = tweetsEntrenados.find({
                                        'fechaTweet':{
                                            '$gte': entrena_ini,
                                            '$lt':  entrena_fin
                                        }
                                    })

    return list(tw)

def getTweetsClasificadosMM(fechaini,fechafin):

    conexion = getConexion()
    client = MongoClient(conexion)
    tdb = getDB()
    db = client[tdb]
    coleccion = getCollEntrenado()
    tweetsEntrenados = db[coleccion]

    #idt=[]
    texto=[]
    categoria=[]
    fechaini=datetime.strptime(fechaini,"%Y-%m-%d")
    fechafin=datetime.strptime(fechafin,"%Y-%m-%d")
    #for text in tweetsdb.find({"idioma":"es","consulta": "@AjuntamentVLC", "fechaDescarga":"22-03-17"},{"idt":1,"tweet":1,"_id":0}) :
    for text in tweetsEntrenados.find({"fechaTweet":{ "$gt" :fechaini ,"$lt" :fechafin}},{"categoria":1,"texto":1,"_id":0}) :
        categoria.append(str(text['categoria'].encode('utf-8')))
        texto.append(str(text['texto'].encode('utf-8')))

    return texto,categoria

def addClasificador(nombre, accMedio, desviacion, entrena_ini, entrena_fin):

    entrena_ini = entrena_ini + ' 00:00:00'
    entrena_ini=datetime.strptime(entrena_ini,"%Y-%m-%d %H:%M:%S")

    entrena_fin = entrena_fin + ' 23:59:59'
    entrena_fin=datetime.strptime(entrena_fin,"%Y-%m-%d %H:%M:%S")

    modelo = {
                'nombre': nombre,
                'accuracy': accMedio,
                'desviacion': desviacion,
                'entrena_ini': entrena_ini,
                'entrena_fin': entrena_fin,
                'fecha_creacion': datetime.now(),
                'predeterminado': False
    }

    conexion = getConexion()
    client = MongoClient(conexion)
    tdb = getDB()
    db = client[tdb]
    coleccion = getCollClasificadores()
    clasificadores = db[coleccion]

    post_id = clasificadores.insert(modelo)

def getClasificadores():
    conexion = getConexion()
    client = MongoClient(conexion)
    tdb = getDB()
    db = client[tdb]
    coleccion = getCollClasificadores()
    cursor = db[coleccion]
    clasificadores = cursor.find({})

    return list(clasificadores)


def eliminarClasificadorDAO(nombre):
    conexion = getConexion()
    client = MongoClient(conexion)
    tdb = getDB()
    db = client[tdb]
    coleccion = getCollClasificadores()
    cursor = db[coleccion]


    result = cursor.delete_one({'nombre': nombre})

    if result.deleted_count != 1:
        raise Exception('Ha fallado el eliminar el clasificador ' + nombre)


def getClasiDefecto():
    conexion = getConexion()
    client = MongoClient(conexion)
    tdb = getDB()
    db = client[tdb]
    coleccion = getCollClasificadores()
    cursor = db[coleccion]
    clasificador = cursor.find({
                                        'predeterminado': True
                                    }).limit(1)

    return ((list(clasificador))[0])['nombre']


def editarClasificadorDAO(nombreOri, nombreNuev, predeterminado):
    conexion = getConexion()
    client = MongoClient(conexion)
    tdb = getDB()
    db = client[tdb]

    coleccion = getCollClasificadores()
    cursor = db[coleccion]


    if predeterminado != None:

        #Primero busco el clasificador que actualmente es el predeterminado
        clasificador =cursor.find_one({'predeterminado':True})
        reg_id=clasificador['_id']

        result = cursor.update_one(
                                {'_id':reg_id},
                                {'$set':{
                                    'nombre':nombreNuev,
                                    'predeterminado':False
                                    }
                                }
        )

        if nombreNuev != None:
            #Luego busco el que queremos cambiar y actualizamos informacion
            clasificador =cursor.find_one({'nombre':nombreOri})
            reg_id=clasificador['_id']

            result = cursor.update_one(
                                    {'_id':reg_id},
                                    {'$set':{
                                        'nombre':nombreNuev,
                                        'predeterminado':True
                                        }
                                    }
            )

        else:
            clasificador =cursor.find_one({'nombre':nombreOri})
            reg_id=clasificador['_id']

            result = cursor.update_one(
                                    {'_id':reg_id},
                                    {'$set':{
                                        'predeterminado':True
                                        }
                                    }
            )

    else:
        if nombreNuev != None:
            clasificador =cursor.find_one({'nombre':nombreOri})
            reg_id=clasificador['_id']

            result = cursor.update_one(
                                    {'_id':reg_id},
                                    {'$set':{
                                        'nombre':nombreNuev
                                        }
                                    }
            )



def updateClasificador(nombre, accMedio, desviacion, entrena_ini, entrena_fin):

    entrena_ini = entrena_ini + ' 00:00:00'
    entrena_ini=datetime.strptime(entrena_ini,"%Y-%m-%d %H:%M:%S")
    entrena_fin = entrena_fin + ' 23:59:59'
    entrena_fin=datetime.strptime(entrena_fin,"%Y-%m-%d %H:%M:%S")

    conexion = getConexion()
    client = MongoClient(conexion)
    tdb = getDB()
    db = client[tdb]

    coleccion = getCollClasificadores()
    cursor = db[coleccion]

    clasificador =cursor.find_one({'nombre':nombre})
    reg_id=clasificador['_id']

    result = cursor.update_one(
                            {'_id':reg_id},
                            {'$set':{
                                'accuracy': accMedio,
                                'desviacion': desviacion,
                                'entrena_ini': entrena_ini,
                                'entrena_fin': entrena_fin,
                                'fecha_creacion': datetime.now()
                                }
                            }
    )
