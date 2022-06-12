from pymongo import *
import datetime
import re
from bson.objectid import ObjectId

client = MongoClient("mongo", 27017) # Conectar al servicio (docker) "mongo" en su puerto estandar
db = client.SampleCollections
movies = db.Sakila_films
users = client.database.users



def iniciar_prueba_BD():
    if users.count_documents({}) == 0:
        usuario = {"user_id": 1, "name": "Paco", "password": "1234" }
        result = users.insert_one(usuario)



def encontrar_movies(query):
    query = { "Title": { "$regex": query } }
    result = movies.find(query)
    response = []
    for i in result:
        response.append(i)
    return response


def mostrar_movies():
    response = []
    for document in movies.find({}):
        response.append(document)
    return response

def borrar_movie(id):
    if(len(id) < 10):
        movies.delete_one( { "_id": int(id) } )
    else:
        movies.delete_one( { "_id": ObjectId(id) } )


def edit_movie(id, campo, valor):
        if(len(id) < 10):
            doc = movies.find_one_and_update(
            {"_id" : int(id)},
            {"$set": {campo: valor} },upsert=True)
        else:
            doc = movies.find_one_and_update(
            {"_id" : ObjectId(id)},
            {"$set":
            {campo: valor}
            },upsert=True
            )

    
def buscar_por_campo(campo, token):
    response=[]
    for document in movies.find( { campo: token }):
        response.append(document)
    return response

def insert_movie(atributos):
    item = {
        "Title": atributos[0],
        "Length": atributos[1],
        "Category": atributos[2],
        "Rating": atributos[3] 
    }
    id = movies.insert_one(item)
    return id


def adduser(nam, passwd):

    if  users.count_documents({"name": nam}) > 0:
        return False
    else:
        user = {
        "user_id": users.count_documents({})+1, 
        "name": nam,
        "password": passwd
        }
        users.insert_one(user)
        return True


def list_users():
    response = []
    for x in client.database.users.find():
        response.append(x["name"])
    return response
