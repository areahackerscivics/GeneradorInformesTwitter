# Descarga Tweets


## Descripción

Este repositorio contiene el módulo de Descarga de Tweets  del  proyecto "Sistema automático de clasificación de mensajes intercambiados entre la ciudadanía y el Ayuntamiento de València". A partir de los canales de comunicación del Ayuntamiento de València se ha generado un formato que cualquier consistorio puede adaptar a sus necesidades.

El trabajo realizado se concreta en forma de código fuente  que  está diseñada para descargar tweets filtrando por unas  las cuentas que se deseen especificadar.


## Guía de uso

##### Lenguaje de programación
Este módulo fue desearrollado con **Python 2.7.11**

##### Dependencias

* [Pymongo V 3.4.0](https://api.mongodb.com/python/current/ "Pymongo 3.4.0")
* [Tweepy V 3.5.0](http://tweepy.readthedocs.io/en/v3.5.0/ "Tweepy V 3.5.0")

**Nota**: El modulo fue desarrollado usando las librerías que se mencionaron anteriormente, por lo que se recomienda  que para un adecuado funcionamiento se usen  las versiones establecidas.

##### Base de datos

Como sistema de almacenamiento se usa MongoDB que es una base de datos NoSQL que guarda los datos en documentos almacenados en BSON. Para este módulo se usa una colección que tiene la siguiente estructura:

```json
{
    "_id" : ObjectId("58adb1bebc54f400e09531ea"),
    "username" : "pepito",
    "userSeguidores" : 13532,
    "consulta" : "@vivons",
    "idioma" : "es",
    "idt" : "123456789",
    "userid" : 1234,
    "fecha_creacion" : ISODate("2017-02-22T15:40:19.000Z"),
    "dispositivo" : "TweetDeck",
    "tweet" : "Que viva la vida",
    "fechaTweet" : ISODate("2017-02-28T00:00:00.000Z")
}

```
La colección se crea en tiempo de ejecución del código _DescargaTweet.py_ la primera vez que se ejecuta. Si los nombres de los campos no han sufrido ningún cambio, las siguientes veces que se ejecute el código, tan solo insertará registros.

En el archivo **ConexionMongoPublico.py**, se indica el nombre de la colección y la base de datos con la que se trabajó, si desea poner otro nombre a la base de datos o a la colección, es necesario que actualice el archivo. Finalmente debe cambiar  el nombre a  **ConexionMongo.py** .

En el archivo **credencialesTwitterPublico.py**, se  deben indicar las credenciales de tweeter requeridas para acceder a la API de tweeter. Finalmente debe cambiar  el nombre a  **credencialesTwitter.py**.

El Àrea se abstiene de publicar los tweets descargados hasta el momento, debido a la Ley Orgánica de Protección de Datos.

##### Funcionamiento del proyecto

Dentro de la carpeta se encuentra el archivo _DescargaTweet.py_ que permite arrancar el proyecto.

Si se van a cambiar las cuentas de las cuales se desea descargar tweets es en este archivo donde deben hacerlo  _cuentas.csv_.


## Equipo
- Autores principales:  

  - **<a href="https://www.linkedin.com/in/marylin-mattos-a0a59b22/" target="_blank"> Marylin Mattos Barros</a>**, estudiante de Máster Oficial Universitario en Gestión de la Información
  - **<a href="https://github.com/xikoto" target="_blank">José Miguel Benítez</a>**, estudiante de grado en ingeniería Informática.


- Director del proyecto:
  - [Diego Álvarez](https://about.me/diegoalsan) | @diegoalsan


## Contexto del proyecto

El trabajo que contiene este repositorio se ha desarrollado en el [**Àrea Hackers cívics**](http://civichackers.cc). Un espacio de trabajo colaborativo formado por [hackers cívics](http://civichackers.webs.upv.es/conocenos/que-es-una-hacker-civicoa/) que buscamos y creamos soluciones a problemas que impiden que los ciudadanos y ciudadanas podamos influir en los asuntos que nos afectan y, así, construir una sociedad más justa. En definitiva, abordamos aquellos retos que limitan, dificultan o impiden nuestro [**empoderamiento**](http://civichackers.webs.upv.es/conocenos/una-aproximacion-al-concepto-de-empoderamiento/).

El [**Àrea Hackers cívics**](http://civichackers.cc) ha sido impulsada por la [**Cátedra Govern Obert**](http://www.upv.es/contenidos/CATGO/info/). Una iniciativa surgida de la colaboración entre la Concejalía de Transparencia, Gobierno Abierto y Cooperación del Ayuntamiento de València y la [Universitat Politècnica de València](http://www.upv.es).

![ÀHC](http://civichackers.webs.upv.es/wp-content/uploads/2017/02/Logo_CGO_web.png) ![ÀHC](http://civichackers.webs.upv.es/wp-content/uploads/2017/02/logo_AHC_web.png)



## Términos de uso

![](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)El contenido de este repositorio está sujeto a la licencia [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/).
