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

Filters = {'InfGain', 'CrossEntropy' , 'MutualInfo', 'Freq' , 'OddsRatio', 'NormalSeparation', 'Diferencia'}

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
    myfolder = app.config['UPLOAD_FOLDER']+'/'+ correo_id
    # si no existe lo creamos
    createDirectory(myfolder)
    return  jsonify(client.insertClient(correo_id)), 200    

# remove client
@app.route('/delete/<string:correo_id>', methods = ['DELETE'])
def deleteClient(correo_id):
    return  jsonify(client.deleteClient(correo_id)), 200 

# devuelve los archivos Indexados de un cliente dado su id
@app.route('/filesindex/<string:correo_id>', methods=['GET'])
def filesindex(correo_id):
    myfolder = app.config['UPLOAD_FOLDER']+'/'+ correo_id
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
        filenamepos = secure_filename(filepos.filename)
        filenameneg = secure_filename(fileneg.filename)
        # Guardo nombres en mongodb
        response = client.insertFiles(correo_id,typefile,filenamepos, filenameneg)

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
        return "The request body is null", 400
    if body['positive'] is None:
        return 'You need to specify the file positive',400
    if body['negative'] is None:
        return 'You need to specify the file negative',400
    if body['typefile'] == '':
        return 'You need to specify the typefile',400
    if body['wanted'] == '':
        return 'You need to specify what looking for',400

    filepos = body['positive']
    fileneg = body['negative']
    typefile = body['typefile']
    correo = body['id']['email']
    count = filepos.find(".txt")
    count2 = fileneg.find(".txt")
    pathfile = app.config['UPLOAD_FOLDER']+'/'+correo+'/'+typefile+'/lucene_'+filepos[:count]
    resultado = lc.search(pathfile,body['wanted'], False)
    pathfile = app.config['UPLOAD_FOLDER']+'/'+correo+'/'+typefile+'/lucene_'+fileneg[:count2]
    aux = lc.search(pathfile,body['wanted'], False)

    for i in aux:
        resultado.append(i)
    return jsonify(resultado), 200

@app.route('/tis', methods = ['GET', 'POST'])
def selectTIS():
    response = ''
    body = request.get_json() # obtener el contenido del cuerpo de la solicitud
    if body is None:
        return "The request body is null", 400
    if body['positive'] is None:
        return 'You need to specify the file positive',400
    if body['negative'] is None:
        return 'You need to specify the file negative',400

    filepos = body['positive']
    fileneg = body['negative']
    typefile = body['typefile']
    correo = body['id']['email']
    count = filepos.find(".txt")
    count2 = fileneg.find(".txt")
    pathfilepos = app.config['UPLOAD_FOLDER']+'/'+correo+'/filesTIS/lucene_'+filepos[:count]
    print("pathfilepos")
    print(pathfilepos)
    pathfileneg = app.config['UPLOAD_FOLDER']+'/'+correo+'/filesTIS/lucene_'+fileneg[:count2]
    print("pathfileneg")
    print(pathfileneg)
    resultadopos = lc.termsFreqsTIS(pathfilepos)
    print("end positive")
    resultadoneg = lc.termsFreqsTIS(pathfileneg)
    print(" end negative ")
    resultado = {'terms_freqs_positive': resultadopos, 'terms_freqs_negative': resultadoneg}
    return jsonify(resultado), 200

@app.route('/filter', methods = ['GET', 'POST'])
def filter():
    body = request.get_json()
    typefilter = body['typefilter']
    if typefilter not in Filters:
        return "No existe el filtro seleccionado "
    terms_freqs_positive = body['terms_freqs_positive']
    print(terms_freqs_positive)
    terms_freqs_negative = body['terms_freqs_negative']
    print(terms_freqs_negative)
    sum = body['sum']
    print(sum)
    email = body['email']
    print(email)
    resultado = lc.filter(typefilter, terms_freqs_positive, terms_freqs_negative, sum, email)
    # devuelvo la consulta ???
    return jsonify(resultado), 200

