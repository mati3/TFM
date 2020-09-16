#!/usr/bin/env python
# coding: utf-8
from flask import jsonify
import requests
import json

import lucene
from lupyne import engine
lucene.initVM()

class Lucene:
    
    def __init__ (self, cat=None):
        self.catalogo= []
        self.catalogo = json.dumps(cat)
   
    def test(self):
        searcher = engine.IndexSearcher('index/path')
        hits = searcher.search('text:query')
        
