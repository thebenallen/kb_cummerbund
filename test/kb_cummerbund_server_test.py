import unittest
import os
import json
import time

from os import environ
from ConfigParser import ConfigParser
from pprint import pprint

from biokbase.workspace.client import Workspace as workspaceService
from kb_cummerbund.kb_cummerbundImpl import kb_cummerbund


class kb_cummerbundTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        cls.ctx = {'token': token}
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('kb_cummerbund'):
            cls.cfg[nameval[0]] = nameval[1]
        cls.wsURL = cls.cfg['ws_url']
        cls.wsClient = workspaceService(cls.wsURL, token=token)
        cls.serviceImpl = kb_cummerbund(cls.cfg)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_kb_cummerbund_" + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    def test_your_method(self):
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(), 'objects': []})
        #
        #ws_id="pranjan77:1452551559640"
        #ws_obj_id="Ath_wt_hy5_cuffdiff"
        
        ws_id="pranjan77:1475698249756"
        ws_id="pranjan77:1481019426226"
        ws_id="pranjan77:1481237567854"
        c1 = 'wt'
        c2 = 'hy5'
        ws_obj_id="Ath_cuffdiff"
        ws_obj_id="wt-hy5-hisat2-cuffdiff"
        ws_obj_id="Poplar_hisat2_stringtie_6samples_cuffdiff"
        '''
        #ws_id = 'pranjan77:1473962459187'
        #c1 = 'ecoli_8083'
        #c2 = 'ecoli_8085'
        #ws_obj_id="test_3_samples_cuffdiff"
        ws_out_id="expx1"
        diffstat_out="expx12"

        #run get cummernund plot
        cummerbundParams={'workspace_name': ws_id, 'ws_cuffdiff_id': ws_obj_id, 'ws_cummerbund_output':ws_out_id, 'ws_diffstat_output': 'diffstat_out'}
        ret = self.getImpl().generate_cummerbund_plot2(self.getContext(), cummerbundParams)


        #run get expression matrix
        ws_out_id2="exp_out_obj_rep_ath_comma"
        expParams={'workspace_name': ws_id, 'ws_cuffdiff_id': ws_obj_id, 'ws_expression_matrix_id':ws_out_id2, 'include_replicates':1}
        #ret = self.getImpl().create_expression_matrix (self.getContext(), expParams)
        #x=1
        #y=1
        #self.assertEqual(x,y,1)
        ws_out_id3 = "exp3x"
        num_g = "5"
        interactiveHeatmapParams={
                'workspace_name': ws_id, 
                'ws_cuffdiff_id': ws_obj_id, 
                'ws_expression_matrix_id':ws_out_id3,
                'logMode': 'log2', 
                'removezeroes': 1,
                'condition_select':'all_pairs',
                'sample1':c1, 
                'sample2' :c2, 
                'q_value_cutoff':0.1,
                'log2_fold_change_cutoff': 1.2, 
                'num_genes' :num_g
                }
        interactiveHeatmapParams={
                'workspace_name': ws_id, 
                'ws_cuffdiff_id': ws_obj_id, 
                'ws_expression_matrix_id':ws_out_id3,
                'logMode': 'log2', 
                'removezeroes': 1,
                'condition_select':'all_pairs',
                'sample1':'ecoli_8083', 
                'sample2' :'ecoli_8085', 
                'q_value_cutoff':0.1,
                'log2_fold_change_cutoff': 1.2, 
                'num_genes' :num_g
                }
'''
        num_g=100
        ws_out_id3 = "expuuc"
        heatmapParams={
                'workspace_name': ws_id, 
                'ws_cuffdiff_id': ws_obj_id, 
                'ws_expression_matrix_id':ws_out_id3,
                'sample1':'Control', 
                'sample2' :'PD', 
                'q_value_cutoff':0.4,
                'log2_fold_change_cutoff': 1, 
                'num_genes' :num_g
                }


        ret = self.getImpl().create_interactive_heatmap_de_genes_old(self.getContext(), heatmapParams)
        #ret = self.getImpl().create_interactive_heatmap_de_genes(self.getContext(), interactiveHeatmapParams)
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods
        pass
