import os
import operator
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from itertools import *
import math
import numpy as np, scipy.stats as st
from scipy.special import ndtri
import json
import pytrec_eval

import lucene
from java.nio.file import Paths
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import Term, IndexOptions, IndexReader, FieldInfos, MultiFields, IndexWriter, IndexWriterConfig, DirectoryReader, MultiTerms
from org.apache.lucene.document import Document, Field, StringField, TextField, FieldType
from org.apache.lucene.store import SimpleFSDirectory, NIOFSDirectory
from org.apache.lucene.queryparser.classic import QueryParser, QueryParserBase, MultiFieldQueryParser
from org.apache.lucene.search import IndexSearcher, BooleanClause, TermQuery
from org.apache.lucene.util import BytesRefIterator
from org.apache.lucene import index, util
from org.apache.lucene.classification.utils import ConfusionMatrixGenerator
from org.apache.lucene.analysis import  StopwordAnalyzerBase
from org.apache.lucene.analysis.core import StopFilter, StopAnalyzer

lucene.initVM()

class Lucene():

    def createDirectory(self, myfolder):
        """
        Crea un nuevo directorio.

        Comprueba si el directorio no existe lo crea.

        Args:
        ----------
        myfolder : string  
        >    Ruta para el nuevo directorio.

        """
        try: 
            os.stat(myfolder)
        except:
            os.mkdir(myfolder)

    def addDocument(self, writer, file, filename, tft):
        """
        Indexa una serie de documentos que se encuentran en un archivo.

        Indexa una serie de documentos para consultas biomédicas, con unas caracteristicas específicas, por cada documento se guardará:

        ***docid*** → Identificación del documento (nombre_del_archivo_x, estando x en el rango [1 - nº de documentos]).  
        ***abstract*** → sección abstract del documento. En una sola línea comenzando por 'AB  -'.  
        ***título*** → sección de título del documento. En una sola línea comenzando por 'ST  -'.  
        ***key words*** → sección de palabras clave del documento. Comienza siempre con 'KW  -' y termina con 'N1  -' or 'PY  -'

        Args:
        ----------
        writer : IndexWriter
        >    Crea y mantiene un índice.  

        file : File
        >    Archivo a indexar.  

        filename : String
        >    Nombre del archivo que contiene los documentos.  
        
        tft : FieldType
        >    Instancia de FieldType para establecer storeTermVector ó TextField.TYPE_STORED, dependiendo del tipo de archivo a indexar.

        """
        docid = 1
        docs =file.read()
        # por todos los documentos
        for line in docs:
            primero = docs.find(b"- JOUR")
            ultimo = docs.find(b"ER  -")
            cadena = docs[primero:ultimo]
            # para cada documento
            if (cadena != -1) and (primero != -1) and (ultimo != -1):
                doc = Document()
                text = cadena.decode('utf-8').strip().split('\n')
                abstract = ''
                titulo = ''
                golden = ''
                start = False
                for line in text:
                    if line.find('AB  -') != -1:
                        abstract = line
                    if line.find('ST  -') != -1:
                        titulo = line
                    # 'N1  -' or 'PY  -'
                    if line.find('KW  -') != -1:
                        start = True
                    if (line.find('PY  -') != -1) or (line.find('N1  -') != -1):  #or line.find('N1  -')
                        start = False
                    if start:
                        golden = golden + line
                doc.add(
                    Field("docid", (filename+'_'+str(docid)), StringField.TYPE_STORED)
                )
                docid += 1
                doc.add(
                    Field("abstract", abstract, tft)
                )
                doc.add(
                    Field("titulo", titulo, tft)
                )
                doc.add(
                    Field("key_words", golden, tft)
                )
                writer.addDocument(doc)
                writer.commit()

            # elimino del total, el documento indexado.
            docs = docs.replace(cadena,b"")
            docs = docs.replace(b"TY  ER  -",b"")
        file.close()

    def index(self, filepath, filepos, fileneg, typefile):
        """
        Indexador.

        Indexa un par de archivos, positivo y negativo. Respectivamente contienen documentos positivos y negativos.  
        Si el tipo de archivo es FVS o FDS, el analizador es EnglishAnalyzer, ademas usaremos TextField.TYPE_STORED a la hora de añadir un documento.  
        Si el tipo de archivo es TIS, el analizador es StandardAnalyzer y usaremos una instancia de FieldType para poder generar métricas.

        Args:
        ----------
        filepath : string
        >    Ruta donde se guardarán los nuevos archivos indexados.  

        filepos : File
        >    Archivo con los documentos positivos  

        fileneg : File
        >    Archivo con los documentos negativos  

        typefile : string
        >    Tipo de archivo a indexar, puede ser filesFVS, filesFDS o filesTIS

        Returns:
        -------
        string
            Mensaje, si todo ha ido bien: 'All indexing ok', si no se ejecuta correctamente 'something went wrong, exception in index method'

        """
        try:
            # cambiamos espacios por '_'en el nombre del archivo
            filenamepos = secure_filename(filepos.filename)
            filenameneg = secure_filename(fileneg.filename)
            # eliminamos del nombre la extensión del archivo, en nuestro caso ha de ser siempre .txt
            filenamepos = filenamepos[:(filenamepos.find(".txt"))]
            filenameneg = filenameneg[:(filenameneg.find(".txt"))]
            # Ruta donde se guardarán los nuevos archivos indexados
            pathpos = filepath+"/lucene_"+filenamepos
            pathneg = filepath+"/lucene_"+filenameneg
            # si los directorios no existen los creamos
            self.createDirectory(pathpos)
            self.createDirectory(pathneg)

            directorypos = SimpleFSDirectory(Paths.get(pathpos))
            directoryneg = SimpleFSDirectory(Paths.get(pathneg))

            if typefile == 'filesTIS':
                
                # creo una instancia de FieldType para establecer storeTermVector
                # proposito poder sacar las frecuencias.
                tft = FieldType()
                tft.setStored(True)
                tft.setTokenized(True)
                tft.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS_AND_OFFSETS)
                tft.setStoreTermVectors(True)
                tft.setStoreTermVectorPositions(True)
                tft.freeze()

                analyzer = StandardAnalyzer()
                config = IndexWriterConfig(analyzer)
                writer = IndexWriter(directorypos, config)
                self.addDocument(writer,filepos,filenamepos, tft) ########
                writer.close()

                analyzer = StandardAnalyzer()
                config = IndexWriterConfig(analyzer)
                writer = IndexWriter(directoryneg, config)
                self.addDocument(writer,fileneg,filenameneg, tft) ########
                writer.close()

            else: #los analizadores son EnglishAnalyzer, no hay tft.

                analyzer = EnglishAnalyzer()
                config = IndexWriterConfig(analyzer)
                writer = IndexWriter(directorypos, config)
                self.addDocument(writer,filepos,filenamepos, TextField.TYPE_STORED) ########
                writer.close()
                
                analyzer = EnglishAnalyzer()
                config = IndexWriterConfig(analyzer)
                writer = IndexWriter(directoryneg, config)
                self.addDocument(writer,fileneg,filenameneg, TextField.TYPE_STORED) ########
                writer.close()
         
            return 'All indexing ok'
        
        except:
            return 'something went wrong, exception in index method'

    def searchScore(self, filepath, word):
        """
        Search.

        Buscador en una ruta específica, el termino buscado debería estar en uno de los tres campos: abstract, titulo o key_words.

        Args:
        ----------
        filepath : string
        >    Ruta donde buscaremos.  

        word : string
        >    String que queremos buscar en los documentos.  

        Returns:
        -------
        dic 
        >    Diccionario tipo {documento: grado  de relevancia}

        """
        directory = SimpleFSDirectory(Paths.get(filepath))
        searcher = IndexSearcher(DirectoryReader.open(directory))
        analyzer = EnglishAnalyzer()
        
        # El termino buscado debería estar en uno de los tres campos: abstract, titulo o key_words
        SHOULD = BooleanClause.Occur.SHOULD
        query = MultiFieldQueryParser.parse(word, ["titulo","abstract","key_words"],
                                                [SHOULD, SHOULD, SHOULD],
                                                analyzer)
        
        scoreDocs = searcher.search(query, 1000).scoreDocs
        
        result = {}
        for sd in scoreDocs:
            d = searcher.doc(sd.doc)
            result[d.get("docid")] = sd.score
        
        return result

    def searchDocument(self, filepath, word):
        """
        Search.

        Buscador en una ruta específica, el termino buscado debería estar en uno de los tres campos: abstract, titulo o key_words.

        Args:
        ----------
        filepath : string
        >    Ruta donde buscaremos.  

        word : string
        >    String que queremos buscar en los documentos.  

        Returns:
        -------
        dic or list
        >    Lista de documentos con los atributos docid, abstract, titulo y key_words

        """
        directory = SimpleFSDirectory(Paths.get(filepath))
        searcher = IndexSearcher(DirectoryReader.open(directory))
        analyzer = EnglishAnalyzer()
        
        # El termino buscado debería estar en uno de los tres campos: abstract, titulo o key_words
        SHOULD = BooleanClause.Occur.SHOULD
        query = MultiFieldQueryParser.parse(word, ["titulo","abstract","key_words"],
                                                [SHOULD, SHOULD, SHOULD],
                                                analyzer)
        
        scoreDocs = searcher.search(query, 1000).scoreDocs
       
        result = []
        for sd in scoreDocs:
            d = searcher.doc(sd.doc)
            result.append({
                    "docid":  d.get("docid"),
                    "titulo":  d.get("titulo"),
                    "abstract": d.get("abstract"),
                    "key_words": d.get("key_words")
                })
        
        return result
    
    def positiveDocID(self, filepath):
        """
        Buscamos los identificares de los documentos.

        Buscamos los identificadores de los documentos para trec_eval, han de tener un peso, como los documentos positivos tienen todos la misma relevancia, será 10.

        Args:
        ----------
        filepath : string
        >    Ruta donde buscaremos.

        Returns:
        -------
        dic
        >    Diccionario tipo {documento: peso}, siendo el peso de 10.

        """
        store = SimpleFSDirectory(Paths.get(filepath))
        reader = None
        try:
            reader = DirectoryReader.open(store)
            term_enum = MultiTerms.getTerms(reader, "docid").iterator()
            
            docids = [term.utf8ToString()
                      for term in BytesRefIterator.cast_(term_enum)]
            print("docids")
            print(docids)

        finally:
            store.close()
        #diccionario = dict(enumerate(set(docids)))
        diccionario = {}
        for d in docids:
            diccionario[d] = 10
        print(diccionario)
        return diccionario


    def termsFreqsTIS(self, filepath):
        """
        Calcula la frecuencia de cada termino.

        Calcula la frecuencia de cada termino del archivo que se encuentra en la ruta especifica.  
        Como primeros parametros se añaden docCount (numero de documentos) y sumTotalTermFreq (suma total de la frecuencia de todos los terminos en los documentos)

        Args:
        ----------
        filepath : string
        >    Ruta donde se encuentran los archivos TIS.

        Returns:
        -------
        dic
        >    Devuelve un diccionario de tipo {termino: frecuencia}

        """
        store = SimpleFSDirectory(Paths.get(filepath))
        reader = None
        try:

            indexReader = DirectoryReader.open(NIOFSDirectory.open(Paths.get(filepath)))
            docCount = indexReader.numDocs()
            sumTotalTermFreq = 0
            # totalTermFreq, Devuelve el número total de apariciones de este término en todos los documentos (la suma de freq () para cada documento que tiene este término).
            # getSumTotalTermFreq, Devuelve la suma de totalTermFreq()todos los términos de este campo.
            sumTotalTermFreq += MultiTerms.getTerms(indexReader, "key_words").getSumTotalTermFreq()
            sumTotalTermFreq += MultiTerms.getTerms(indexReader, "abstract").getSumTotalTermFreq()
            sumTotalTermFreq += MultiTerms.getTerms(indexReader, "titulo").getSumTotalTermFreq()

            terms_freqs = {}
            terms_freqs['docCount'] = docCount
            terms_freqs['sumTotalTermFreq'] = sumTotalTermFreq

            for doc in range(docCount):
                termswat = []
                #vector de terminos
                termsk = indexReader.getTermVector(doc, "key_words")
                termsa = indexReader.getTermVector(doc, "abstract")
                termst = indexReader.getTermVector(doc, "titulo")
                if termsk is not None:
                    termswat.append(termsk) 
                elif termsa is not None:
                    termswat.append(termsa) 
                elif termst is not None:
                    termswat.append(termst) 

                for termss in termswat:
                    termsEnum = termss.iterator()
                    for term in BytesRefIterator.cast_(termsEnum):
                        # descartamos los números
                        if term.utf8ToString() != '©':
                            try: 
                                float(term.utf8ToString()) or int(term.utf8ToString())
                            except:
                                terms_freqs[term.utf8ToString()]=termsEnum.totalTermFreq()

                # quitamos palabras vacías
                stops = set(line.strip() for line in open('english_stopwords.txt'))
                for s in stops:
                    if s in terms_freqs:
                        del terms_freqs[s]
            
            '''print("terms_freqs")
            print(terms_freqs)

            # volver a inspeccionar docCount, hacerlo en un for      
            termssW = indexReader.getTermVector((docCount-1), "key_words")# NONE, antes tenia la restricción que si no había key_words, no guardaba el documento, ya no
            termssA = indexReader.getTermVector((docCount-1), "abstract")
            termssT = indexReader.getTermVector((docCount-1), "titulo")
            termssWAT = [termssW,termssA,termssT]
  
            terms_freqs2 = {}
            terms_freqs2['docCount'] = docCount
            terms_freqs2['sumTotalTermFreq'] = sumTotalTermFreq

            print("termssWAT")
            print(termssWAT)
            for termss in termssWAT:
                termsEnum = termss.iterator()
                for term in BytesRefIterator.cast_(termsEnum):
                    # descartamos los números
                    if term.utf8ToString() != '©':
                        try: 
                            float(term.utf8ToString()) or int(term.utf8ToString())
                        except:
                            terms_freqs2[term.utf8ToString()]=termsEnum.totalTermFreq() 

            # quitamos palabras vacías
            stops = set(line.strip() for line in open('english_stopwords.txt'))
            for s in stops:
                if s in terms_freqs2:
                    del terms_freqs2[s]
            print("terms_freqs2")
            print(terms_freqs2)'''
            
        finally:
            store.close()
        return terms_freqs