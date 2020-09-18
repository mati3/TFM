from flask import Flask, request, Response
from flask_cors import CORS, cross_origin
import json
from flask import jsonify
from src.dbclientes import dbClientes
from pymongo import MongoClient
import os
from werkzeug.utils import secure_filename
from flask_caching import Cache

#from src.lucene import Lucene
# lc = Lucene

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

conn = MongoClient('mongodb', 27017)
# create db
db = conn.baseDeDatos
# create collection Clientes
client = dbClientes(db.Clientes)
print(client)

@app.route('/')
@cache.cached(timeout=50)
def hello_world():
    return jsonify('Hello, World !'), 200

# devuelve los archivos de un cliente dado su id
@app.route('/files/<string:correo_id>', methods=['GET','POST'])
@cache.cached(timeout=50)
def cesta(correo_id):
    return jsonify(client.getCesta(correo_id)), 200

@app.route('/todo', methods = ['GET','POST'])
@cache.cached(timeout=50)
def todo():
    return  jsonify(client.getAll()), 200

# new cesta 
@app.route('/file/add/<string:correo_id>/<string:cesta_id>', methods = ['GET','POST'])
def newcesta(correo_id,cesta_id):
    return jsonify(client.insertCesta(correo_id,cesta_id)), 200

#############

# recorre el directorio y devuelve lista d los clientes
@app.route('/clientes', methods = ['GET','POST'])
@cache.cached(timeout=50)
def clientes():
    return  jsonify(client.getClientes()), 200

# new client
@app.route('/newclient/<string:correo_id>', methods = ['GET','POST'])
def newclient(correo_id):
    return  jsonify(client.insertClient(correo_id)), 200    

# remove client
@app.route('/delete/<string:correo_id>', methods = ['DELETE'])
def deleteClient(correo_id):
    return  jsonify(client.deleteClient(correo_id)), 200 
    
@app.route('/removefile/<string:correo_id>', methods = ['POST'])
def removefile(correo_id):
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
        os.remove(app.config['UPLOAD_FOLDER']+'/'+correo_id+'/'+ filename)
        return jsonify(response), 200
    response = 'response post ok'
    return jsonify(response), 200

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def concat_file(file1, file2, myfolder):
    count = file1.find("included")
    newstr = file1[:count]
    f1 = open(myfolder+'/'+file1, "r").read()
    f2 = open(myfolder+'/'+file2, "r").read()
    indexfolder = myfolder+'/indexar/'
    try: 
        os.stat(indexfolder)
    except:
        os.mkdir(indexfolder)
    newfile = open(indexfolder+newstr+".txt", "a")
    newfile.write(f1 + f2)
    # aqui directamente llamo a indexar ???

def checkpair(filename, myfolder):
    if "included" in filename:
        nameaux = filename.replace("included", "negative") 
        if os.listdir(myfolder).count(nameaux):
            concat_file(filename, nameaux, myfolder)
    elif "negative" in filename:
        nameaux = filename.replace("negative", "included") 
        if os.listdir(myfolder).count(nameaux):
            concat_file(nameaux, filename, myfolder)

# insert file in folder uploads
@app.route('/upload/<string:correo_id>/<string:typefile>', methods = ['POST'])
def upload(correo_id, typefile):
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
        # comprobar si el directorio para el usuario actual existe
        myfolder = app.config['UPLOAD_FOLDER']+'/'+correo_id
        try: 
            os.stat(myfolder)
        except:
            os.mkdir(myfolder)
        # guardar archivo en directorio para el usuario actual
        file.save(os.path.join(myfolder, filename))
        # chequeo si el par del archivo existe, si es asi se concatenaran para indexar
        checkpair(filename, myfolder)
        
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
