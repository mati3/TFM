from flask import Flask, request, Response
from flask_cors import CORS, cross_origin
import json
from flask import jsonify
from src.dbclientes import dbClientes
from pymongo import MongoClient
import os
from werkzeug.utils import secure_filename
from flask_caching import Cache

config = {
    "DEBUG": True,          
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 300
}
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['txt'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_mapping(config)
cache = Cache(app)

CORS(app)
#cors = CORS(app, resources={r"/*": {"origins": "http://localhost:4201"}}, supports_credentials = True )

conn = MongoClient('mongodb', 27017)
# create db
db = conn.baseDeDatos
# create collection Clientes

client = dbClientes(db.Clientes)

@app.route('/')
@cache.cached(timeout=50)
def hello_world():
    return jsonify('Hello, World !'), 200

# devuelve los archivos de un cliente dado su id
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

@app.route('/removefile', methods = ['POST'])
def removefile():
    print(request.files)
    print(request.files.get('file'))
    response = ''   
    # check if the post request has the file part
    if 'file' not in request.files:
        response='no file in request', 500
        return jsonify(response)
    file = request.files['file']
    if file.filename == '':
        response ='no selected file'
        return jsonify(response), 500
    if file and allowed_file(file.filename):
        response = 'file remove ok'
        filename = secure_filename(file.filename)
        os.remove(app.config['UPLOAD_FOLDER']+'/'+ filename)
        return jsonify(response), 200
    response = 'response post ok'
    return jsonify(response), 200

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload/<string:correo_id>', methods = ['POST'])
def upload(correo_id):
    print(request.files)
    print(request.files.get('file'))
    response = ''   
    # check if the post request has the file part
    if 'file' not in request.files:
        response='no file in request', 500
        return jsonify(response)
    file = request.files['file']
    if file.filename == '':
        response ='no selected file'
        return jsonify(response), 500
    if file and allowed_file(file.filename):
        response = 'file upload ok'
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(client.insertCesta(correo_id,filename))
        return jsonify(response), 200
    response = 'response post ok'
    return jsonify(response), 200

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:4201')
    response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With,content-type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

if __name__ == '__main__':
    app.run()
