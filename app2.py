from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask import Flask,jsonify,request 
from bson.objectid import ObjectId
from flask_cors import CORS

import receipt
import json
from flask_cors import CORS
uri = "mongodb+srv://elliot:1234@cluster0.eeen5dm.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db= client.Thea
products=db.products

app = Flask(__name__)
CORS(app, resources={r"/post": {"origins": "http://localhost:4200"}})
@app.route("/wvzIFw3tb60eNBks8Fymxnt5Ac", methods=["POST"])
def buy():
    data=request.json
    data_dict = json.loads(data[0])
    productos=[]
# Acceder a los elementos del diccionario
    nombre = data_dict["nombre"]
    numero = data_dict["numero"]
    direccion = data_dict["direccion"]
    theaid=  data[1]
    for i in theaid:
        one=db.products.find_one({"_id": ObjectId(
            i["theaId"])})
        one["quantity"]=i["quantity"]
        productos.append(one)
        if db.code.find_one({"code":data[2]}) is None:
            code={"code":"nonos", "discount":"0"}
        else:
          code=db.code.find_one({"code":data[2]})
       
   
    receipt.generateReceipt(nombre, numero, direccion, "pay", productos,code["discount"])
    return "ok"

if __name__ == '__main__':
   app.run(debug=True ,port=4100) 


