#   Trabajo Fin de Máster
#   Máster en Ingeniería Informática
#
#   2020 - Copyright (c) - GNU v3.0
#
#  Matilde Cabrera <mati331@correo.ugr.es>

import math
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
                dicResult[measure] = "{0:.4f}".format(value)
        
        return dicResult