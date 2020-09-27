import os
from datetime import datetime, timedelta

import lucene
from java.nio.file import Paths
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, DirectoryReader
from org.apache.lucene.document import Document, Field, StringField, TextField
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher

lucene.initVM()

class Lucene:

    def indexar(self, filepath):
        directory = SimpleFSDirectory(Paths.get(filepath+"/lucene"))
        analyzer = EnglishAnalyzer()
        analyzer = LimitTokenCountAnalyzer(analyzer, 10000)
        config = IndexWriterConfig(analyzer)
        writer = IndexWriter(directory, config)

        doc = Document()
        # 'AB  -' -> es abtrast
        # 'KW  -' -> son las palabras claves
        # 'ST  -' -> es el titulo
        lista = os.listdir(filepath)
        if "lucene" in lista: lista.remove("lucene") 
        for file in lista:
            with open(filepath+'/'+file) as fp:
                text = fp.readlines()
                #print('******** FILE ********')
                #print(file)
                abtrast = ''
                titulo = ''
                golden = ''
                start = False
            for line in text:
                if line.find('AB  -') != -1:
                    print(' ********* ABTRAST ***********')
                    print(line)
                    abtrast = line
                if line.find('ST  -') != -1:
                    #print(' ********* TITULO *********')
                    #print(line)
                    titulo = line
                # 'N1  -' or 'PY  -'
                if line.find('KW  -') != -1:
                    start = True
                    #print(' ********* GOLDEN WORDS *********')
                if (line.find('PY  -') != -1) or (line.find('N1  -') != -1):  #or line.find('N1  -')
                    start = False
                if start:
                    #print(line)
                    golden = golden + line
            doc.add(
                Field("abtrast", abtrast, StringField.TYPE_STORED)
            )
            doc.add(
                Field("titulo", titulo, StringField.TYPE_STORED)
            )
            doc.add(
                Field("golden words", golden, StringField.TYPE_STORED)
            )

            writer.addDocument(doc)
            writer.commit()
        print(" end ")
        writer.close()

    def search(self, filepath, word):
        directory = SimpleFSDirectory(Paths.get(filepath+"/lucene"))
        searcher = IndexSearcher(DirectoryReader.open(directory))
        analyzer = EnglishAnalyzer()
        query = QueryParser("abtrast", analyzer).parse(word)
        print("word")
        print(word)
        print("query")
        print(query)
        #query = "titulo:"+filename
        #print(query)
        scoreDocs = searcher.search(query, 10).scoreDocs
        print("scoreDocs")
        print(scoreDocs)
        for sd in scoreDocs:
            doc = searcher.doc(sd.doc)
            print(' ********* abtrast')
            print(doc.get("titulo"))
