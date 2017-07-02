#!/usr/bin/env python
# encoding: utf-8
import sys, os
import numpy as np
import datetime
parent_dir=os.getcwd()
path= os.path.dirname(parent_dir)
sys.path.append(path)

from DAO.DBMongoMetrica import leer_CalculoxEstado


def leer_CalculoxEstadoBLL(fechaini,fechafin):

    if fechaini==None:
        fechaini= "2017-01-01"
    if fechafin==None:
        fechafin= "2017-05-01"

    dicc =leer_CalculoxEstado(fechaini,fechafin)#DBMongoMetrica

    if len(dicc)>0:#validación
        return dicc
    else:
        return {}
