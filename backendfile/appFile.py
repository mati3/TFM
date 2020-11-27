#   Trabajo Fin de Máster
#   Máster en Ingeniería Informática
#
#   2020 - Copyright (c) - GNU v3.0
#
#  Matilde Cabrera <mati331@correo.ugr.es>

from flask import Flask, request
from flask_cors import CORS
import json
from flask import jsonify
from src.dbclientes import dbClientes
from pymongo import MongoClient
import os
from time import time
import shutil
from werkzeug.utils import secure_filename
from flask_caching import Cache

#from src.lucene import Lucene
from src.recuperacionInformacion import Lucene
from src.filtros import Filtros
from src.rendimiento import Rendimiento

lc = Lucene()
ft = Filtros()
md = Rendimiento()

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

Filters = {
    'InfGain', 
    'CrossEntropy', 
    'MutualInfo', 
    'Freq', 
    'OddsRatio', 
    'NormalSeparation', 
    'Diferencia'
    }

Typefiles = {
    'filesFDS', 
    'filesFVS', 
    'filesTIS'}

# return 'hello world', test metod
#@app.route('/')
#@cache.cached(timeout=50)
#def hello_world():
#    return jsonify('Hello, World !'), 200

# return all of mongodb, test metod
#@app.route('/todo', methods = ['GET','POST'])
#@cache.cached(timeout=50)
#def todo():
#    return  jsonify(client.getAll()), 200

# new client
@app.route('/newclient/<string:correo_id>', methods = ['GET','POST'])
def newclient(correo_id):
    myfolder = app.config['UPLOAD_FOLDER']+'/'+ correo_id
    # si no existe lo creamos
    createDirectory(myfolder)
    return  jsonify(client.insertClient(correo_id)), 200    

# remove client
@app.route('/delete/<string:correo_id>', methods = ['DELETE'])
def deleteClient(correo_id):
    return  jsonify(client.deleteClient(correo_id)), 200 

# devuelve los archivos de un cliente dado su id
@app.route('/files/<string:correo_id>', methods=['GET'])
def filesClient(correo_id):
    files = client.getFiles(correo_id)
    #print("files")
    #print(files)
    return jsonify(files), 200
    
@app.route('/removefile/<string:correo_id>/<string:typefile>', methods = ['DELETE'])
def removefile(correo_id,typefile):
    if (client.getCliente(correo_id) is False):
        return "Usuario NO existe, operación no valida"
    shutil.rmtree(app.config['UPLOAD_FOLDER']+'/'+correo_id+'/'+ typefile)
    os.mkdir(app.config['UPLOAD_FOLDER']+'/'+correo_id+'/'+typefile)
    files = client.deleteFiles(correo_id,typefile)
    if files:
        salida = "archivos eliminados", 200
    else:
        salida = "error, los archivos no han sido eliminados", 400
    return jsonify(salida)

# insert file in folder clients
@app.route('/upload', methods = ['POST'])
def upload():
    response = '' 

    if 'typefile' not in request.form:
        return 'No has seleccionado el tipo de archivo', 400
    typefile = request.form['typefile']
    if typefile not in Typefiles:
        return "No existe el tipo de archivo seleccionado ",400

    if 'email' not in request.form:
        return 'Es necesario que se identifique', 400
    correo_id = request.form['email']
    # si email no coincide con ningun usuario...
    if not client.getCliente(correo_id):
        return "Usuario no existente", 400

    # check if the post request has the file part
    if ('filepositive' not in request.files) or ('filenegative' not in request.files):
        response='no file positive or negative in request', 500
        return jsonify(response), 500

    filepos = request.files['filepositive']
    fileneg = request.files['filenegative']

    if (filepos.filename == '') or (fileneg.filename == ''):
        response ='no selected file positive or negative'
        return jsonify(response), 500

    if (filepos and allowed_file(filepos.filename)) or (fileneg and allowed_file(fileneg.filename)):
        filenamepos = secure_filename(filepos.filename)
        filenameneg = secure_filename(fileneg.filename)
        
        # Guardo nombres en mongodb
        response = client.insertFiles(correo_id,typefile,filenamepos, filenameneg)

        if response == "Usuario NO existe, operación no valida":
            return jsonify(response), 500

        # el directorio para el usuario actual
        myfolder = app.config['UPLOAD_FOLDER']+'/'+correo_id
        # si no existe el directorio lo creamos
        createDirectory(myfolder)
        # guardar archivo en directorio para el usuario actual
        filepath =  app.config['UPLOAD_FOLDER']+'/'+ correo_id+'/'+typefile
        response += lc.index(filepath, filepos, fileneg, typefile)
        
        return jsonify(response), 200

    response = 'response post NO indexing'
    return jsonify(response), 200

@app.route('/search', methods = ['GET', 'POST'])
def search():
    response = ''
    body = request.get_json() # obtener el contenido del cuerpo de la solicitud
    
    if body is None:
        return "Request body es null", 400
    if body['positive'] == '':
        return 'Necesita especificar el archivo  positive',400
    if body['negative'] == '':
        return 'Necesita especificar el archivo negative',400
    if body['typefile'] == '':
        return 'Necesita especificar el tipo de archivo',400
    if body['wanted'] == '':
        return 'Necesita especificar que busca',400
    if body['email'] == '':
        return 'Es necesario que se identifique',400

    filepos = body['positive']
    fileneg = body['negative']
    typefile = body['typefile']
    correo = body['email']

    if (client.getCliente(correo) is False):
        return "Usuario NO existe, operación no valida"
    if typefile not in Typefiles:
        return "No existe el tipo de archivo seleccionado ",400

    count = filepos.find(".txt")
    count2 = fileneg.find(".txt")
    pathfile = app.config['UPLOAD_FOLDER']+'/'+correo+'/'+typefile+'/lucene_'+filepos[:count]
    resultado = lc.searchDocument(pathfile,body['wanted'])
    pathfile = app.config['UPLOAD_FOLDER']+'/'+correo+'/'+typefile+'/lucene_'+fileneg[:count2]
    aux = lc.searchDocument(pathfile,body['wanted'])

    for i in aux:
        resultado.append(i)
    return jsonify(resultado), 200

