#!/usr/bin/env python
# encoding: utf-8

"""
Creado el 3 de Abril del 2017
@author: MLMB
"""
import re
import nltk
import string
from contraerPalabras import CONTRACCION_MAPA
#from hastags import eliminarPalabras
from nltk.stem import SnowballStemmer
from pattern.en import tag
from nltk.corpus import wordnet as wn

stop_words = nltk.corpus.stopwords.words('spanish')#le indicamos el idioma
stemmer = SnowballStemmer('spanish') #le indicamos el idioma


def tokenizar_texto(texto):
    """a.Divide el texto en elemententos denominados tokens

        Arg:
            texto: cada uno de los textos que conforman un corpus
        Res:
            palabras: lista que contiene cada una de los palabras que conforman el texto
        """
    texto=texto.lower()
    palabras = nltk.word_tokenize(texto)
    return palabras

def expandir_contracciones(texto, contraccion_mapping):
    """b.Expande las palabras que tienen contracciones

        Arg:
            texto: cada uno de los textos que conforman un corpus
        Res:
            texto_expandido: texto con las palabras correctas, sin contracciones
        """
    contracciones_patron = re.compile('({})'.format('|'.join(contraccion_mapping.keys())),
                                      flags=re.IGNORECASE|re.DOTALL)
    def expandir_match(contraccion):

        match = contraccion.group(0)
        first_char = match[0]
        contraccion_expandida = contraccion_mapping.get(match)\
                                if contraccion_mapping.get(match)\
                                else contraccion_mapping.get(match.lower())
        contraccion_expandida = first_char+contraccion_expandida[1:]
        return contraccion_expandida

    texto_expandido = contracciones_patron.sub(expandir_match, texto)
    texto_expandido = re.sub("'", "", texto_expandido)
    return texto_expandido

def eliminar_palabras(texto, reemplazo):
    """b.Expande las palabras que tienen contracciones

        Arg:
            texto: cada uno de los textos que conforman un corpus
        Res:
            texto_expandido: texto con las palabras correctas, sin contracciones
        """
    regex = re.compile("(%s)" % "|".join(map(re.escape, reemplazo.keys())))
    return regex.sub(lambda x: str(reemplazo[x.string[x.start() :x.end()]]), texto)


def eliminar_caracteres_especiales(palabras):
    """d.Elimina los caracteres especiales que conforman el texto

        Arg:
            texto: cada uno de los textos que conforman un corpus
        Res:
            texto_filtrado: texto sin caracteres especiales
        """

    pattern = re.compile('[{}]'.format(re.escape(string.punctuation)))
    palabras_filtradas = filter(None, [pattern.sub('', palabra) for palabra in palabras])
    texto_filtrado = ''.join(palabras_filtradas)
    return texto_filtrado


def eliminar_stopwords(texto):
    """e.Elimina las palabras vacias, que no le aportan ningún valor al texto

        Arg:
            texto: cada uno de los textos que conforman un corpus
        Res:
            texto_filtrado: texto sin palabras vacias
        """

    palabras=tokenizar_texto(texto)
    palabras_filtradas = [palabra for palabra in palabras if palabra not in stop_words]
    texto_filtrado = ' '.join(palabras_filtradas)# este join se hace para unir las palabras y dejar el texto separados por un espacio
    return texto_filtrado


def Stemmer(texto):
    """c.Lematiza el texto basado en los tags POS
	Eliminar las variantes/inflexiones de las palabras, almacenando sólo el lema o forma base.

        Arg:
            texto: cada uno de los textos que conforman un corpus
        Res:
            texto_lemmatizado: texto con palabras lematizadas
        """

    palabras = tokenizar_texto(texto)
    texto_stemmer = []
    for palabra in palabras:
        texto_stemmer.append(stemmer.stem(palabra))
    texto_filtrado = ' '.join(texto_stemmer)# este join se hace para unir las palabras y dejar el texto separados por un espacio
    return texto_filtrado

def normalizar_corpus(corpus):
    """f.Corpus normalizado
        En este punto se realiza la normalización del texto, no se incluye los stop words porque
        esa tarea se le deja al vectorizador que está en el modulo de extraccion de caracteristicas

        Arg:
            corpus: todos los textos
        Res:
            corpus_normalizado: texto sin palabras vacias

        Nota: Si se quiere aplicar a otro proyecto, se debe crear otra función donde
        llame todas las funciones que se consideren pertinentes.
        """
    corpus_normalizado = []
    for texto in corpus:
        texto=texto.decode('utf-8')
        texto = expandir_contracciones(texto, CONTRACCION_MAPA)
        #texto = eliminar_palabras(texto, eliminarPalabras)
        texto = eliminar_caracteres_especiales(texto)
        texto = eliminar_stopwords(texto)
        texto = Stemmer(texto)
        corpus_normalizado.append(texto)
    return corpus_normalizado
