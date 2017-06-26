#!/usr/bin/env python
# encoding: utf-8
#from bottle import route, run, template

import sys, os
import numpy as np
import datetime
parent_dir=os.getcwd()
path= os.path.dirname(parent_dir)
sys.path.append(path)

import bottle
from bottle import route, request, response, template

from BLL.revisionBLL import *
from BLL.metricaBLL import *
from BLL.administrarClasificadorBLL import *

from DAO.DBMongoTweet import leer
from DAO.DBMongoEntrenado import guardar_textoreentrenado

'''
try:

    #from Clasificar_Texto_2_Normalizar_texto.normalizacion import normalizar_corpus
    #from procesopickle import leer_Pickle

except ImportError:
    print 'Verificar si en la carpeta DAO están  los archivos DBMongoClasificado,DBMongoEntrenado, DBMongoMetrica'
    print 'Verificar si en la carpeta Clasificar_Texto_2_Normalizar_texto existen el archivo Normalizacion'
    print 'Verificar si en la carpeta existe el archivo procesopickle'
    print 'Verificar si en la carpeta DAO existen los archivos LeerDBTweet y DBMongoClasificado '
'''
@bottle.get("/")
def presentar_bienvenida():
    # check for a cookie, if present, then extract value

#cuando se tenga lo del login se descomentarean estos dos
    #cookie = bottle.request.get_cookie("session")
    #username = sessions.get_username(cookie)  # see if user is logged in
    username="UsuarioPrueba"

    if username is None:
        print "Bienvenido: No se puede identificar al usuario...redireccionando "
        #bottle.redirect("/signup")

    return bottle.template("bienvenida", {'username': username})



@bottle.get('/revision')
def ver_tweets():
    #Al cargar la pagina la primera vez, se cargan los siguietes valores
    catnew="Ninguna"
    ntwets=10
    fechaini= "2017-01-01"
    fechafin= "2017-01-01"
    reentre=0
    #--------------------------------------------------------------------
    #Leer los textos clasificados con los parametros establecidos
    dicc = leer_textoclasificadoTodoBLL(catnew, ntwets,fechaini,fechafin)
    #dicc={"idt":idt,"catold":catold,"tweet":tweet,"catsel":catnew,"ntwets":ntwets,"fechaini":fechaini, "fechafin":fechafin,"reentre":reentre}
    dicc['catsel'] = catnew
    dicc['ntwets'] = ntwets
    dicc['fechaini'] = fechaini
    dicc['fechafin'] = fechafin
    dicc['reentre'] = reentre
    return bottle.template('revision',dict=dicc)

@bottle.post('/revision')
def listar_tweets():
    #Al cargar la página después de la primera vez se cargan los valores de la página
    catnew= bottle.request.forms.get("catlistar")
    ntwets=bottle.request.forms.get("nlistwets")
    fechaini= bottle.request.forms.get("FechaInicio")
    fechafin=bottle.request.forms.get("FechaFin")
    #--------------------------------------------------------------------
    #Leer el nro de textos reentrenados para los parámetros establecidos
    reentre=leer_ClasificadosconEstadoBLL(catnew,fechaini,fechafin)
    #--------------------------------------------------------------------
    #Leer los textos clasificados con los parametros establecidos
    dicc = leer_textoclasificadoTodoBLL(catnew, ntwets,fechaini,fechafin)

    #el resultado se guarda en un diccionario y se envia de vuelta a la página
    dicc['catsel'] = catnew
    dicc['ntwets'] = ntwets
    dicc['fechaini'] = fechaini
    dicc['fechafin'] = fechafin
    dicc['reentre'] = reentre
    return bottle.template('revision',dict=dicc)

@bottle.post('/Actualizar')
def actualizar_tweets():
    contar=bottle.request.forms.get("contar")
    for i in range(int(contar)):
        catnewp="catnew"+str(i)
        catoldn='catold'+str(i)
        idtnl="idt"+str(i)
        texton="texto"+str(i)
        catnew=bottle.request.forms.get(catnewp)
        idt=bottle.request.forms.get(idtnl)
        texto=bottle.request.forms.get(texton)
        catold= bottle.request.forms.get(catoldn)
        estado="R"
        if catnew=="Desechado":
            estado="D"
            actualizar_textoclasificadosBLL(idt,estado)#D=Desechado
        else:
            if catnew=="Correcta":
                catnew=catold
                estado="C"
            #--------------8.Actualizar la BD de clasificado el twit reentrenado--------
            actualizar_textoclasificadosBLL(idt,estado)#R=Reentrenado
            #--------------7.Agregar a la BD de entrenamiento el twit reentrenado--------
            guardar_textoreentrenadoBLL(texto,catnew,idt)

    bottle.redirect('/revision')