@app.route('/applyFilter', methods = ['GET', 'POST'])
def applyFilter():
    response = ''
    body = request.get_json() # obtener el contenido del cuerpo de la solicitud
    if body is None:
        return "The request body is null", 400
    if body['id']['email'] is None:
        return 'You need to identify yourself', 400
    if body['wanted'] == '':
        return 'You need to specify what looking for',400

    correo = body['id']['email']
    files = client.getFiles(correo)
    for i in files:
        filesFVS = i['filesFVS']
        filesFDS = i['filesFDS']
        filesTIS = i['filesTIS'] 
        files = {'filesFVS':filesFVS, 'filesFDS': filesFDS, 'filesTIS': filesTIS}

    salida = {}
    if body['typefile'] == 'filesFVS':
        filesX = filesFVS
    elif body['typefile']== 'filesFDS':
        filesX = filesFDS
    for e in filesX:
        resultado = {}
        setAllPos = {}
        filepos = e['positive']
        fileneg = e['negative']
        typefile =  body['typefile']
        count = filepos.find(".txt")
        count2 = fileneg.find(".txt")
        #pathfile = app.config['UPLOAD_FOLDER']+'/'+correo+'/'+typefile+'/'+filepos[:count]+fileneg[:count2]
        #resultado.append(lc.search(pathfile,body['wanted']))
        pathfile = app.config['UPLOAD_FOLDER']+'/'+correo+'/'+typefile+'/lucene_'+filepos[:count]
        resultado[filepos[:count]] = lc.search(pathfile,body['wanted'], True)
        #setPos = lc.searchDocID(pathfile))
        setAllPos[filepos[:count]] = lc.positiveDocID(pathfile)
        pathfile = app.config['UPLOAD_FOLDER']+'/'+correo+'/'+typefile+'/lucene_'+fileneg[:count2]
        resultado[fileneg[:count2]] = lc.search(pathfile,body['wanted'], True)
        '''for r in searchpos:
            resultado.append(r)
        for i in searchneg:
            resultado.append(i)'''
        '''for i in setPos:
            setAllFVSPos.append(i)'''
        salida[filepos[:count]] = lc.medidas_de_rendimiento(setAllPos,resultado)    

    print(salida)
    return jsonify(salida), 200

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def concat_file2(file1, file2, myfolder):
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
    return lc.indexar(filepath,filename)

def concat_file(file1, file2, myfolder):
    count = file1.find(".txt")
    count2 = file2.find(".txt")
    filename = file1[:count]+file2[:count2]
    f1 = open(myfolder+'/'+file1, "r").read()
    f2 = open(myfolder+'/'+file2, "r").read()
    filepath = myfolder+'/'+filename
    try: 
        os.stat(filepath)
    except:
        os.mkdir(filepath)

    newfile = open(myfolder+'/'+filename+'.txt', "a")
    newfile.write(f1 + f2)
    newfile.close()

    text_file = open(myfolder+'/'+filename+'.txt','r')
    docs =text_file.read()
    text_file.close()
    contador = 0
    for i in docs:
        if contador < 100:
            primero = docs.find("- JOUR")
            ultimo = docs.find("ER  -")
            cadena = docs[primero:ultimo]
            if primero != -1 :
                new_file = open(filepath+'/DOC_0' + str(contador) + '.txt' , 'w')
                new_file.write(cadena)
                new_file.close()
        else:
            primero = docs.find("- JOUR")
            ultimo = docs.find("ER  -")
            cadena = docs[primero:ultimo]
            if primero != -1 :
                new_file = open(filepath+'/DOC_' + str(contador) + '.txt' , 'w')
                new_file.write(cadena)
                new_file.close()

        # elimino el documento recogido.
        docs = docs.replace(cadena,"")
        docs = docs.replace("TY  ER  -","")
        contador = contador + 1
    os.remove(myfolder+'/'+filename+'.txt')
    start = time()
    response = lc.indexar(filepath)   
    end = time()
    elapsed_time = end - start
    print("indexar")
    print("Elapsed time: %0.10f seconds." % elapsed_time)  
    return response

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
