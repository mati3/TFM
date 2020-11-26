#!/usr/bin/env python
# coding: utf-8

import unittest
import json
import sys, os.path

dir_path = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))+ '/src/')
sys.path.append(dir_path)

from filtros import Filtros

class TestFiltros(unittest.TestCase): 

    def test_Filtros(self):
        terms_freqs_positive = {
            'pneumonia': 3,
            'age': 2, 
            'autoimmune': 2,
            'biopsy': 1,
            'blood': 3, 
            'capacity': 2, 
            'classification': 4, 
            'cryptogenic': 2, 
            'ctd': 7, 
            'development': 2, 
            'diseases': 7, 
            'dlco': 3, 
            'docCount': 12, 
            'drug': 3, 
            'features': 2,
            'fibrosis': 4, 
            'follow': 3, 
            'group': 8, 
            'idiopathic': 4, 
            'iip': 9, 
            'imaging': 3, 
            'immunology': 4, 
            'interstitial': 4, 
            'ipaf': 13,  
            'mortality': 2,
            'myositis': 2, 
            'pathology': 3, 
            'patients': 4, 
            'reclassified': 2, 
            'sumTotalTermFreq': 4369, 
            'therapy': 3, 
            'undifferentiated': 4
        }
        terms_freqs_negative = { 
            'associated': 2,
            'based': 4, 
            'biomarker': 1,  
            'carcinoma': 3,  
            'compared': 2, 
            'conut': 13, 
            'diseases': 4, 
            'dna': 2, 
            'docCount': 7, 
            'failure': 3, 
            'group': 2,
            'hbv': 3, 
            'hcc': 4, 
            'hemorrhage': 3,  
            'hepatitis': 2, 
            'hepatocellular': 3, 
            'high': 2,
            'im': 5, 'immune': 2, 
            'immunology': 5, 
            'independent': 3, 
            'liver': 4,
            'lung': 4, 
            'mortality': 3, 
            'neoplasms': 3,
            'nomogram': 4,
            'pathology': 5, 
            'patients': 6,  
            'postoperative': 3, 
            'predict': 3, 
            'prognostic': 3, 
            'score': 8,
            'sumTotalTermFreq': 2188,
            'viral': 3
        }

        f = Filtros()

        self.assertEqual(f.filter("Freq",terms_freqs_positive, terms_freqs_negative, 5,"mati@correo.ugr.es"), ['ipaf', 'iip', 'ctd', 'classification', 'fibrosis'], " error en filtro frecuencia")
        self.assertEqual(f.filter("InfGain",terms_freqs_positive, terms_freqs_negative, 5,"mati@correo.ugr.es"), ['ipaf', 'iip', 'diseases', 'group', 'patients'], " error en filtro ganancia de información")
        self.assertEqual(f.filter("CrossEntropy",terms_freqs_positive, terms_freqs_negative, 5,"mati@correo.ugr.es"), ['biomarker', 'biopsy', 'associated', 'compared', 'dna'], "error en filtro entropía cruzada")
        self.assertEqual(f.filter("MutualInfo",terms_freqs_positive, terms_freqs_negative, 5,"mati@correo.ugr.es"), ['mortality', 'pathology', 'immunology', 'group', 'diseases'], "error en filtro información mutua")
        self.assertEqual(f.filter("OddsRatio",terms_freqs_positive, terms_freqs_negative, 5,"mati@correo.ugr.es"), ['group', 'pneumonia', 'age', 'autoimmune', 'biopsy'], "error en filtro odds ratio")
        self.assertEqual(f.filter("NormalSeparation",terms_freqs_positive, terms_freqs_negative, 5,"mati@correo.ugr.es"), ['ctd', 'diseases', 'group', 'iip', 'immunology'], "error en filtro normal separación")
        self.assertEqual(f.filter("Diferencia",terms_freqs_positive, terms_freqs_negative, 5,"mati@correo.ugr.es"), ['ipaf', 'iip', 'ctd', 'group', 'classification'], "error en filtro diferencia")
        self.assertEqual(f.filter("Filtro_no_existente",terms_freqs_positive, terms_freqs_negative, 5,"mati@correo.ugr.es"), "No existe el filtro seleccionado ", "error, el filtro no debería existir")