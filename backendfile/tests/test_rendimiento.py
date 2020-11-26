#!/usr/bin/env python
# coding: utf-8

import unittest
import json
import sys, os.path

dir_path = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))+ '/src/')
sys.path.append(dir_path)

from rendimiento import Rendimiento

class TestRendimiento(unittest.TestCase): 

    def test_medidas_de_rendimiento(self):
        qrels_file = {
            'q1': {
                'd1': 0,
                'd2': 1,
                'd3': 0,
            },
            'q2': {
                'd2': 1,
                'd3': 1,
            },
        }
        resultado = {
            'q1': {
                'd1': 1.0,
                'd2': 0.0,
                'd3': 1.5,
            },
            'q2': {
                'd1': 1.5,
                'd2': 0.2,
                'd3': 0.5,
            }
        }
        r = Rendimiento()

        self.assertEqual(r.medidas_de_rendimiento(qrels_file,resultado), {'num_q': 1.0, 
                                                                        'num_ret': 3.0, 
                                                                        'num_rel': 2.0, 
                                                                        'num_rel_ret': 2.0, 
                                                                        'map': 0.5833333333333333, 
                                                                        'gm_map': -0.5389965007326871, 
                                                                        'Rprec': 0.5, 
                                                                        'bpref': 1.0, 
                                                                        'recip_rank': 0.5, 
                                                                        'iprec_at_recall_0.00': 0.6666666666666666, 
                                                                        'iprec_at_recall_0.10': 0.6666666666666666, 
                                                                        'iprec_at_recall_0.20': 0.6666666666666666, 
                                                                        'iprec_at_recall_0.30': 0.6666666666666666, 
                                                                        'iprec_at_recall_0.40': 0.6666666666666666, 
                                                                        'iprec_at_recall_0.50': 0.6666666666666666, 
                                                                        'iprec_at_recall_0.60': 0.6666666666666666, 
                                                                        'iprec_at_recall_0.70': 0.6666666666666666, 
                                                                        'iprec_at_recall_0.80': 0.6666666666666666, 
                                                                        'iprec_at_recall_0.90': 0.6666666666666666, 
                                                                        'iprec_at_recall_1.00': 0.6666666666666666, 
                                                                        'P_5': 0.4, 
                                                                        'P_10': 0.2, 
                                                                        'P_15': 0.13333333333333333, 
                                                                        'P_20': 0.1, 
                                                                        'P_30': 0.06666666666666667, 
                                                                        'P_100': 0.02, 
                                                                        'P_200': 0.01, 
                                                                        'P_500': 0.004, 
                                                                        'P_1000': 0.002, 
                                                                        'relstring': 0.0, 
                                                                        'recall_5': 1.0, 
                                                                        'recall_10': 1.0, 
                                                                        'recall_15': 1.0, 
                                                                        'recall_20': 1.0, 
                                                                        'recall_30': 1.0, 
                                                                        'recall_100': 1.0, 
                                                                        'recall_200': 1.0, 
                                                                        'recall_500': 1.0, 
                                                                        'recall_1000': 1.0, 
                                                                        'infAP': 0.5833316666999994, 
                                                                        'gm_bpref': 0.0, 
                                                                        'Rprec_mult_0.20': 0.0, 
                                                                        'Rprec_mult_0.40': 0.0, 
                                                                        'Rprec_mult_0.60': 0.5, 
                                                                        'Rprec_mult_0.80': 0.5, 
                                                                        'Rprec_mult_1.00': 0.5, 
                                                                        'Rprec_mult_1.20': 0.6666666666666666, 
                                                                        'Rprec_mult_1.40': 0.6666666666666666, 
                                                                        'Rprec_mult_1.60': 0.5, 
                                                                        'Rprec_mult_1.80': 0.5, 
                                                                        'Rprec_mult_2.00': 0.5, 
                                                                        'utility': 1.0, 
                                                                        '11pt_avg': 0.6666666666666667, 
                                                                        'binG': 0.6309297535714575, 
                                                                        'G': 0.6309297535714575, 
                                                                        'ndcg': 0.6934264036172708, 
                                                                        'ndcg_rel': 0.5401396054259062, 
                                                                        'Rndcg': 0.38685280723454163, 
                                                                        'ndcg_cut_5': 0.6934264036172708, 
                                                                        'ndcg_cut_10': 0.6934264036172708, 
                                                                        'ndcg_cut_15': 0.6934264036172708, 
                                                                        'ndcg_cut_20': 0.6934264036172708, 
                                                                        'ndcg_cut_30': 0.6934264036172708, 
                                                                        'ndcg_cut_100': 0.6934264036172708, 
                                                                        'ndcg_cut_200': 0.6934264036172708, 
                                                                        'ndcg_cut_500': 0.6934264036172708, 
                                                                        'ndcg_cut_1000': 0.6934264036172708, 
                                                                        'map_cut_5': 0.5833333333333333, 
                                                                        'map_cut_10': 0.5833333333333333, 
                                                                        'map_cut_15': 0.5833333333333333, 
                                                                        'map_cut_20': 0.5833333333333333, 
                                                                        'map_cut_30': 0.5833333333333333, 
                                                                        'map_cut_100': 0.5833333333333333, 
                                                                        'map_cut_200': 0.5833333333333333, 
                                                                        'map_cut_500': 0.5833333333333333, 
                                                                        'map_cut_1000': 0.5833333333333333, 
                                                                        'relative_P_5': 1.0, 
                                                                        'relative_P_10': 1.0, 
                                                                        'relative_P_15': 1.0, 
                                                                        'relative_P_20': 1.0, 
                                                                        'relative_P_30': 1.0, 
                                                                        'relative_P_100': 1.0, 
                                                                        'relative_P_200': 1.0, 
                                                                        'relative_P_500': 1.0, 
                                                                        'relative_P_1000': 1.0, 
                                                                        'success_1': 0.0, 
                                                                        'success_5': 1.0, 
                                                                        'success_10': 1.0, 
                                                                        'set_P': 0.6666666666666666, 
                                                                        'set_relative_P': 1.0, 
                                                                        'set_recall': 1.0, 
                                                                        'set_map': 0.6666666666666666, 
                                                                        'set_F': 0.8, 
                                                                        'num_nonrel_judged_ret': 0.0},
                                                                     "error en medidas de rendimiento")


