import sys, os
import numpy as np
import datetime
parent_dir=os.getcwd()
path= os.path.dirname(parent_dir)
sys.path.append(path)

from DAO.DBMongoClasificado import *

def leer_textoclasificadoTodoBLL(catnew, ntwets,fechaini,fechafin):
    idt,catold,tweet = leer_textoclasificadoTodo(catnew, ntwets,fechaini,fechafin)
    dicc={"idt":idt,"catold":catold,"tweet":tweet}
    return dicc


def leer_ClasificadosconEstadoBLL(catnew,fechaini,fechafin):
    return leer_ClasificadosconEstado(catnew,fechaini,fechafin)


def actualizar_textoclasificadosBLL(idt,estado):
    return actualizar_textoclasificados(idt,estado)

def guardar_textoreentrenadoBLL(texto,catnew,idt):
    return guardar_textoreentrenado(texto,catnew,idt)
