from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask import Flask,jsonify,request 
from bson.objectid import ObjectId
from flask_cors import CORS
import re
from urllib.parse import unquote






uri = "mongodb+srv://elliot:1234@cluster0.eeen5dm.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db= client.Thea
products=db.products

def getPage(page):
    output=[]
    cursor = db.products.find().skip(40*page).limit(40)
    for document in cursor:
         document['_id'] = str(document['_id'])
         output.append(document)
    return  output


## start server

app = Flask(__name__)
CORS(app)

@app.route("/products/<string:page>", methods=["GET"])
def getProducts(page):
    page=page.split("=")[1]
    page=int(page)
    return  jsonify({"products":getPage(page)})

@app.route("/product/<string:id>", methods=["GET"])
def getProduct(id):
    # Convierte el ID en un objeto ObjectId
    product_id = ObjectId(id)
    
    # Realiza la búsqueda del producto utilizando el ID
    product = db.products.find_one({"_id": product_id})
    product["_id"] = str(product["_id"])
  
    return product
  

    
@app.route("/product", methods=["POST"])
def addProduct():
    new={
         "name":request.json["name"],
            "price":request.json["price"],
               "colors":request.json["colors"],
                  "relevance":request.json["relevance"],
                     "imgs":request.json["imgs"],
                        "gender":request.json["gender"],
                            "sizes":request.json["sizes"],
                                "tags":request.json["tags"],
                                "brand":request.json["brand"]
    }
    products.insert_one(new)
    print(new)
    return "perfecto"



### categories
@app.route("/products/categories/<string:category>/<string:page>", methods=["GET"])
def getCategory(page,category):
    page=page.split("=")[1]
    page=int(page)
    output=[]
    cursor = db.products.find({"tags":category}).skip(40*page).limit(40)
    for document in cursor:
         document['_id'] = str(document['_id'])
         output.append(document)
    return output

### genere
@app.route("/products/genere/<string:genere>/<string:page>", methods=["GET"])
def getGenere(page,genere):
    page=page.split("=")[1]
    page=int(page)
    output=[]
    cursor = db.products.find({"genere": genere }).skip(40*page).limit(40)
    for document in cursor:
         document['_id'] = str(document['_id'])
         output.append(document)
    return output

## seach
@app.route("/products/search", methods=["GET"])
def find():
    query = request.args.get('query')
    page = request.args.get('page')
    limit = request.args.get('limit')
    limit= int(limit)
    page=int(page)
    output=[]

    query=unquote(query)
    print(query)
    query = {"$regex": query, "$options": "i"}
  
    query = {
    '$or': [
        {'name': query},
        {'tags': query}
    ]}
    print(query)
    cursor = db.products.find(query).skip(limit*page).limit(limit)
    for document in cursor:
         document['_id'] = str(document['_id'])
         output.append(document)
         

    return output



@app.route("/discount/<string:code>", methods=["GET"])
def discount(code):
    value = db.code.find_one({"code": code})
    if value:
        return {"code": value["code"], "discount": value["discount"]}
    else:
        return {"error": "Code not found"}
    


if __name__ == '__main__':
   app.run( port=8080) 


