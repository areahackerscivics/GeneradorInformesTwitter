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

    cat,D,R,C,SubTC,Total,TotalR,TotalD,TotalC =leer_CalculoxEstado(fechaini,fechafin)

    dicc={"cat":cat,"D":D, "R":R, "C":C,"SubTC":SubTC,"Total":Total,"TotalR":TotalR,"TotalD":TotalD,"TotalC":TotalC,"fechaini":fechaini, "fechafin":fechafin}

    return dicc
