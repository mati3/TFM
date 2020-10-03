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
from org.apache.lucene.search import IndexSearcher, BooleanClause

lucene.initVM()

class Lucene():

    def indexar(self, filepath):
        directory = SimpleFSDirectory(Paths.get(filepath+"/lucene"))
        analyzer = EnglishAnalyzer()
        analyzer = LimitTokenCountAnalyzer(analyzer, 10000)
        config = IndexWriterConfig(analyzer)
        writer = IndexWriter(directory, config)

        # 'AB  -' -> es Abstract
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
                abstract = ''
                titulo = ''
                golden = ''
                start = False
            for line in text:
                if line.find('AB  -') != -1:
                    #print(' ********* Abstract ***********')
                    #print(line)
                    abstract = line
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
                Field("abstract", abstract, TextField.TYPE_STORED)
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
        return 'files upload ok'


    def search(self, filepath, word):
        directory = SimpleFSDirectory(Paths.get(filepath+"/lucene"))
        searcher = IndexSearcher(DirectoryReader.open(directory))
        analyzer = EnglishAnalyzer()
        #query = QueryParser("abstract", analyzer).parse(word)
        result = []
        SHOULD = BooleanClause.Occur.SHOULD
        query = MultiFieldQueryParser.parse(QueryParserBase.escape(word), ["titulo","abstract","golden_words"],
                                                [SHOULD, SHOULD, SHOULD],
                                                analyzer)
        scoreDocs = searcher.search(query, 1000).scoreDocs
        #print("scoreDocs")
        #print(scoreDocs)
        for sd in scoreDocs:
            d = searcher.doc(sd.doc)
            result.append({
                    "titulo":  d.get("titulo"),
                    "abstract": d.get("abstract"),
                    "golden_words": d.get("golden_words")
                })
            #print(' ********* titulo')
            #print(doc.get("titulo"))
            #print(' ********* abstract')
            #print(doc.get("abstract"))
            #print(' ********* golden words')
            #print(doc.get("golden words"))
        return result
