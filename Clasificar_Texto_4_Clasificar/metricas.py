#!/usr/bin/env python
# encoding: utf-8
"""
<<<e.Código de evaluación del modelo>>
En esta parte se hace la evaluación del modelo
"""
import numpy as np
from sklearn import metrics


def evaluar_modelo(y_true,y_pred):
    ex = np.round(metrics.accuracy_score(y_true,y_pred),2)
    pr = np.round(metrics.precision_score(y_true,y_pred,average='weighted'),2)
    re = np.round(metrics.recall_score(y_true,y_pred,average='weighted'),2)
    fm = np.round(metrics.f1_score(y_true,y_pred,average='weighted'),2)

    return ex, pr, re, fm

def evaluar_clases(y_true,y_pred):
    
    exc = np.round(metrics.accuracy_score(y_true,y_pred),2)
    prc = np.round(metrics.precision_score(y_true,y_pred, average=None),2)
    rec = np.round(metrics.recall_score(y_true,y_pred, average=None),2)
    fmc = np.round(metrics.f1_score(y_true,y_pred, average=None),2)

    print 'Accuracy:', exc
    print 'Precision:', prc
    print 'Recall:', rec
    print 'F1 Score:', fmc

   
