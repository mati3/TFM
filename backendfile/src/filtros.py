#   Trabajo Fin de Máster
#   Máster en Ingeniería Informática
#
#   2020 - Copyright (c) - GNU v3.0
#
#  Matilde Cabrera <mati331@correo.ugr.es>

import math
import numpy as np, scipy.stats as st
from scipy.special import ndtri


class Filtros():


    def tabla_Term(self, resultadopos, resultadoneg):
        """
        Tabla de medidas necesarias de los terminos.
        
        Tabla de médidas para los terminos de un par de archivos, positivo y negativo, siendo:

        - F = término
        - P(F) = probabilidad[term] = freq_pos + freq_neg / sum_total_term_freq_pos_and_neg
        - P(Ci|F) = P(F,Ci) / P(F)
            - P(F,Cpos) = (freq_term_en_positivos/freq_term_pos+freq_term_neg) / P(F)
            - P(F,Cneg) =( freq_term_en_negativos/freq_term_pos+freq_term_neg) / P(F)

        - P(F|Ci) = P(Ci,F) / P(Ci)
            - P(F,Cpos) = (freq_term_en_positivos/freq_term_pos+freq_term_neg) / P(Cpos)
            - P(F,Cneg) = (freq_term_en_negativos/freq_term_pos+freq_term_neg) / P(Cneg)


        Args:
        ----------
        resultadopos : dic
        >    Diccionario de terminos: frecuencia de los documentos positivos  

        resultadoneg : dic
        >    Diccionario de terminos: frecuencia de los documentos negativos 

        Returns:
        -------
        dic
        >    Diccionario de termminos, por cada termino devuelve: P(F), P(Ci|F), P(F|Ci), sum_F (frecuencia total del termino, suma de positivos y negativos).

        """
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
        #print("tabla")
        #print(tabla)
        del tabla['sumTotalTermFreq']
        del tabla['docCount']
        return tabla

    def filterInfGain(self, resultadopos, resultadoneg, sum):
        """
        Filtro InfGain.

        Filtro ganancia de información.

        Args:
        ----------
        resultadopos : dic
        >    Diccionario termino:frecuencia de los documentos positivos  

        resultadoneg : dic
        >    Diccionario termino:frecuencia de los documentos negativos  

        sum : int
        >    Cantidad de terminos a devolver

        Returns:
        -------
        list
        >    lista de los mejores terminos encontrados con el filtro.

        """
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
        #print("InfGain")
        #print(InfGain)
        salida = sorted(InfGain, key=InfGain.get, reverse=True)
        #print('salida sorted')
        #print(salida)
        salida = salida[:int(sum)]
        return salida

    def filterCrossEntropy(self, resultadopos, resultadoneg, sum):
        """
        Filtro CrossEntropy.

        Args:
        ----------
        resultadopos : dic
        >    Diccionario termino:frecuencia de los documentos positivos  

        resultadoneg : dic
        >    Diccionario termino:frecuencia de los documentos negativos  

        sum : int
        >    Cantidad de terminos a devolver

        Returns:
        -------
        list
        >    lista de los mejores terminos encontrados con el filtro.

        """
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
        #print("CrossEntropy")
        #print(CrossEntropy)
        salida = sorted(CrossEntropy, key=CrossEntropy.get, reverse=True)
        #print('salida sorted')
        #print(salida)
        salida = salida[:int(sum)]
        return salida

    def filterMutualInfo(self, resultadopos, resultadoneg, sum):
        """
        Filtro MutualInfo.

        Args:
        ----------
        resultadopos : dic
        >    Diccionario termino:frecuencia de los documentos positivos  

        resultadoneg : dic
        >    Diccionario termino:frecuencia de los documentos negativos  

        sum : int
        >    Cantidad de terminos a devolver

        Returns:
        -------
        list
        >    lista de los mejores terminos encontrados con el filtro.

        """
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
        #print("mutualInfo")
        #print(mutualInfo)
        salida = sorted(mutualInfo, key=mutualInfo.get, reverse=True)
        #print('salida sorted')
        #print(salida)
        salida = salida[:int(sum)]
        return salida

    def filterfreq(self, resultadopos, resultadoneg, sum):
        """
        Filtro Frecuencias.

        Args:
        ----------
        resultadopos : dic
        >    Diccionario termino:frecuencia de los documentos positivos  

        resultadoneg : dic
        >    Diccionario termino:frecuencia de los documentos negativos  

        sum : int
        >    Cantidad de terminos a devolver

        Returns:
        -------
        list
        >    lista de los mejores terminos encontrados con el filtro.

        """
        totalTerms = resultadopos.copy()
        for k in resultadoneg:
            if k in resultadopos:
                del totalTerms[k]
        #print(totalTerms)
        salida = sorted(totalTerms, key=totalTerms.get, reverse=True)
        #print(salida)
        salida = salida[:int(sum)]
        return salida

    def filterOddsRatio(self, resultadopos, resultadoneg, sum):
        """
        Filtro Odds Ratio.

        Args:
        ----------
        resultadopos : dic
        >    Diccionario termino:frecuencia de los documentos positivos  

        resultadoneg : dic
        >    Diccionario termino:frecuencia de los documentos negativos  

        sum : int
        >    Cantidad de terminos a devolver

        Returns:
        -------
        list
        >    lista de los mejores terminos encontrados con el filtro.

        """
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
        #print("oddsRatio")
        #print(OddsRatio)
        salida = sorted(OddsRatio, key=OddsRatio.get, reverse=True)
        #print('salida sorted')
        #print(salida)
        salida = salida[:int(sum)]
        return salida

    def filterNormalSeparation(self, resultadopos, resultadoneg, sum):
        """
        Filtro Normal Separation.

        Args:
        ----------
        resultadopos : dic
        >    Diccionario termino:frecuencia de los documentos positivos  

        resultadoneg : dic
        >    Diccionario termino:frecuencia de los documentos negativos  

        sum : int
        >    Cantidad de terminos a devolver

        Returns:
        -------
        list
        >    lista de los mejores terminos encontrados con el filtro.

        """
        tabla = self.tabla_Term(resultadopos, resultadoneg)
        
        md = []
        for m in tabla:
            md.append(tabla[m]['sum_F'])
        
        distribucion_inversa = {}
        for d in tabla: 
            #distribucion_inversa[d] = st.norm.ppf(tabla[d]['sum_F'],loc = np.mean(md), scale = st.sem(md))
            distribucion = st.norm.cdf(tabla[d]['sum_F'],loc = np.mean(md), scale = st.sem(md))
            distribucion_inversa[d] = ndtri(distribucion)
        #print("distribucion_inversa")
        #print(distribucion_inversa)
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
        #print("NormalSeparation")
        #print(NormalSeparation)
        salida = sorted(NormalSeparation, key=NormalSeparation.get, reverse=True)
        #print('salida sorted')
        #print(salida)
        salida = salida[:int(sum)]
        return salida

    def filterDiferencia(self, resultadopos, resultadoneg, sum):
        """
        Filtro Diferencia.

        Args:
        ----------
        resultadopos : dic
        >    Diccionario termino:frecuencia de los documentos positivos  

        resultadoneg : dic
        >    Diccionario termino:frecuencia de los documentos negativos  

        sum : int
        >    Cantidad de terminos a devolver

        Returns:
        -------
        list
        >    lista de los mejores terminos encontrados con el filtro.

        """
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
        #print("Diferencia")
        #print(Diferencia)
        salida = sorted(Diferencia, key=Diferencia.get, reverse=True)
        #print('salida sorted')
        #print(salida)
        salida = salida[:int(sum)]
        return salida

    def filter(self, typefilter, terms_freqs_positive, terms_freqs_negative, sum, email):
        """
        Filtro.

        Ejecuta el tipo de filtro seleccionado.

        Args:
        ----------
        typefilter : string
        >    Tipo de filtro a ejecutar  

        terms_freqs_positive : dic
        >    Diccionario termino:frecuencia de los documentos positivos  

        terms_freqs_negative : dic
        >    Diccionario termino:frecuencia de los documentos negativos  

        sum : int
        >    Cantidad de terminos a devolver

        Returns:
        -------
        list or string
        >    lista de los mejores terminos encontrados con el filtro. En caso de no encontrar el filtro pasado devuelve mensaje de error.
        """
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