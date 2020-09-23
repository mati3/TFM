import os
from datetime import datetime, timedelta

import lucene
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

    def indexar(self, filepath, filename):
        directory = SimpleFSDirectory(Paths.get("./lucene/index"))
        analyzer = SpanishAnalyzer()
        analyzer = LimitTokenCountAnalyzer(analyzer, 10000)
        config = IndexWriterConfig(analyzer)
        writer = IndexWriter(directory, config)

        d = open(filepath, "r")
        doc = Document()
        doc.add(
            Field("titulo", filename, StringField.TYPE_STORED)
        )
        print(doc['titulo'])
        doc.add(
            Field("texto", d.read(), TextField.TYPE_STORED)
        )
        d.close()
        writer.addDocument(doc)
        
        writer.commit()
        writer.close()
        print(filename)
        searcher = IndexSearcher(DirectoryReader.open(directory))
        query = QueryParser("titulo", analyzer).parse(filename)
        print(query)
        #query = "titulo:"+filename
        #print(query)
        scoreDocs = searcher.search(query, 10).scoreDocs
        print(scoreDocs)
        for sd in scoreDocs:
            doc = searcher.doc(sd.doc)
            print(' ********* titulo')
            print(doc.get("titulo"))