#!/usr/bin/env python
# encoding: utf-8
import sys, os

try:
    import cPickle as pickle
except ImportError:
    print 'Verifique si tiene instalada la librería cPickle'

def guardar_Pickle(dafile, variable):
    filePath = os.path.abspath('output')
    datafile = os.path.join(filePath,dafile)
    fichero = file(datafile, "w")
    pickle.dump(variable, fichero)
    fichero.close()
    print 'creado ',dafile

def leer_Pickle(parametro):
    datafile = os.path.abspath(parametro)
    fichero = file(datafile)
    variable = pickle.load(fichero)
    return variable
