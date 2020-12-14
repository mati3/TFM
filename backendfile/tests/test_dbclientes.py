#!/usr/bin/env python
# coding: utf-8

import unittest
import json
import sys, os.path

dir_path = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))+ '/src/')
sys.path.append(dir_path)

from dbclientes import dbClientes
from pymongo import MongoClient
import mongomock

@mongomock.patch(servers=(('mongodb', 27017),))
def db():
    c = MongoClient('mongodb')
    con = c.baseDeDatos
    db = dbClientes(con.Clientes)
    return db

class TestdbClientes(unittest.TestCase): 

    def test_insert(self):
        self.assertEqual(db().insertClient("mati@ugr.es"), "Usuario registrado : mati@ugr.es", "usuario no registrado")
        self.assertEqual(db().insertClient("mati@ugr.es"), "Usuario existente, operación no valida", "usuario existente error")
        self.assertEqual(db().insertFiles("mati@ugr.es","filesTIS","all_positive","all_negative"), [{'positive': 'all_positive', 'negative': 'all_negative'}], "archivo no insertado, error")
        self.assertEqual(db().insertFiles("nadie@ugr.es", "filesTIS", "all_positive", "all_negative"), "Usuario NO existe, operación no valida", "usuario existe, error")

    def test_get(self):
        self.assertIsNot(db().getClientes(), [], "sin clientes error")
        self.assertIsNot(db().getCliente("mati@ugr.es"), [], "usuario no encontrado, error")
        self.assertEqual(db().getFiles("nadie@ugr.es"), "Usuario no encontrado", "usuario existe, error")
        self.assertEqual(db().getFiles("mati@correo.ugr.es"), { "_id": "mati@correo.ugr.es", "filesFDS" : [], "filesFVS" : [], "filesTIS" : [] }, "archivos no encontrados, error")
    
    def test_delete(self):
        self.assertEqual(db().deleteFiles("mati@ugr.es", "filesTIS"), 0, "archivos no eliminados, error")
        self.assertEqual(db().deleteClient("mati@ugr.es"), 0, "user no borrado error")

