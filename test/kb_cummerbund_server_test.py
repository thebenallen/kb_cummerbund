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

        #ws_id="pranjan77:1472587176942"
        #ws_obj_id="Ath_test_cuffdiff_validation"
        ws_id = 'pranjan77:1473962459187'
        ws_obj_id="test_3_samples_cuffdiff"


        ws_out_id="cummerbund_out_obj_ath"

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
        ws_out_id3 = "exp3"
        num_g = "100"
        interactiveHeatmapParams={'workspace_name': ws_id, 'ws_cuffdiff_id': ws_obj_id, 'ws_cummerbund_output':ws_out_id3, 'ws_expression_matrix_id':"abc",
                'sample1':'ecoli_8083', 'sample2' :'ecoli_8085', 'q_value_cutoff':0.5,  'log2_fold_change_cutoff': 1, 'num_genes' :num_g ,'include_replicates':1, 'condition_select':'selected_pair', 'removezeroes':1, 'logMode':2}
        ret = self.getImpl().create_interactive_heatmap_de_genes(self.getContext(), interactiveHeatmapParams)
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods
        pass
