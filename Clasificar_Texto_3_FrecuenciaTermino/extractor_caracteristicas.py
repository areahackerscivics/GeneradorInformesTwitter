#!/usr/bin/env python
# encoding: utf-8
"""
Creado el 11 de Abril del 2017
@author: MLMB
"""

from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer, TfidfVectorizer
import numpy as np
import nltk

def mbp_extractor(corpus, ngram_range=(1,1)):
    """a. Este modelo de bolsa de palabras  permite calcular la frecuencia de aparición de cada n-grama dentro un documento
        http://scikit-learn.org/stable/modules/feature_extraction.html

        Arg:
            corpus: Conjunto de documentos
                    (Si hablamos de twitter, sería cada uno de los twits)
            ngram_range:son el número de palabras que podrán integrar los n-gramas considerados.
                        Se ha acotado a unigramas
                        (Si se quieren extendera hasta bigramas, sería ngram_range=(1,2),
                         si es a trigramas, sería ngram_range=(1,3))
            max df : Frecuencia máxima con la que un grama podrá aparecer en la totalidad de los
                    documentos para ser considerado. En nuestro caso, se establece a un 90 %.
            min df : Frecuencia minima con la que un grama podrá aparecer en la totalidad de los
                    documentos para ser considerado. En nuestro caso, se establece a un 10 %.
        Res:
            caracteristica: Transforma los documentos en una matriz de documento.
                            Cada palabra se le asigna un numero,así que se muestra
                            el número al que equivale cada palabra con la frencia de aparicion en el documento
        Nota: el calculo de la frecuencia de palabra se hace por documentos, no por corpus, así que cada documento
              muestra el número de veces que aparece una palabra en dicho documento             
        """
    vectorizar = CountVectorizer(
                                min_df=1,
                                ngram_range=ngram_range
                                )
    caracteristica= vectorizar.fit_transform(corpus)
    return vectorizar, caracteristica

def tfidf_extractor(corpus, ngram_range=(1,1)):
    """#b. Este modelo de bolsa de palabra permite ponderar la relevancia semántica de cada n-grama 
        http://scikit-learn.org/stable/modules/feature_extraction.html

        Arg:
            corpus: Conjunto de documentos
                    (Si hablamos de twitter, sería cada uno de los twits)
            ngram_range:son el número de palabras que podrán integrar los n-gramas considerados.
                        Se ha acotado a unigramas
                        (Si se quieren extendera hasta bigramas, sería ngram_range=(1,2),
                         si es a trigramas, sería ngram_range=(1,3)) 
            max df : Frecuencia máxima con la que un grama podrá aparecer en la totalidad de los
                    documentos para ser considerado. En nuestro caso, se establece a un 90 %.
            min df : Frecuencia minima con la que un grama podrá aparecer en la totalidad de los
                    documentos para ser considerado. En nuestro caso, se establece a un 10 %.
        Res:
            caracteristica: Transforma los documentos en una matriz de documento.
                            Cada n_grama se le asigna un numero que equivale a dicho n_grama
                            seguido del valor con la frencia de aparicion en el documento
        Nota: El formato con que será devuelta la matriz TF-IDF serà una matriz en la que para cada documento se
        establece un valor absoluto sobre el peso de cada n-grama.             
        """
    vectorizar = TfidfVectorizer(
                                min_df=1,
                                ngram_range=ngram_range
                                )
    caracteristica = vectorizar.fit_transform(corpus)
    return vectorizar, caracteristica
    
def tfidf_transformar(mbp_matrix):
    
    transformar = TfidfTransformer(norm='l2',smooth_idf=True,use_idf=True)
    caracteristica = transformar.fit_transform(mbp_matrix)
    return transformar, caracteristica

