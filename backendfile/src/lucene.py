from flask import jsonify, Flask, request, render_template
import requests
import json

from bs4 import BeautifulSoup
import os
from datetime import datetime, timedelta

import lucene
from lupyne import engine

from java.nio.file import Paths
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.es import SpanishAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, DirectoryReader
from org.apache.lucene.document import Document, Field, StringField, TextField
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher

lucene.initVM()

class Lucene:

    def main(self):
        resultados = []
        indice_vacio = False
        if len(os.listdir("./lucene/index")) == 0:
            indice_vacio = True
        else:
            consulta = request.args.get("consulta", None)
            if consulta is not None:
                directory = SimpleFSDirectory(Paths.get("./lucene/index"))
                searcher = IndexSearcher(DirectoryReader.open(directory))
                analyzer = SpanishAnalyzer()
                query = QueryParser("texto", analyzer).parse(consulta)
                scoreDocs = searcher.search(query, 10).scoreDocs

                for sd in scoreDocs:
                    doc = searcher.doc(sd.doc)
                    resultados.append({
                        "url": 'https://boe.es' + doc.get("pdf"),
                        "titulo": doc.get("titulo")
                    })


        return render_template("main.html", lucene=lucene.VERSION, indice_vacio=indice_vacio, resultados=resultados)

    def colectar(self):
        fecha_inicio = request.args.get("fecha_inicio", None)
        fecha_fin = request.args.get("fecha_fin", None)

        for root, dirs, files in os.walk("./documentos"):
            for file in files:
                os.remove(os.path.join(root, file))

        fecha_inicio = datetime.strptime(fecha_inicio, "%d-%m-%Y") if fecha_inicio is not None else datetime.today()
        fecha_fin = datetime.strptime(fecha_fin, "%d-%m-%Y") if fecha_fin is not None else datetime.today()

        data = []
        boletines = 0
        while fecha_inicio <= fecha_fin:
            direccion = 'https://boe.es' + "/diario_boe/xml.php?id=BOE-S-"+fecha_inicio.strftime("%Y%m%d")
            print(direccion)
            r = requests.get(direccion)
            if r.status_code != 400:
                bs = BeautifulSoup(r.text, "lxml")
                if bs.error is None:
                    xmls = bs.find_all("urlxml")
                    for x in xmls:
                        ra = requests.get('https://boe.es'+x.text)
                        if ra.status_code != 400:
                            bsa = BeautifulSoup(ra.text, "lxml")
                            identificador = bsa.documento.metadatos.identificador.text
                            data.append(identificador)
                            boletines += 1
                            print(boletines)
                            open("./documentos/"+identificador+".xml","w").write(ra.text)
            fecha_inicio = fecha_inicio + timedelta(days=1)
        
        return render_template("colectados.html", lucene=lucene.VERSION, data=data, boletines=boletines)

    def indexar(self):
        directory = SimpleFSDirectory(Paths.get("./lucene/index"))
        analyzer = SpanishAnalyzer()
        analyzer = LimitTokenCountAnalyzer(analyzer, 10000)
        config = IndexWriterConfig(analyzer)
        writer = IndexWriter(directory, config)

        doc_names = os.listdir("./documentos")
        indexados = 0
        for dn in doc_names:
            d = open("./documentos/"+dn, "r")
            bs = BeautifulSoup(d, "lxml")
            d.close()
            doc = Document()
            doc.add(
                Field("id", bs.documento.metadatos.identificador.text, StringField.TYPE_STORED)
            )
            doc.add(
                Field("titulo", bs.documento.metadatos.titulo.text, StringField.TYPE_STORED)
            )
            doc.add(
                Field("pdf", bs.documento.metadatos.url_pdf.text, StringField.TYPE_STORED)
            )
            doc.add(
                Field("texto", bs.documento.texto.text, TextField.TYPE_STORED)
            )
            writer.addDocument(doc)
            indexados += 1
        writer.commit()
        writer.close()
        
        return render_template("indexados.html", lucene=lucene.VERSION, indexados=indexados)
