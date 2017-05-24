#!/usr/bin/env python
# encoding: utf-8

"""
<<<a.Código de preparación de los datos>>>
@author: Marylin Mattos
"""
import os, sys, io
parent_dir=os.getcwd()
path= os.path.dirname(parent_dir)
path2=path+"\DAO\input\\"


def leer_archivo(dfile):
    datafile = os.path.join(path2,dfile)
    """lee un archivo csv.
             Args:
            texto (list): Se espera una lista de N textos que estan en la 3ra posicion del archivo csv.
            cat (list): Se espera una lista de N categorias que estan en la 4ta posicion del archivo csv.
        Nota:
            
    """
    texto = []
    cat = []
    with open(datafile, "r") as f:
        header = f.readline().split(";")
        for line in f:
            fields = line.split(";")        
            texto.append(fields[2])
            cat.append(fields[1])
        return  texto,cat
		
