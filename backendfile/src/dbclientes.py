import json
from pymongo import MongoClient

class dbClientes:
    def __init__(self, collection):
        self.client = collection

#########
    def insertClient(self, correo_id):
        clientes = self.client.find({},{"FVS":1,"_id":1})
        salida = "ok"
        for c in clientes:
            if correo_id == c['_id'] :
                salida = "Usuario existente, operación no valida"
        if salida == "ok" :
            FDS = []
            FVS = []
            TIS = {}
            self.client.insert_one({'_id':correo_id,'FDS':FDS,'FVS':FVS,'TIS':TIS })
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

################
    def insertFile(self, correo_id, typefile, filename):
        clientes = self.client.find({},{"_id":1})
        salida = "Usuario NO existe, operación no valida"
        for c in clientes:
            if correo_id == c['_id'] :
                salida = "ok"
        if salida == "ok" :
            self.client.insert_one({'_id':correo_id, typefile:filename })
            salida = "archivo insertado : " + correo_id
        return  salida       


    def getAll(self):
        clientes = self.client.find({},{"FVS":1,"_id":1})
        salida = []
        for c in clientes:
            salida.append(c)
        return  salida

    def getCesta(self, correo_id):
        clientes = self.client.find({"_id": correo_id},{"FVS":1,"_id":0,"TIS":1})
        salida = []
        for c in clientes:
            FVS = c['FVS']
            for f in FVS:
                salida.append(f)
            salida.append(c['TIS'])
        return salida


