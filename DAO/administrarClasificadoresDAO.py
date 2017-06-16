import sys, os
import numpy as np
import datetime
parent_dir=os.getcwd()
path= os.path.dirname(parent_dir)
sys.path.append(path)

from pymongo import MongoClient
from conexionMongo import *

from datetime import datetime

def getTweetsClasificados(entrena_ini, entrena_fin):

    conexion = getConexion()
    client = MongoClient(conexion)
    tdb = getDB()
    db = client[tdb]
    coleccion = getCollEntrenado()
    tweetsClasificados = db[coleccion]

    desde = entrena_ini + 'T00:00:00.000Z'
    desde = parse(desde)
    hasta = entrena_fin + 'T23:59:59.999Z'
    hasta = parse(hasta)

    tw = tweetsClasificados.find({
                                        'fechaTweet':{
                                            '$gte': desde,
                                            '$lt':  hasta
                                        }
                                    })

    return list(tw)

def addClasificador(nombre, accMedio, desviacion, entrena_ini, entrena_fin):

    desde = entrena_ini + 'T00:00:00.000Z'
    desde = parse(desde)
    hasta = entrena_fin + 'T23:59:59.999Z'
    hasta = parse(hasta)

    modelo = {
                'nombre': nombre,
                'accuracy': accMedio,
                'desviacion': desviacion,
                'entrena_ini': desde,
                'entrena_fin': hasta,
                'fecha_creacion': datetime.now()
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
    clasificadores = db[coleccion]

    return list(clasificadores)
