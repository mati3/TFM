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
        try: 
            os.stat(myfolder)
        except:
            os.mkdir(myfolder)

    def addDocument(self, writer, file, filename, tft):
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
        filenamepos = secure_filename(filepos.filename)
        filenamepos = filenamepos[:(filenamepos.find(".txt"))]
        filenameneg = secure_filename(fileneg.filename)
        filenameneg = filenameneg[:(filenameneg.find(".txt"))]

        pathpos = filepath+"/lucene_"+filenamepos
        pathneg = filepath+"/lucene_"+filenameneg

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

        else: #los analizadores son EnglishAnalyzer no hay tft.

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

        return 'files upload ok'

    def search(self, filepath, word, score):
        directory = SimpleFSDirectory(Paths.get(filepath))
        searcher = IndexSearcher(DirectoryReader.open(directory))
        analyzer = EnglishAnalyzer()
        
        # El termino buscado debería estar en uno de los tres campos: abstract, titulo o key_words
        SHOULD = BooleanClause.Occur.SHOULD
        query = MultiFieldQueryParser.parse(word, ["titulo","abstract","key_words"],
                                                [SHOULD, SHOULD, SHOULD],
                                                analyzer)
        
        scoreDocs = searcher.search(query, 1000).scoreDocs
        if score:
            result = {}
            for sd in scoreDocs:
                d = searcher.doc(sd.doc)
                result[d.get("docid")] = sd.score
        else:
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
    
    def searchDocID(self, filepath):
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
            diccionario[d] = 10.0
        print(diccionario)
        return diccionario


    def selectTIS(self, filepath):
        store = SimpleFSDirectory(Paths.get(filepath))
        reader = None
        try:
            reader = DirectoryReader.open(store)
            term_enum = MultiTerms.getTerms(reader, "docid").iterator()
            
            docids = [term.utf8ToString()
                      for term in BytesRefIterator.cast_(term_enum)]
            print("docids")
            print(docids)

            indexReader = DirectoryReader.open(NIOFSDirectory.open(Paths.get(filepath)))
            docCount = indexReader.numDocs()
            # volver a inspeccionar docCount, hacerlo en un for      
            termssW = indexReader.getTermVector((docCount-1), "key_words")# NONE, antes tenia la restricción que si no había key_words, no guardaba el documento, ya no
            termssA = indexReader.getTermVector((docCount-1), "abstract")
            termssT = indexReader.getTermVector((docCount-1), "titulo")
            termssWAT = [termssW,termssA,termssT]
  
            sumTotalTermFreq = 0
            # totalTermFreq, Devuelve el número total de apariciones de este término en todos los documentos (la suma de freq () para cada documento que tiene este término).
            # getSumTotalTermFreq, Devuelve la suma de totalTermFreq()todos los términos de este campo.
            sumTotalTermFreq += MultiTerms.getTerms(reader, "key_words").getSumTotalTermFreq()
            sumTotalTermFreq += MultiTerms.getTerms(reader, "abstract").getSumTotalTermFreq()
            sumTotalTermFreq += MultiTerms.getTerms(reader, "titulo").getSumTotalTermFreq()

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
            print(terms_freqs2)
            
        finally:
            store.close()
        return terms_freqs2
    
    def tabla_Term(self, resultadopos, resultadoneg):
        sumTotalTermFreq = resultadopos['sumTotalTermFreq'] + resultadoneg['sumTotalTermFreq']
        p_Cpos = resultadopos['docCount']/(resultadopos['docCount']+resultadoneg['docCount'])
        p_Cneg = resultadoneg['docCount']/(resultadoneg['docCount']+resultadopos['docCount'])

        prob = {}
        # ya tenemos los positivos
        totalTerm = resultadopos.copy()
        # incluimos los negativos, obtengo el vector de todos los terminos y su frecuencia.
        for k in resultadoneg:
            if k in resultadopos:
                totalTerm[k] = resultadopos[k] + resultadoneg[k]
            else:
                totalTerm[k] = resultadoneg[k]

        p_Cpos_F = {}
        p_Cneg_F = {}
        p_F_Cpos = {}
        p_F_Cneg = {}
        tabla = {}
        for k in totalTerm:
            prob[k] = totalTerm[k]/sumTotalTermFreq
            if k in resultadopos:
                p_Cpos_F[k] = (resultadopos[k]/totalTerm[k])/prob[k]
                p_F_Cpos[k] = (resultadopos[k]/totalTerm[k])/p_Cpos
            else: 
                p_Cpos_F[k] = 0
                p_F_Cpos[k] = 0
            if k in resultadoneg:
                p_Cneg_F[k] = (resultadoneg[k]/totalTerm[k])/prob[k]
                p_F_Cneg[k] = (resultadoneg[k]/totalTerm[k])/p_Cneg
            else: 
                p_Cneg_F[k] = 0
                p_F_Cneg[k] = 0
            tabla[k] = {'prob': prob[k], 'p_Cpos_F': p_Cpos_F[k], 'p_Cneg_F':  p_Cneg_F[k], 'p_F_Cpos': p_F_Cpos[k], 'p_F_Cneg':  p_F_Cneg[k], 'sum_F': totalTerm[k]}
        print("tabla")
        print(tabla)
        del tabla['sumTotalTermFreq']
        del tabla['docCount']
        return tabla

    def filterInfGain(self, resultadopos, resultadoneg, sum):
        p_Cpos = resultadopos['docCount']/(resultadopos['docCount']+resultadoneg['docCount'])
        p_Cneg = resultadoneg['docCount']/(resultadoneg['docCount']+resultadopos['docCount'])

        tabla = self.tabla_Term(resultadopos, resultadoneg)
        InfGain = {}
        for f in tabla:
            p_F = tabla[f]['prob']# P(F) 
            not_p_F = 1 - tabla[f]['prob']# P(F⁻)
            p_Cpos_F = tabla[f]['p_Cpos_F'] # P(Ci|F)
            if f in resultadoneg: 
                not_p_Cpos_F = resultadoneg[f]/not_p_F # P(Ci|F⁻)
                not_logpos = math.log(not_p_Cpos_F/p_Cpos)
            else: 
                not_p_Cpos_F = 0
                not_logpos = 0
            p_Cneg_F = tabla[f]['p_Cneg_F'] # P(Ci|F)
            if f in resultadopos: 
                not_p_Cneg_F = resultadopos[f]/not_p_F # P(Ci|F⁻)
                not_logneg = math.log(not_p_Cneg_F/p_Cneg)
            else: 
                not_p_Cneg_F = 0
                not_logpos = 0
            # error cuando p_Cneg_F es 0
            if p_Cpos_F==0: logpos=0
            else: logpos = math.log(p_Cpos_F/p_Cpos)
            if p_Cneg_F==0:logneg = 0
            else: logneg = math.log(p_Cneg_F/p_Cneg)

            sumatoria = (p_Cpos_F * logpos) + (p_Cneg_F * logneg)
            not_sumatoria = (not_p_Cpos_F * not_logpos) + (not_p_Cneg_F * not_logneg)
            InfGain[f]= (p_F * sumatoria)+(not_p_F * not_sumatoria)
        print("InfGain")
        print(InfGain)
        salida = sorted(InfGain, key=InfGain.get, reverse=True)
        print('salida sorted')
        print(salida)
        salida = salida[:int(sum)]
        return salida

    def filterCrossEntropy(self, resultadopos, resultadoneg, sum):
        p_Cpos = resultadopos['docCount']/(resultadopos['docCount']+resultadoneg['docCount'])
        p_Cneg = resultadoneg['docCount']/(resultadoneg['docCount']+resultadopos['docCount'])

        tabla = self.tabla_Term(resultadopos, resultadoneg)
        CrossEntropy = {}
        for f in tabla:
            p_F = tabla[f]['prob'] # P(F)
            p_Cpos_F = tabla[f]['p_Cpos_F'] # P(Ci|F)
            p_Cneg_F = tabla[f]['p_Cneg_F'] # P(Ci|F)
            # error cuando p_Cneg_F es 0
            if p_Cpos_F==0: logpos=0
            else: logpos = math.log(p_Cpos_F/p_Cpos)
            if p_Cneg_F==0:logneg = 0
            else: logneg = math.log(p_Cneg_F/p_Cneg)
            CrossEntropy[f]=p_F*( (p_Cpos_F*logpos)+(p_Cneg_F*logneg) )
        print("CrossEntropy")
        print(CrossEntropy)
        salida = sorted(CrossEntropy, key=CrossEntropy.get, reverse=True)
        print('salida sorted')
        print(salida)
        salida = salida[:int(sum)]
        return salida

    def filterMutualInfo(self, resultadopos, resultadoneg, sum):
        # prob de ci, la probabilidad de una clase, es el numero de documentos de esa clase entre el total de documentos.
        p_Cpos = resultadopos['docCount']/(resultadopos['docCount']+resultadoneg['docCount'])
        p_Cneg = resultadoneg['docCount']/(resultadoneg['docCount']+resultadopos['docCount'])

        tabla = self.tabla_Term(resultadopos, resultadoneg)
        mutualInfo = {}
        for f in tabla:
            p_F = tabla[f]['prob'] # P(F)
            p_F_Cpos = tabla[f]['p_F_Cpos'] # P(F|Ci)
            p_F_Cneg =  tabla[f]['p_F_Cneg'] # P(F|Ci)
            # error cuando p_Cneg_F es 0
            if p_F_Cpos==0: logpos=0
            else: logpos = math.log(p_F_Cpos/p_F)
            if p_F_Cneg==0:logneg = 0
            else: logneg = math.log(p_F_Cneg/p_F)
            mutualInfo[f]=(p_Cpos*logpos)+(p_Cneg*logneg)
        print("mutualInfo")
        print(mutualInfo)
        salida = sorted(mutualInfo, key=mutualInfo.get, reverse=True)
        print('salida sorted')
        print(salida)
        salida = salida[:int(sum)]
        return salida

    def filterfreq(self, resultadopos, resultadoneg, sum):
        totalTerms = resultadopos.copy()
        for k in resultadoneg:
            if k in resultadopos:
                del totalTerms[k]
        print(totalTerms)
        salida = sorted(totalTerms, key=totalTerms.get, reverse=True)
        print(salida)
        salida = salida[:int(sum)]
        return salida

    def filterOddsRatio(self, resultadopos, resultadoneg, sum):
        
        tabla = self.tabla_Term(resultadopos, resultadoneg)
        OddsRatio = {}
        for f in tabla:
            # P(F|pos) = is the conditional probability of feature F occurring given the class value ‘positive’
            # numero de veces que aparece un termino en el positivo entre el totalterminofrecuencia de los positivos
            if f in resultadopos:
                condProbFpos = resultadopos[f]/resultadopos['sumTotalTermFreq']
            else:
                condProbFpos = 0
            if f in resultadoneg:
                condProbFneg = resultadoneg[f]/resultadoneg['sumTotalTermFreq']
            else:
                condProbFneg = 0
            # si condProbFneg es 0, es decir, el termino no existe en negativos, no se puede calcular oddratio
            if (condProbFpos==0) or (condProbFneg==0):
                OddsRatio[f] = 0
            else:
                OddsRatio[f]=math.log((condProbFpos*(1-condProbFneg))/((1-condProbFpos)*condProbFneg))
        print("mutualInfo")
        print(OddsRatio)
        salida = sorted(OddsRatio, key=OddsRatio.get, reverse=True)
        print('salida sorted')
        print(salida)
        salida = salida[:int(sum)]
        return salida

    def filterNormalSeparation(self, resultadopos, resultadoneg, sum):
       
        tabla = self.tabla_Term(resultadopos, resultadoneg)
        
        md = []
        for m in tabla:
            md.append(tabla[m]['sum_F'])
        
        distribucion_inversa = {}
        for d in tabla: 
            #distribucion_inversa[d] = st.norm.ppf(tabla[d]['sum_F'],loc = np.mean(md), scale = st.sem(md))
            distribucion = st.norm.cdf(tabla[d]['sum_F'],loc = np.mean(md), scale = st.sem(md))
            distribucion_inversa[d] = ndtri(distribucion)
        print("distribucion_inversa")
        print(distribucion_inversa)
        NormalSeparation = {}
        for f in tabla:
            if f in resultadopos:
                condProbFpos = resultadopos[f]/resultadopos['sumTotalTermFreq']
            else:
                condProbFpos = 0
            if f in resultadoneg:
                condProbFneg = resultadoneg[f]/resultadoneg['sumTotalTermFreq']
            else:
                condProbFneg = 0
            NormalSeparation[f]=(distribucion_inversa[f]*condProbFpos)-(distribucion_inversa[f]*condProbFneg)
        print("NormalSeparation")
        print(NormalSeparation)
        salida = sorted(NormalSeparation, key=NormalSeparation.get, reverse=True)
        print('salida sorted')
        print(salida)
        salida = salida[:int(sum)]
        return salida

    def filterDiferencia(self, resultadopos, resultadoneg, sum):
        tabla = self.tabla_Term(resultadopos, resultadoneg)

        # el peso de termino es mejor que otro si aparece muchas veces en los positivos y no aparece en los negativos
        Diferencia = {}
        for f in tabla:
            if f in resultadopos:
                #nº veces clase positiva / nº total termino en la clase positiva
                Pesopos = resultadopos[f]/resultadopos['sumTotalTermFreq']
            else:
                Pesopos = 0
            if f in resultadoneg:
                Pesoneg = resultadoneg[f]/resultadoneg['sumTotalTermFreq']
            else:
                Pesoneg = 0
            #resto negativo al positivo.
            Diferencia[f] = Pesopos - Pesoneg
        print("Diferencia")
        print(Diferencia)
        salida = sorted(Diferencia, key=Diferencia.get, reverse=True)
        print('salida sorted')
        print(salida)
        salida = salida[:int(sum)]
        return salida

    def filter(self, typefilter, terms_freqs_positive, terms_freqs_negative, sum, email):
        if typefilter == "Freq":
            return self.filterfreq(terms_freqs_positive,terms_freqs_negative, sum)
        elif typefilter == "InfGain":
            return self.filterInfGain(terms_freqs_positive,terms_freqs_negative, sum)
        elif typefilter == "CrossEntropy":
            return self.filterCrossEntropy(terms_freqs_positive,terms_freqs_negative, sum)
        elif typefilter == "MutualInfo":
            return self.filterMutualInfo(terms_freqs_positive,terms_freqs_negative, sum)
        elif typefilter == "OddsRatio":
            return self.filterOddsRatio(terms_freqs_positive,terms_freqs_negative, sum)
        elif typefilter == "NormalSeparation":
            return self.filterNormalSeparation(terms_freqs_positive,terms_freqs_negative, sum)
        elif typefilter == "Diferencia":
            return self.filterDiferencia(terms_freqs_positive,terms_freqs_negative, sum)
        else:
            return "No existe el filtro seleccionado "

    def medidas_de_rendimiento(self, setAllFVSPos, resultado):
        print("setAllFVSPos")
        print(setAllFVSPos)
        print("resultado")
        print(resultado)
        qrels_file = setAllFVSPos
        results_file = resultado
        evaluator = pytrec_eval.RelevanceEvaluator(qrels_file, {'map', 'ndcg'})

        print(json.dumps(evaluator.evaluate(results_file), indent=1))
        
        return "tengo que recoger precisión, recall y f1"        

# qrel_file : ruta del archivo con la lista de documentos relevantes para cada consulta
# results_file : ruta del archivo con la lista de documentos recuperados por su aplicación