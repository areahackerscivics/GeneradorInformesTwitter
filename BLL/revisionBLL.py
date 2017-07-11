    #!/usr/bin/env python
# encoding: utf-8
import sys, os
import numpy as np
import datetime
parent_dir=os.getcwd()
path= os.path.dirname(parent_dir)
sys.path.append(path)

from DAO.revisionDAO import *


def leer_textoclasificadoTodoBLL(catnew, ntwets,fechaini,fechafin):#
    reentre=getreentre(catnew,fechaini,fechafin)#DBMongoClasificado
    idt,catold,tweet,fechaTweet = leer_textoclasificadoTodo(catnew, ntwets,fechaini,fechafin)#DBMongoClasificado
    if idt!=-1:#validación de vacion
        dicc={
            "idt":idt,"catold":catold,"tweet":tweet,"fechaTweet":fechaTweet,
              "reentre":reentre,"catsel":catnew, "ntwets":ntwets,"fechaini":fechaini,"fechafin":fechafin
            }
        return dicc
    else:
        dicc={"idt":[],"catold":[],"tweet":[],"catsel":catnew,"ntwets":ntwets,
        "fechaini":fechaini, "fechafin":fechafin,"reentre":reentre}
        return dicc


def leer_ClasificadosconEstadoBLL(catnew,fechaini,fechafin):
    return leer_ClasificadosconEstado(catnew,fechaini,fechafin)


def actualizar_textoclasificadosBLL(idt,estado):
    return actualizar_textoclasificados(idt,estado)

def guardar_textoreentrenadoBLL(texto,catnew,idt,fechat):
    return guardar_textoreentrenado(texto,catnew,idt,fechat)
