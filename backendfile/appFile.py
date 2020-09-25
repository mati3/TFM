from flask import Flask, request
from flask_cors import CORS
import json
from flask import jsonify
from src.dbclientes import dbClientes
from pymongo import MongoClient
import os
import shutil
from werkzeug.utils import secure_filename
from flask_caching import Cache

from src.lucene import Lucene
lc = Lucene()

config = {
    "DEBUG": True,          
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 300
}
UPLOAD_FOLDER = './clients' 
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

# return 'hello world', test metod
@app.route('/')
@cache.cached(timeout=50)
def hello_world():
    return jsonify('Hello, World !'), 200

# return all of mongodb, test metod
@app.route('/todo', methods = ['GET','POST'])
@cache.cached(timeout=50)
def todo():
    return  jsonify(client.getAll()), 200

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

# devuelve los archivos Indexados de un cliente dado su id
@app.route('/filesindex/<string:correo_id>', methods=['GET'])
@cache.cached(timeout=50)
def filesindex(correo_id):
    myfolder = app.config['UPLOAD_FOLDER']+'/'+correo_id
    createDirectory(myfolder)
    filesFVS = os.listdir(app.config['UPLOAD_FOLDER']+'/'+correo_id+'/filesFVS/index')
    if "lucene" in filesFVS: filesFVS.remove("lucene") 
    filesFDS = os.listdir(app.config['UPLOAD_FOLDER']+'/'+correo_id+'/filesFDS/index')
    if "lucene" in filesFDS: filesFDS.remove("lucene") 
    filesTIS = os.listdir(app.config['UPLOAD_FOLDER']+'/'+correo_id+'/filesTIS/index')
    if "lucene" in filesTIS: filesTIS.remove("lucene") 
    files = {'filesFVS':filesFVS, 'filesFDS': filesFDS, 'filesTIS': filesTIS}
    return jsonify(files), 200

# devuelve los archivos de un cliente dado su id
@app.route('/files/<string:correo_id>', methods=['GET'])
@cache.cached(timeout=50)
def files(correo_id):
    files = client.getFiles(correo_id)
    for i in files:
        filesFVS = i['filesFVS']
        filesFDS = i['filesFDS']
        filesTIS = i['filesTIS'] 
        files = {'filesFVS':filesFVS, 'filesFDS': filesFDS, 'filesTIS': filesTIS}
        return jsonify(files), 200
    return jsonify("error"), 500
    
@app.route('/removefile/<string:correo_id>/<string:typefile>', methods = ['DELETE'])
def removefile(correo_id,typefile):
    shutil.rmtree(app.config['UPLOAD_FOLDER']+'/'+correo_id+'/'+ typefile)
    os.mkdir(app.config['UPLOAD_FOLDER']+'/'+correo_id+'/'+typefile)
    os.mkdir(app.config['UPLOAD_FOLDER']+'/'+correo_id+'/'+typefile+'/index')
    files = client.deleteFiles(correo_id,typefile)
    return jsonify('ok'), 200

# insert file in folder clients
@app.route('/upload/<string:correo_id>/<string:typefile>', methods = ['POST'])
def upload(correo_id, typefile):
    response = ''   
    # check if the post request has the file part
    if ('filepositive' not in request.files) or ('filenegative' not in request.files):
        response='no file positive or negative in request', 500
        return jsonify(response)
    filepos = request.files['filepositive']
    fileneg = request.files['filenegative']
    if (filepos.filename == '') or (fileneg.filename == ''):
        response ='no selected file positive or negative'
        return jsonify(response), 500
    if (filepos and allowed_file(filepos.filename)) or (fileneg and allowed_file(fileneg.filename)):
        response = 'files upload ok'
        filenamepos = secure_filename(filepos.filename)
        filenameneg = secure_filename(fileneg.filename)
        # comprobar si el directorio para el usuario actual existe
        myfolder = app.config['UPLOAD_FOLDER']+'/'+correo_id
        # si no existe lo creamos
        createDirectory(myfolder)
        # guardar archivo en directorio para el usuario actual
        filepos.save(os.path.join(myfolder+'/'+typefile, filenamepos))
        fileneg.save(os.path.join(myfolder+'/'+typefile, filenameneg))
        # concatenamos los archivos y lo indexamos
        concat_file(filenamepos, filenameneg, myfolder+'/'+typefile)
        client.insertFiles(correo_id,typefile,filenamepos, filenameneg)
        
        return jsonify(response), 200
    response = 'response post ok'
    return jsonify(response), 200

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def concat_file(file1, file2, myfolder):
    count = file1.find(".txt")
    filename = file1[:count]+file2
    f1 = open(myfolder+'/'+file1, "r").read()
    f2 = open(myfolder+'/'+file2, "r").read()
    filepath = myfolder+'/index/'
    try: 
        os.stat(filepath)
    except:
        os.mkdir(filepath)
    newfile = open(filepath+filename, "a")
    newfile.write(f1 + f2)
    newfile.close()
    lc.indexar(filepath,filename)

def createDirectory(myfolder):
    try: 
        os.stat(myfolder)
    except:
        os.mkdir(myfolder)
        os.mkdir(myfolder+'/filesFVS')
        os.mkdir(myfolder+'/filesFDS')
        os.mkdir(myfolder+'/filesTIS')
        os.mkdir(myfolder+'/filesFVS/index')
        os.mkdir(myfolder+'/filesFDS/index')
        os.mkdir(myfolder+'/filesTIS/index')
        os.mkdir(myfolder+'/filesFVS/index/lucene')
        os.mkdir(myfolder+'/filesFDS/index/lucene')
        os.mkdir(myfolder+'/filesTIS/index/lucene')

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:4201')
    response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With,content-type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

if __name__ == '__main__':
    app.run()
