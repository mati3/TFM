import os
import operator
from datetime import datetime, timedelta

import lucene
from java.nio.file import Paths
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.index import Term, IndexOptions, IndexReader, FieldInfos, MultiFields, IndexWriter, IndexWriterConfig, DirectoryReader, MultiTerms
from org.apache.lucene.document import Document, Field, StringField, TextField, FieldType
from org.apache.lucene.store import SimpleFSDirectory, NIOFSDirectory
from org.apache.lucene.queryparser.classic import QueryParser, QueryParserBase, MultiFieldQueryParser
from org.apache.lucene.search import IndexSearcher, BooleanClause, TermQuery
from org.apache.lucene.util import BytesRefIterator
from org.apache.lucene import index, util
from org.apache.lucene.classification.utils import ConfusionMatrixGenerator

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

    def indexTIS(self, filepath, file, filename):
        path = filepath+"/lucene_"+filename
        try: 
            os.stat(path)
        except:
            os.mkdir(path)
        directory = SimpleFSDirectory(Paths.get(path))
        analyzer = EnglishAnalyzer() # No hacer steaming. hay que hacer la consulta con los terminos originales.
        analyzer = LimitTokenCountAnalyzer(analyzer, 10000)
        config = IndexWriterConfig(analyzer)
        writer = IndexWriter(directory, config)

        doc = Document()
        text = file.readlines()
        #print('******** FILE ********')
        #print(file)
        abstract = ''
        titulo = ''
        golden = ''
        start = False
        
        # creo una instancia de FieldType para establecer storeTermVector
        # proposito poder sacar las frecuencias.
        tft = FieldType()
        tft.setStored(True)
        tft.setTokenized(True)
        tft.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS_AND_OFFSETS)
        tft.setStoreTermVectors(True)
        tft.setStoreTermVectorPositions(True)
        tft.freeze()

        for line in text:
            if line.find(b'AB  -') != -1:
                abstract = line.decode('utf-8')
            if line.find(b'ST  -') != -1:
                titulo = line.decode('utf-8')
            # 'N1  -' or 'PY  -'
            if line.find(b'KW  -') != -1:
                start = True
                #print(' ********* GOLDEN WORDS *********')
            if (line.find(b'PY  -') != -1) or (line.find(b'N1  -') != -1): 
                start = False
                # si no tenemos palabras clave, no se guardará el doc
                doc.add(
                    Field("abstract", abstract, TextField.TYPE_STORED)
                )
                doc.add(
                    Field("titulo", titulo, TextField.TYPE_STORED)
                )
                doc.add(
                    Field("golden_words", golden, tft)
                )
                writer.addDocument(doc)
                writer.commit()
                doc = Document()
            if start:
                golden = golden + line.decode('utf-8')
            
        writer.close()

        return 'files upload ok'

    def search(self, filepath, word):
        directory = SimpleFSDirectory(Paths.get(filepath+"/lucene"))
        searcher = IndexSearcher(DirectoryReader.open(directory))
        analyzer = EnglishAnalyzer()
        result = []
        SHOULD = BooleanClause.Occur.SHOULD
        query = MultiFieldQueryParser.parse(QueryParserBase.escape(word), ["titulo","abstract","golden_words"],
                                                [SHOULD, SHOULD, SHOULD],
                                                analyzer)
        scoreDocs = searcher.search(query, 1000).scoreDocs
        for sd in scoreDocs:
            d = searcher.doc(sd.doc)
            result.append({
                    "titulo":  d.get("titulo"),
                    "abstract": d.get("abstract"),
                    "golden_words": d.get("golden_words")
                })
        return result

    def selectTIS(self, filepath):
        store = SimpleFSDirectory(Paths.get(filepath))
        reader = None
        try:
            reader = DirectoryReader.open(store)
            term_enum = MultiTerms.getTerms(reader, "golden_words").iterator()
            
            docids = [term.utf8ToString()
                      for term in BytesRefIterator.cast_(term_enum)]
            print("docids")
            print(docids)

            # devuelve los terminos
            terminos = MultiTerms.getTerms(reader,"golden_words")
            indexReader = DirectoryReader.open(NIOFSDirectory.open(Paths.get(filepath)))
            docCount = indexReader.numDocs()
            terms_freqs = {}
            for doc in range(docCount):
                print("nº de documento: " + str(doc))
                #vector de terminos
                termss = indexReader.getTermVector(doc, "golden_words")
                termsEnum = termss.iterator()
                terms = []
                freqs = []
                #terms_freqs = []
                for term in BytesRefIterator.cast_(termsEnum):
                    terms.append(term.utf8ToString())
                    freqs.append(termsEnum.totalTermFreq())
                    terms_freqs[term.utf8ToString()]=termsEnum.totalTermFreq()    
            print("terms")
            print(terms)
            print("freq")
            print(freqs)
            print("terms_freqs")
            print(terms_freqs)
            
            termss = indexReader.getTermVector((docCount-1), "golden_words")
            termsEnum = termss.iterator()
            terms = []
            freqs = []
            terms_freqs2 = []
            for term in BytesRefIterator.cast_(termsEnum):
                terms.append(term.utf8ToString())
                freqs.append(termsEnum.totalTermFreq())
                terms_freqs2.append({term.utf8ToString(), termsEnum.totalTermFreq()}) 
            print("terms")
            print(terms)
            print("freq")
            print(freqs)
            print("terms_freqs2")
            print(terms_freqs2)
            
        finally:
            store.close()
        return terms_freqs

    def filterfreq(self, resultadopos, resultadoneg):
        for k in resultadoneg:
            if k in resultadopos:
                del resultadopos[k]
        print(resultadopos)
        salida = sorted(resultadopos, key=resultadopos.get, reverse=True)
        print(salida)
        return salida
    

    def medidas_de_rendimiento(self, filepath, textFieldName):
        store = SimpleFSDirectory(Paths.get(filepath))
        reader = None
        try:
            reader = DirectoryReader.open(store)
            classifier = analyzer = EnglishAnalyzer()
            categoryFieldName = "golden_words"
            #textFieldName = "lista de palabras"
            confusionMatrix = ConfusionMatrixGenerator.getConfusionMatrix(reader, classifier, categoryFieldName, textFieldName, -1)

            avgClassificationTime = confusionMatrix.getAvgClassificationTime()
            accuracy = confusionMatrix.getAccuracy()
            print("accuracy")
            print(accuracy)
            precision = confusionMatrix.getPrecision()
            print("precision")
            print(precision)
            recall = confusionMatrix.getRecall()
            print("recall")
            print(recall)
            f1Measure = confusionMatrix.getF1Measure()
            print("f1Measure")
            print(f1Measure)

            term_enum = MultiTerms.getTerms(reader, "golden_words").iterator()
            
            docids = [term.utf8ToString()
                      for term in BytesRefIterator.cast_(term_enum)]

            for term in docids:
                precision = confusionMatrix.getPrecision(term)
                print("precision")
                print(precision)
                recall = confusionMatrix.getRecall(term)
                print("recall")
                print(recall)
                f1Measure = confusionMatrix.getF1Measure(term)
                print("f1Measure")
                print(f1Measure)
        finally:
            if (reader != None):
                reader.close()
            
        