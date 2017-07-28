#!/usr/bin/env python
# encoding: utf-8
#from bottle import route, run, template

import sys, os, io
import numpy as np
import datetime
import time
parent_dir=os.getcwd()
path= os.path.dirname(parent_dir)
sys.path.append(path)

import bottle
from bottle import route, request, response, template

from BLL.revisionBLL import *
from BLL.metricaBLL import *
from BLL.clasificacionBLL import *
from BLL.administrarClasificadorBLL import *

errorP="Ha ocurrido un error a nivel de Base de Datos"
errorL="No hay tweet que clasificar, pulse OK para regresar"
today=datetime.datetime.now()

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


# ====================  REVISION MANUAL =============================
@bottle.get('/revision')
def ver_tweets():

    dicc={"idt":[],"catold":[],"tweet":[],"catsel":"Ninguna","ntwets":10,"fechaini":"2017-01-01", "fechafin":today,"reentre":0}
    return bottle.template('revision',dict=dicc)

@bottle.post('/revision')
def listar_tweets():
    #Al cargar la página después de la primera vez se cargan los valores de la página
    catnew= bottle.request.forms.get("catlistar")
    ntwets=bottle.request.forms.get("nlistwets")
    fechaini= bottle.request.forms.get("FechaInicio")#Fecha en la que se hizo la clasificación
    fechafin=bottle.request.forms.get("FechaFin")#Fecha en la que se hizo la clasificación
    dicc=leer_textoclasificadoTodoBLL(catnew, ntwets,fechaini,fechafin)
    return bottle.template('revision',dict=dicc)
    # try:
    #     dicc=leer_textoclasificadoTodoBLL(catnew, ntwets,fechaini,fechafin)
    #     #la validación cuando la consulta no devuelve nada está en la BLL por lógica del negocio
    #     return bottle.template('revision',dict=dicc)
    # except OSError as error:
    #     bottle.redirect('/error?msj='+ str(errorP) +'&page=revision')
    # except Exception as error:
    #     bottle.redirect('/error?msj='+ str(errorP) +'&page=revision')

@bottle.post('/actualizar')
def actualizar_tweets():
    contar=bottle.request.forms.get("contar")
    try:
        if contar=="0":
            return 5/0 #forzar la excepcion
    except ZeroDivisionError as err:
        bottle.redirect('/error?msj='+ str(errorL) +'&page=revision')
    #try:

    for i in range(int(contar)):
        catnewp="catnew"+str(i)
        catoldn='catold'+str(i)
        idtnl="idt"+str(i)
        fechatn="fechat"+str(i)
        texton="texto"+str(i)
        catnew=bottle.request.forms.get(catnewp)
        idt=bottle.request.forms.get(idtnl)
        texto=bottle.request.forms.get(texton)
        catold= bottle.request.forms.get(catoldn)
        fechat= bottle.request.forms.get(fechatn)
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
            guardar_textoreentrenadoBLL(texto,catnew,idt,fechat)
    bottle.redirect('/revision')
    # except OSError as error:
    #     bottle.redirect('/error?msj='+ str(errorP) +'&page=revision')
    # except Exception as error:
    #     bottle.redirect('/error?msj='+ str(errorP) +'&page=revision')

# ==================== FIN REVISION MANUAL ==========================
# ====================  ESTADISTICA REVISION MANUAL =============================
@bottle.get('/metrica')
def metrica_revision():
    #Al cargar la página después de la primera vez se cargan los valores de la página
    fechaini= bottle.request.forms.get("FechaInicio") #Fecha en la que se hizo la clasificación
    fechafin=bottle.request.forms.get("FechaFin") #Fecha en la que se hizo la clasificación
    try:
        #el resultado se guarda en un diccionario y se envia de vuelta a la página
        dicc = leer_CalculoxEstadoBLL(fechaini,fechafin)
        return bottle.template('metrica',dict=dicc)
    except OSError as error:
        bottle.redirect('/error?msj='+ str(errorP) +'&page=metrica')
    except Exception as error:
        bottle.redirect('/error?msj='+ str(errorP) +'&page=metrica')

@bottle.post('/metrica')
def metrica_revisionListar():
    #Al cargar la página después de la primera vez se cargan los valores de la página
    fechaini= bottle.request.forms.get("FechaInicio")
    fechafin=bottle.request.forms.get("FechaFin")

    try:
        #el resultado se guarda en un diccionario y se envia de vuelta a la página
        dicc = leer_CalculoxEstadoBLL(fechaini,fechafin)
        return bottle.template('metrica',dict=dicc)
    except OSError as error:
        bottle.redirect('/error?msj='+ str(errorP) +'&page=metrica')
    except Exception as error:
        bottle.redirect('/error?msj='+ str(errorP) +'&page=metrica')

# ==================== FIN ESTADISTICA REVISION MANUAL ==========================

# ====================  CLASIFICACIÓN =============================
@bottle.get('/clasificar')
def clasificar_inicio():
    # try:
    dicc=generar_tabla()
    return bottle.template('clasificar',dict=dicc)
    # except OSError as error:
    #     bottle.redirect('/error?msj='+ str(errorP) +'&page=clasificar')
    # except Exception as error:
    #     bottle.redirect('/error?msj='+ str(errorP) +'&page=clasificar')


@bottle.post('/clasificar')
def clasificar_enviar():
    #1--------------------cargar el corpus-------------------
    #fechaini= bottle.request.forms.get("FechaInicio")#Fecha en la que se hizo la descarga del tweet
    #fechafin=bottle.request.forms.get("FechaFin") #Fecha en la que se hizo la descarga del tweet
    contar=bottle.request.forms.get("contar")
    for i in range(int(contar)):
            fechatn="fechat"+str(i)
            fechaTw=bottle.request.forms.get(fechatn)
            if fechaTw!=None:
                print fechaTw
                generar_clasificacionBLL(fechaTw)

    # try:
        #generar_clasificacionBLL(fechaini,fechafin)#se hace el insert
    dicc=generar_tabla() #se muestra nuevamente la grilla con los cambios
    return bottle.template('clasificar',dict=dicc)
    # except OSError as error:
    #     bottle.redirect('/error?msj='+ str(errorP) +'&page=clasificar')
    # except Exception as error:
    #     bottle.redirect('/error?msj='+ str(errorP) +'&page=clasificar')

# ====================  ADMINISTRAR CLASIFICADORES =============================

@bottle.post('/Editar')
def editarClasificador():
    nombreOri = bottle.request.forms.get('editar_nombre')
    nombreNuev = bottle.request.forms.get('editar_nombre_nuevo')

    editarClasificadorBLL(nombreOri, nombreNuev)

    bottle.redirect("/ListarClasificadores")

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