# Obtener los términos frecuencia de un par de archivos seleccionados.
@app.route('/tis', methods = ['GET', 'POST'])
def selectTIS():
    response = ''
    body = request.get_json() # obtener el contenido del cuerpo de la solicitud
    if body is None:
        return "Request body es null", 400
    if body['positive'] == '':
        return 'Necesita especificar el archivo  positive',400
    if body['negative'] == '':
        return 'Necesita especificar el archivo negative',400
    if body['typefile'] != 'filesTIS':
        return 'Sólo se admiten archivos TIS',400
    if body['email'] == '':
        return 'Es necesario que se identifique',400

    filepos = body['positive']
    fileneg = body['negative']
    typefile = body['typefile']
    correo = body['email']
    if (client.getCliente(correo) is False):
        return "Usuario NO existe, operación no valida"
        
    count = filepos.find(".txt")
    count2 = fileneg.find(".txt")
    pathfilepos = app.config['UPLOAD_FOLDER']+'/'+correo+'/filesTIS/lucene_'+filepos[:count]
    #print("pathfilepos")
    #print(pathfilepos)
    pathfileneg = app.config['UPLOAD_FOLDER']+'/'+correo+'/filesTIS/lucene_'+fileneg[:count2]
    #print("pathfileneg")
    #print(pathfileneg)
    resultadopos = lc.termsFreqsTIS(pathfilepos)
    #print("end positive")
    resultadoneg = lc.termsFreqsTIS(pathfileneg)
    #print(" end negative ")
    resultado = {'terms_freqs_positive': resultadopos, 'terms_freqs_negative': resultadoneg}
    return jsonify(resultado), 200

# se obtiene una consulta
@app.route('/filter', methods = ['GET', 'POST'])
def filter():
    body = request.get_json()
    typefilter = body['typefilter']
    if typefilter not in Filters:
        return "No existe el filtro seleccionado "
    if body['terms_freqs_positive'] == '':
        return 'Necesita especificar los terminos positivos',400
    if body['terms_freqs_negative'] == '':
        return 'Necesita especificar los terminos negativos',400
    if body['email'] == '':
        return 'Es necesario que se identifique',400
    if body['sum'] == '':
        return 'No ha especificado cuantas palabras quiere',400

    if (client.getCliente(body['email']) is False):
        return "Usuario NO existe, operación no valida"

    terms_freqs_positive = body['terms_freqs_positive']
    #print(terms_freqs_positive)
    terms_freqs_negative = body['terms_freqs_negative']
    #print(terms_freqs_negative)
    # números positivos
    sum = body['sum']
    #print(sum)
    email = body['email']
    #print(email)
    resultado = ft.filter(typefilter, terms_freqs_positive, terms_freqs_negative, sum, email)
    # devuelvo la consulta ???
    return jsonify(resultado), 200

# obtiene las medidas de rendimiento
@app.route('/applyFilter', methods = ['GET', 'POST'])
def applyFilter():
    response = ''
    body = request.get_json() # obtener el contenido del cuerpo de la solicitud
    if body is None:
        return "The request body is null", 400
    if body['email'] is None:
        return 'Es necesario que se identifique', 400
    if body['wanted'] == '':
        return 'Necesita especificar que busca',400

    correo = body['email']
    if (client.getCliente(body['email']) is False):
        return "Usuario NO existe, operación no valida"
    files = client.getFiles(correo)

    salida = {}
    if body['typefile'] == 'filesFVS':
        filesX = files['filesFVS']
    elif body['typefile']== 'filesFDS':
        filesX = files['filesFDS']
    else:
        return "Los tipos de archivos solo pueden ser FVS o FDS", 400

    for e in filesX:
        resultado = {}
        setAllPos = {}
        filepos = e['positive']
        fileneg = e['negative']
        typefile =  body['typefile']
        count = filepos.find(".txt")
        count2 = fileneg.find(".txt")
        pathfile = app.config['UPLOAD_FOLDER']+'/'+correo+'/'+typefile+'/lucene_'+filepos[:count]
        resultado[filepos[:count]] = lc.searchScore(pathfile,body['wanted'])
        setAllPos[filepos[:count]] = lc.positiveDocID(pathfile)
        pathfile = app.config['UPLOAD_FOLDER']+'/'+correo+'/'+typefile+'/lucene_'+fileneg[:count2]
        resultado[fileneg[:count2]] = lc.searchScore(pathfile,body['wanted'])
        
        salida[filepos[:count]] = md.medidas_de_rendimiento(setAllPos,resultado)    

    #print(salida)
    return jsonify(salida), 200

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def createDirectory(myfolder):
    try: 
        os.stat(myfolder)
    except:
        os.mkdir(myfolder)
        os.mkdir(myfolder+'/filesFVS')
        os.mkdir(myfolder+'/filesFDS')
        os.mkdir(myfolder+'/filesTIS')



@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:4201')
    response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With,content-type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

if __name__ == '__main__':
    app.run()
