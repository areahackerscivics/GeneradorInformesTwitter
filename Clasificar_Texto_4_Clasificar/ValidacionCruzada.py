#!/usr/bin/env python
# encoding: utf-8

from sklearn.model_selection import train_test_split 
def validacion_cruzada(corpus, categorias):
    """Divide el corpus para entrenar y probar en la proporción que
        se indica con los parámetros train_size y test_size

        Args:
            corpus(list): Se espera una coleccion de documentos que contienen los textos.
            cat (list): Se espera una lista de N categorias.
        Res:
            e_X: lista de documentos (tweets)que serán usados para el entrenamiento
            p_X: lista de documentos (tweets)que serán usados para pruebas
            e_Y: lista de categorías que serán usadas para el entrenamiento
            p_Y: lista de categorías que serán usadas para pruebas
        """
    e_X, p_X, e_Y, p_Y = train_test_split(corpus, categorias,
                                          train_size=0.75, test_size=0.25)
    return e_X, p_X, e_Y, p_Y
