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

    desde = entrena_ini + 'T00:00:00.000Z'
    desde = dateutil.parser.parse(desde)
    hasta = entrena_fin + 'T23:59:59.999Z'
    hasta = dateutil.parser.parse(hasta)

    tw = tweetsEntrenados.find({
                                        'fechaTweet':{
                                            '$gte': desde,
                                            '$lt':  hasta
                                        }
                                    })

    return list(tw)

def addClasificador(nombre, accMedio, desviacion, entrena_ini, entrena_fin):

    desde = entrena_ini + 'T00:00:00.000Z'
    desde = dateutil.parser.parse(desde)
    hasta = entrena_fin + 'T23:59:59.999Z'
    hasta = dateutil.parser.parse(hasta)

    modelo = {
                'nombre': nombre,
                'accuracy': accMedio,
                'desviacion': desviacion,
                'entrena_ini': desde,
                'entrena_fin': hasta,
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
                                    })

    return ((list(clasificador))[0])['nombre']


def updateClasificador(nombre, accMedio, desviacion, entrena_ini, entrena_fin):

    desde = entrena_ini + 'T00:00:00.000Z'
    desde = dateutil.parser.parse(desde)
    hasta = entrena_fin + 'T23:59:59.999Z'
    hasta = dateutil.parser.parse(hasta)

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
                                'entrena_ini': desde,
                                'entrena_fin': hasta,
                                'fecha_creacion': datetime.now()
                                }
                            }
    )
