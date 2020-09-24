import json
from pymongo import MongoClient

class dbClientes:
    def __init__(self, collection):
        self.client = collection
        cur = self.client.find({'_id':'mati@correo.ugr.com' }) 
        if cur.count()==0: 
            self.client.insert_one({'_id':'mati@correo.ugr.com', 'filesFDS':[],'filesFVS':[],'filesTIS':[]  })

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
            TIS = []
            #self.client.insert_one({'_id':correo_id })
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

    def insertFiles(self, correo_id, typefile, filenamepos, filenameneg):
        clientes = self.client.find({},{"_id":1})
        salida = "Usuario NO existe, operación no valida"
        for c in clientes:
            if correo_id == c['_id'] :
                salida = "ok"
        if salida == "ok" :
            clientes = self.client.find({},{"_id":correo_id, typefile:1})
            salida = []
            print('clientes')
            print(clientes)
            for count,f in enumerate(clientes):
                print('f')
                print(f)
                if f.get(typefile):
                    for f2 in f.get(typefile):
                        print('f2')
                        print(f2)
                        salida.append(f2)
            print('salida 1 ')
            print(salida)
            salida.append({'positive':filenamepos, 'negative':filenameneg})
            print('salida 2 ')
            print(salida)
            self.client.update({'_id':correo_id} , {'$set': {typefile:salida} }, True)
            #self.client.insert_one({'_id':correo_id, typefile:{'positive':filenamepos, 'negative':filenameneg} })
            salida = "archivo insertado : " + correo_id
        return  salida   

    def getFiles(self, correo_id):
        return self.client.find({},{"_id":correo_id,'filesFDS':1,'filesFVS':1,'filesTIS':1 })

################
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


