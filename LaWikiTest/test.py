from pymongo import MongoClient

# Conectarse a un servidor MongoDB (local en este caso)
client = MongoClient("mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/")

# Acceder a una base de datos
db = client["laWikiDB"]

# Acceder a una colección dentro de la base de datos
collection = db["article"]

# Insertar un documento en la colección
nuevo_documento = {
    "nombre": "John Doe",
    "edad": 30,
    "correo": "johndoe@example.com"
}

collection.insert_one(nuevo_documento)

# Consultar el documento recién insertado
documento = collection.find_one({"nombre": "John Doe"})
print(documento)
