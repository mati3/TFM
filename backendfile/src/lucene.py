import os
from datetime import datetime, timedelta

import lucene
from java.nio.file import Paths
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, DirectoryReader
from org.apache.lucene.document import Document, Field, StringField, TextField
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.queryparser.classic import QueryParser, QueryParserBase, MultiFieldQueryParser
from org.apache.lucene.search import IndexSearcher

lucene.initVM()

class Lucene:

    def indexar(self, filepath):
        directory = SimpleFSDirectory(Paths.get(filepath+"/lucene"))
        analyzer = EnglishAnalyzer()
        analyzer = LimitTokenCountAnalyzer(analyzer, 10000)
        config = IndexWriterConfig(analyzer)
        writer = IndexWriter(directory, config)

        # 'AB  -' -> es abtrast
        # 'KW  -' -> son las palabras claves
        # 'ST  -' -> es el titulo
        lista = os.listdir(filepath)
        if "lucene" in lista: lista.remove("lucene") 
        for file in lista:
            doc = Document()
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
                    #print(' ********* ABTRAST ***********')
                    #print(line)
                    abtrast = line
                if line.find('ST  -') != -1:
                    print(' ********* TITULO *********')
                    print(line)
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
                Field("abtrast", abtrast, TextField.TYPE_STORED)
            )
            doc.add(
                Field("titulo", titulo, TextField.TYPE_STORED)
            )
            doc.add(
                Field("golden_words", golden, TextField.TYPE_STORED)
            )
            writer.addDocument(doc)
            writer.commit()
        writer.close()
        print(" end ")


    def search(self, filepath, word):
        directory = SimpleFSDirectory(Paths.get(filepath+"/lucene"))
        searcher = IndexSearcher(DirectoryReader.open(directory))
        analyzer = EnglishAnalyzer()
        query = QueryParser("abtrast", analyzer).parse(word)
        result = []
        #fields = ["titulo","abtrast","golden_words"]
        #parser = MultiFieldQueryParser( fields, analyzer)
        #parser.setDefaultOperator(QueryParserBase.AND_OPERATOR)
        #query = parser.parse(word)
        #query = MultiFieldQueryParser.parse(word,["titulo","abtrast","golden_words"], analyzer)
        print("filepath")
        print(filepath)
        print("word")
        print(word)
        print("query")
        print(query)
        scoreDocs = searcher.search(query, 10).scoreDocs
        #print("scoreDocs")
        #print(scoreDocs)
        for sd in scoreDocs:
            d = searcher.doc(sd.doc)
            result.append({
                    "titulo":  d.get("titulo"),
                    "abtrast": d.get("abtrast"),
                    "golden_words": d.get("golden_words")
                })
            #print(' ********* titulo')
            #print(doc.get("titulo"))
            #print(' ********* abtrast')
            #print(doc.get("abtrast"))
            #print(' ********* golden words')
            #print(doc.get("golden words"))
        return result
