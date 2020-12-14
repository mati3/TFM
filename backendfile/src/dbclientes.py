#   Trabajo Fin de Máster
#   Máster en Ingeniería Informática
#
#   2020 - Copyright (c) - GNU v3.0
#
#  Matilde Cabrera <mati331@correo.ugr.es>

import json
from pymongo import MongoClient

class dbClientes:
    def __init__(self, collection):
        self.client = collection 
        if self.client.count_documents({'_id':'mati@correo.ugr.es' })==0: 
            self.client.insert_one({'_id':'mati@correo.ugr.es', 'filesFDS':[],'filesFVS':[],'filesTIS':[]  })

    def insertClient(self, correo_id):
        clientes = self.client.find({},{"FVS":1,"_id":1})
        salida = "ok"
        for c in clientes:
            if correo_id == c['_id'] :
                salida = "Usuario existente, operación no valida"
        if salida == "ok" :
            FDS = []
            FVS = []
            TIS = []
            self.client.insert_one({'_id':correo_id,'filesFDS':FDS,'filesFVS':FVS,'filesTIS':TIS })
            salida = "Usuario registrado : " + correo_id
        return  salida 
    
    def deleteClient(self, correo_id):
        self.client.delete_one({"_id": correo_id})
        return self.client.count_documents({"_id": correo_id})

    def getClientes(self):
        clientes = self.client.find({},{"_id":1})
        salida = []
        for c in clientes:
            salida.append(c['_id'])
        return  salida

    def getCliente(self, correo_id):
        clientes = self.client.find({},{"_id":1})
        salida = False
        for c in clientes:
            if correo_id == c['_id']:
                salida = True
                return salida
        return  salida

    def insertFiles(self, correo_id, typefile, filenamepos, filenameneg):
        if self.client.count_documents({'_id': correo_id })==0: 
            return "Usuario NO existe, operación no valida"
        else:
            cliente = self.client.find_one({"_id":correo_id},{'filesFDS':1,'filesFVS':1,'filesTIS':1 })
            salida = []
            for f in cliente.get(typefile):
                salida.append(f)
            salida.append({'positive':filenamepos, 'negative':filenameneg})
            self.client.update({'_id':correo_id} , {'$set': {typefile:salida} }, True)
        return  salida   

    def getFiles(self, correo_id):
        if self.client.count_documents({'_id': correo_id })==0: 
            return "Usuario no encontrado"
        return self.client.find_one({"_id":correo_id},{'filesFDS':1,'filesFVS':1,'filesTIS':1 })


    def deleteFiles(self, correo_id,typefile):
        #print("deletefiles")
        delete = self.client.update({'_id':correo_id} , {'$set': {typefile:[]} })
        salida = delete['updatedExisting']
        #print(salida)
        return salida
