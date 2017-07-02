#!/usr/bin/env python
# encoding: utf-8


import random
from datetime import datetime
import math
from pymongo import MongoClient#Libreria Mongodb

#REAL
from conexionMongo import *

#Conexion a MongoDB
conexion = getConexion()
client = MongoClient(conexion)
tdb = getDB()
db = client[tdb]
coleccion = getCollTweetsClas()
tweetsdb = db[coleccion]


def leer_CalculoxEstado(fechaini,fechafin):
    fechaini = fechaini + ' 00:00:00'
    fechaini=datetime.strptime(fechaini,"%Y-%m-%d %H:%M:%S")
    fechafin = fechafin + ' 23:59:59'
    fechafin=datetime.strptime(fechafin,"%Y-%m-%d %H:%M:%S")
    pipeline=[
        {"$match":{"estado": {"$exists":True},"fecha":{ "$gt" :fechaini ,"$lt" :fechafin}}},
        {"$group":{"_id":{"categoria":"$categoria","estado":"$estado"},
               "Subtotal":{"$sum":1}}},
        { "$group": {"_id":{"categoria":"$_id.categoria"}, "result":
               { "$push": { "estado": "$_id.estado", "Subtotal":"$Subtotal" }}}},
        {"$project":{
        "_id": "$_id",
        "R": {"$filter": {
            "input": "$result",
            "as": "resultado",
            "cond": {"$eq": ["$$resultado.estado", "R"]}
           }},
        "D": {"$filter": {
            "input": "$result",
            "as": "resultado",
            "cond": {"$eq": ["$$resultado.estado", "D"]}
           }},
        "C": {"$filter": {
            "input": "$result",
            "as": "resultado",
            "cond": {"$eq": ["$$resultado.estado", "C"]}
           }}}},
    {"$project":{
        "_id":0,
        "categoria":"$_id.categoria",
        "fecha":"$_id.fecha",
        "R":"$R.Subtotal",
        "C":"$C.Subtotal",
        "D":"$D.Subtotal"}},
    {"$sort":{"categoria":1}}
        ]

   # fecha=[]
    categoria=[]
    R=[]
    D=[]
    C=[]
    SubTC=[]
    Total=[]
    TotalR=[]
    TotalD=[]
    TotalC=[]

    TT=0
    RT=0
    CT=0
    DT=0
    #print 'PORCENTAJES POR CATEGORÍA:'
    for text in tweetsdb.aggregate(pipeline):

        R1=text['R']#Suma de los textos Reentrenados por Categoría
        if R1==[]:
            R1=[0]
        D1=text['D']#Suma de los textos Desechados por Categoría
        if D1==[]:
            D1=[0]
        C1=text['C']#Suma de los textos Correctos por Categoría
        if C1==[]:
            C1=[0]

        TC=R1[0]+D1[0]+C1[0]#Calcula el total de los registros revisados por categoría

        #-----------------Los Porcentajes por categoría-----------------------------------
        if TC!=0:
            RP=round((float(R1[0])/float(TC)),2)*100#Calcula el porcentaje de Reentrenados por Categoría
            DP=round((float(D1[0])/float(TC)),2)*100#Calcula el porcentaje de Desechados por Categoría
            CP=round((float(C1[0])/float(TC)),2)*100#Calcula el porcentaje de Correctos por Categoría
        #print text['categoria'].encode('utf-8'),RP, DP, CP

        #-----------------Los Totales-------------------------------------
        TT=TT+TC#Calcula el total de los textos revisados
        RT=RT+R1[0]#Calcula el total de los textos reentrenados
        CT=CT+C1[0]#Calcula el total de los textos correctos
        DT=DT+D1[0]#Calcula el total de los textos desechados

        #----------------Formando las listas por categoria------------------
        categoria.append(str(text['categoria'].encode('utf-8')))
        #fecha.append(str(text['fecha']))
        D.append(str(DP))
        R.append(RP)
        C.append(CP)
        SubTC.append(TC)
     #-----------------Los Porcentajes Totales-----------------------------------
    if TT!=0:
        RTP=round((float(RT)/float(TT)),2)*100#Calcula el porcentaje de Reentrenados por Categoría
        DTP=round((float(DT)/float(TT)),2)*100#Calcula el porcentaje de Desechados por Categoría
        CTP=round((float(CT)/float(TT)),2)*100#Calcula el porcentaje de Correctos por Categoría
    else:
        RTP=0
        DTP=0
        CTP=0

    #----------------Formando las listas totales------------------
    Total.append(TT)
    TotalR.append(RTP)
    TotalD.append(DTP)
    TotalC.append(CTP)
    dicc={"cat":categoria,"D":D, "R":R, "C":C,"SubTC":SubTC,"Total":Total,"TotalR":TotalR,"TotalD":TotalD,"TotalC":TotalC,"fechaini":fechaini, "fechafin":fechafin}
    if len(dicc)>0:#validación
        return dicc
    else:
        return {}