@bottle.get('/metrica')
def metrica_revision():
    #Al cargar la página después de la primera vez se cargan los valores de la página
    fechaini= bottle.request.forms.get("FechaInicio")
    fechafin=bottle.request.forms.get("FechaFin")

    #el resultado se guarda en un diccionario y se envia de vuelta a la página
    dicc = leer_CalculoxEstadoBLL(fechaini,fechafin)
    return bottle.template('metrica',dict=dicc)

@bottle.post('/metrica')
def metrica_revisionListar():
    #Al cargar la página después de la primera vez se cargan los valores de la página
    fechaini= bottle.request.forms.get("FechaInicio")
    fechafin=bottle.request.forms.get("FechaFin")

    #el resultado se guarda en un diccionario y se envia de vuelta a la página
    dicc = leer_CalculoxEstadoBLL(fechaini,fechafin)
    return bottle.template('metrica',dict=dicc)

@bottle.get('/clasificar')
def clasificar_inicio():
    fechaini= bottle.request.forms.get("FechaInicio")
    if fechaini==None:
        fechaini= "2017-01-01"
    fechafin=bottle.request.forms.get("FechaFin")
    if fechafin==None:
        fechafin= "2017-05-01"
    print fechaini,fechafin
    dicc={"fechaini":fechaini, "fechafin":fechafin}
    return bottle.template('prueba',dict=dicc)
    #return bottle.template('clasificar',dict=dicc)

'''
============== ESTE FALTA REVISARLO ====================
'''
@bottle.post('/clasificar')
def clasificar_enviar():
    #1--------------------cargar el corpus-------------------
    fechaini= bottle.request.forms.get("FechaInicio")
    if fechaini==None:
        fechaini= "2017-01-01"
    fechafin=bottle.request.forms.get("FechaFin")
    if fechafin==None:
        fechafin= "2017-05-01"
    print fechaini,fechafin
    idt,corpus =leer(fechaini,fechafin)
    print 'clasificar',len(idt)
    if len(idt)>0:
        print 'Se han leido los Registros'
        #2--------------Hacer el tratamiento de las palabras del corpus------------------------
        norm_corpus = normalizar_corpus(corpus)
        print 'Se han normalizado los textos'
        #3--------------Cargando el vector y el clasificador------------------------
        tfidf_vectorizar=leer_Pickle("vectorizar.pickle")
        SGDtfidf=leer_Pickle("SGD.pickle")
        tfidf=tfidf_vectorizar.transform(norm_corpus)
        print 'tfidf hecho'
        clases=SGDtfidf.classes_ #generando las clases
        puntaje=SGDtfidf.decision_function(tfidf) #generando puntajes
        print 'Se ha creado el clasificador'
        #4--------------------Guardar  en db Clasificador-------------------
        #guardar_textoclasificados(corpus,puntaje,clases,idt)
    dicc={"fechaini":fechaini, "fechafin":fechafin}
    return bottle.template('prueba',dict=dicc)
    #return bottle.template('clasificar',dict=dicc)


# ====================  ADMINISTRAR CLASIFICADORES =============================

@bottle.post('/Reentrenar')
def reentrenarClasificador():
    nombre = bottle.request.forms.get('reentrenar_nombre')
    entrena_ini = bottle.request.forms.get('reentrenar_entrena_ini')
    entrena_fin = bottle.request.forms.get('reentrenar_entrena_fin')

    reentrenarClasificadorBLL(nombre, entrena_ini, entrena_fin)

    bottle.redirect("/ListarClasificadores")


@bottle.post('/Borrar')
def borrarClasificador():
    nombre = bottle.request.forms.get('borrar_nombre')

    try:
        eliminarClasificador(nombre)
    except OSError as error:
        bottle.redirect('/error?msj='+ str(error) +'&page=ListarClasificadores')
    except Exception as error:
        bottle.redirect('/error?msj='+ str(error) +'&page=ListarClasificadores')

    bottle.redirect("/ListarClasificadores")


@bottle.post('/Anyadir')
def anyadirClasificador():
    nombre = bottle.request.forms.get('anyadir_nombre')
    entrena_ini = bottle.request.forms.get('anyadir_entrena_ini')
    entrena_fin = bottle.request.forms.get('anyadir_entrena_fin')

    crearClasificador(nombre, entrena_ini, entrena_fin)

    bottle.redirect("/ListarClasificadores")


@bottle.get('/ListarClasificadores')
def listar_clasificadores():

    clasific = getClasificadoresBLL()

    return bottle.template('administrarClasificadores',clasificadores=clasific)


# ==================== FIN ADMINISTRAR CLASIFICADORES ==========================


@route('/error')
def display_error():
    mensajeError = request.query.msj
    pagina = request.query.page
    return template('error', error=mensajeError, pagina=pagina)



@bottle.route('/css/:filename', name='css')
def staticCSS(filename):
    return bottle.static_file(filename, root='./css')

@bottle.route('/js/:filename', name='js')
def staticJS(filename):
    return bottle.static_file(filename, root='./js')


bottle.run(host='localhost', port=8080)
