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


class Rendimiento():



    def medidas_de_rendimiento(self, qrels_file, resultado):
        """
        
        Medidas de rendimiento 

        Args:
        ----------
        qrels_file : dic
        >   Diccionario con la lista de documentos relevantes para cada consulta  
        
        resultado : dic
        >   Diccionario con la lista de documentos recuperados anteriormente

        Returns::
        -------
        dic
        >   Diccionario con las medidas de rendimiento de cada archivo positivo.
        
        """
        
        evaluator = pytrec_eval.RelevanceEvaluator(qrels_file, pytrec_eval.supported_measures)
        results = evaluator.evaluate(resultado)

        dicResult = {}
        for query_id, query_measures in results.items():
            for measure, value in query_measures.items():
                if measure == "runid":
                    continue
                if math.isnan(value):
                    value = 0
                dicResult[measure] = value
        
        return dicResult