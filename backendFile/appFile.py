from flask import Flask
from flask_cors import CORS
import json
from flask import jsonify
from src.dbclientes import dbClientes
from pymongo import MongoClient

from flask_caching import Cache

config = {
    "DEBUG": True,          
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 300
}
app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)

CORS(app)

conn = MongoClient('mongodb', 27017)
# create db
db = conn.baseDeDatos
# create collection Clientes

client = dbClientes(db.Clientes)

@app.route('/')
@cache.cached(timeout=50)
def hello_world():
    return jsonify('Hello, World !'), 200

# devuelve la cesta de un cliente dado su id
@app.route('/files/<string:correo_id>', methods=['GET','POST'])
@cache.cached(timeout=50)
def cesta(correo_id):
    return jsonify(client.getCesta(correo_id)), 200

# recorre el directorio y devuelve lista d los clientes
@app.route('/clientes', methods = ['GET','POST'])
@cache.cached(timeout=50)
def clientes():
    return  jsonify(client.getClientes()), 200

@app.route('/todo', methods = ['GET','POST'])
@cache.cached(timeout=50)
def todo():
    return  jsonify(client.getAll()), 200

# new client
@app.route('/newclient/<string:correo_id>', methods = ['GET','POST'])
def newclient(correo_id):
    return  jsonify(client.insertClient(correo_id)), 200    


# new cesta 
@app.route('/file/add/<string:correo_id>/<string:cesta_id>', methods = ['GET','POST'])
def newcesta(correo_id,cesta_id):
    return jsonify(client.insertCesta(correo_id,cesta_id)), 200

@app.route('/delete/<string:correo_id>', methods = ['GET','POST'])
def deleteClient(correo_id):
    return  jsonify(client.deleteClient(correo_id)), 200 

if __name__ == '__main__':
    app.run()
