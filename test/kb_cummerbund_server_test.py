import unittest
import os
import json
import time
import shutil

from os import environ
from ConfigParser import ConfigParser
from pprint import pprint
from ReadsUtils.ReadsUtilsClient import ReadsUtils
from ReadsAlignmentUtils.ReadsAlignmentUtilsClient import ReadsAlignmentUtils
from GenomeFileUtil.GenomeFileUtilClient import GenomeFileUtil
from ExpressionUtils.ExpressionUtilsClient import ExpressionUtils
from biokbase.workspace.client import Workspace as workspaceService
from kb_cummerbund.kb_cummerbundImpl import kb_cummerbund
from DataFileUtil.DataFileUtilClient import DataFileUtil


class TestCummerbund(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        cls.ctx = {'token': token}
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('kb_cummerbund'):
            cls.cfg[nameval[0]] = nameval[1]
        cls.scratch = cls.cfg['scratch']
        cls.wsURL = cls.cfg['ws_url']
        cls.gfu = GenomeFileUtil(cls.callback_url)
        cls.ru = ReadsUtils(cls.callback_url)
        cls.rau = ReadsAlignmentUtils(cls.callback_url, service_ver='dev')
        cls.eu = ExpressionUtils(cls.callback_url, service_ver='dev')
        cls.wsClient = workspaceService(cls.wsURL, token=token)
        cls.dfu = DataFileUtil(cls.callback_url, token=token)
        cls.serviceImpl = kb_cummerbund(cls.cfg)
        cls.prepare_data()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.getWsName()})
            print('Test workspace was deleted')

    @classmethod
    def getWsClient(cls):
        return cls.wsClient

    @classmethod
    def getWsName(cls):
        if hasattr(cls, 'wsName'):
            return cls.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_kb_cummerbund_" + str(suffix)
        cls.ws_info = cls.getWsClient().create_workspace({'workspace': wsName})
        cls.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    @classmethod
    def prepare_data(cls):
        """
        Prepares a full sized DifferentialExpressionSet object with a downsized Athaliana Phytozome 
        genome for testing. This object is created from locally stored data that is uploaded for 
        the test. The other data objects (sampleset, alignmentset and expressionset) are dummy  
        objects that are created simply to set the required references and pass 
        workspace type validation. This was done to speed up the tests. The dummy objects
        do not affect the tests since the Cummerbund functions only use the 
        data in DifferentialExpressionSet object and not the data  in the referenced objects.
        
        :return: 
        """
        print('Preparing data...')
        target_dir = os.path.join(cls.scratch, 'tmp')
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)

        # create a dummy sampleset
        cls.condition_1 = 'test_condition_1'
        cls.condition_2 = 'test_condition_2'
        cls.condition_3 = 'test_condition_3'

        reads_file_name = 'Sample1.fastq'
        reads_file_path = os.path.join(target_dir, reads_file_name)
        shutil.copy(os.path.join('/kb/module/test/data', reads_file_name), reads_file_path)

        reads_object_name_1 = 'test_Reads_1'
        cls.reads_ref_1 = cls.ru.upload_reads({'fwd_file': reads_file_path,
                                               'wsname': cls.getWsName(),
                                               'sequencing_tech': 'Unknown',
                                               'interleaved': 0,
                                               'name': reads_object_name_1
                                               })['obj_ref']

        reads_object_name_2 = 'test_Reads_2'
        cls.reads_ref_2 = cls.ru.upload_reads({'fwd_file': reads_file_path,
                                               'wsname': cls.getWsName(),
                                               'sequencing_tech': 'Unknown',
                                               'interleaved': 0,
                                               'name': reads_object_name_2
                                               })['obj_ref']

        reads_object_name_3 = 'test_Reads_3'
        cls.reads_ref_3 = cls.ru.upload_reads({'fwd_file': reads_file_path,
                                               'wsname': cls.getWsName(),
                                               'sequencing_tech': 'Unknown',
                                               'interleaved': 0,
                                               'name': reads_object_name_3
                                               })['obj_ref']

        workspace_id = cls.dfu.ws_name_to_id(cls.getWsName())
        sample_set_object_name = 'test_sample_set'
        sample_set_data = {
            'sampleset_id': sample_set_object_name,
            'sampleset_desc': 'test sampleset object',
            'Library_type': 'SingleEnd',
            'condition': [cls.condition_1, cls.condition_2, cls.condition_3],
            'domain': 'Unknown',
            'num_samples': 3,
            'platform': 'Unknown'}
        save_object_params = {
            'id': workspace_id,
            'objects': [{
                'type': 'KBaseRNASeq.RNASeqSampleSet',
                'data': sample_set_data,
                'name': sample_set_object_name
            }]
        }

        dfu_oi = cls.dfu.save_objects(save_object_params)[0]
        cls.sample_set_ref = str(dfu_oi[6]) + '/' + str(dfu_oi[0]) + '/' + str(dfu_oi[4])

        # create a dummy genome object
        genbank_file_name = 'at_chrom1_section.gbk'
        genbank_file_path = os.path.join(target_dir, genbank_file_name)
        shutil.copy(os.path.join('/kb/module/test/data', genbank_file_name), genbank_file_path)

        genome_object_name = 'test_Genome'
        cls.genome_ref = cls.gfu.genbank_to_genome({'file': {'path': genbank_file_path},
                                                    'workspace_name': cls.getWsName(),
                                                    'genome_name': genome_object_name,
                                                    'generate_ids_if_needed': 1
                                                    })['genome_ref']

        # create a dummy alignment set object
        alignment_file_name = 'accepted_hits.bam'
        alignment_file_path = os.path.join(target_dir, alignment_file_name)
        shutil.copy(os.path.join('/kb/module/test/data', alignment_file_name), alignment_file_path)

        alignment_object_name_1 = 'test_Alignment_1'
        cls.alignment_ref_1 = cls.rau.upload_alignment(
            {'file_path': alignment_file_path,
             'destination_ref': cls.getWsName() + '/' + alignment_object_name_1,
             'read_library_ref': cls.reads_ref_1,
             'condition': cls.condition_1,
             'library_type': 'single_end',
             'assembly_or_genome_ref': cls.genome_ref
             })['obj_ref']

        alignment_object_name_2 = 'test_Alignment_2'
        cls.alignment_ref_2 = cls.rau.upload_alignment(
            {'file_path': alignment_file_path,
             'destination_ref': cls.getWsName() + '/' + alignment_object_name_2,
             'read_library_ref': cls.reads_ref_2,
             'condition': cls.condition_2,
             'library_type': 'single_end',
             'assembly_or_genome_ref': cls.genome_ref
             })['obj_ref']

        alignment_object_name_3 = 'test_Alignment_3'
        cls.alignment_ref_3 = cls.rau.upload_alignment(
            {'file_path': alignment_file_path,
             'destination_ref': cls.getWsName() + '/' + alignment_object_name_3,
             'read_library_ref': cls.reads_ref_3,
             'condition': cls.condition_3,
             'library_type': 'single_end',
             'assembly_or_genome_ref': cls.genome_ref,
             'library_type': 'single_end'
             })['obj_ref']

        object_type = 'KBaseRNASeq.RNASeqAlignmentSet'
        alignment_set_object_name = 'test_alignment_aet'
        alignment_set_data = {
            'genome_id': cls.genome_ref,
            'read_sample_ids': [reads_object_name_1,
                                reads_object_name_2,
                                reads_object_name_3],
            'mapped_rnaseq_alignments': [{reads_object_name_1: alignment_object_name_1},
                                         {reads_object_name_2: alignment_object_name_2},
                                         {reads_object_name_3: alignment_object_name_3}],
            'mapped_alignments_ids': [{reads_object_name_1: cls.alignment_ref_1},
                                      {reads_object_name_2: cls.alignment_ref_2},
                                      {reads_object_name_3: cls.alignment_ref_3}],
            'sample_alignments': [cls.alignment_ref_1,
                                  cls.alignment_ref_2,
                                  cls.alignment_ref_3],
            'sampleset_id': cls.sample_set_ref}
        save_object_params = {
            'id': workspace_id,
            'objects': [{
                'type': object_type,
                'data': alignment_set_data,
                'name': alignment_set_object_name
            }]
        }

        dfu_oi = cls.dfu.save_objects(save_object_params)[0]
        cls.rnaseq_alignment_set_ref = str(dfu_oi[6]) + '/' + str(dfu_oi[0]) + '/' + str(dfu_oi[4])

        # create a dummy expression set object
        source_dir = '/kb/module/test/data/sample_expression'
        new_source_dir = os.path.join(target_dir+'/expr')
        source_dir = shutil.copytree(source_dir, new_source_dir)

        expression_param_1 = {
            'destination_ref': cls.getWsName() + '/sample_expression_1',
            'source_dir': new_source_dir,
            'alignment_ref': cls.alignment_ref_1,
            'genome_ref': cls.genome_ref}
        cls.expression_ref_1 = cls.eu.upload_expression(expression_param_1)

        expression_param_2 = {
            'destination_ref': cls.getWsName() + '/sample_expression_2',
            'source_dir': new_source_dir,
            'alignment_ref': cls.alignment_ref_2,
            'genome_ref': cls.genome_ref}
        cls.expression_ref_2 = cls.eu.upload_expression(expression_param_2)

        expression_param_3 = {
            'destination_ref': cls.getWsName() + '/sample_expression_3',
            'source_dir': new_source_dir,
            'alignment_ref': cls.alignment_ref_3,
            'genome_ref': cls.genome_ref}
        cls.expression_ref_3 = cls.eu.upload_expression(expression_param_3)

        object_type = 'KBaseRNASeq.RNASeqExpressionSet'
        expression_set_object_name = 'test_expression_set'
        expression_set_data = {'alignmentSet_id': cls.rnaseq_alignment_set_ref,
            'genome_id': cls.genome_ref,
            'mapped_expression_ids': [{cls.alignment_ref_1: cls.expression_ref_1['obj_ref']},
                                      {cls.alignment_ref_2: cls.expression_ref_2['obj_ref']},
                                      {cls.alignment_ref_3: cls.expression_ref_3['obj_ref']}],
            'mapped_expression_objects': [{'alignment_object_name_1': 'sample_expression_1'},
                                           {'alignment_object_name_2': 'sample_expression_2'},
                                           {'alignment_object_name_3': 'sample_expression_3'}],
            'sample_expression_ids': [cls.expression_ref_1['obj_ref'],
                                      cls.expression_ref_2['obj_ref'],
                                      cls.expression_ref_3['obj_ref']],
            'sampleset_id': cls.sample_set_ref,
            'tool_opts': {'a_juncs': '10',
                           'ballgown_mode': '0',
                           'c_min_read_coverage': '2.5',
                           'disable_trimming': '0',
                           'gap_sep_value': '50',
                           'j_min_reads': '1',
                           'label': 'STRG',
                           'merge': '0',
                           'min_isoform_abundance': '0.1',
                           'min_length': '200',
                           'skip_reads_with_no_ref': '1'},
            'tool_used': 'StringTie',
            'tool_version': '1.2.3'}
        save_object_params = {
            'id': workspace_id,
            'objects': [{
                'type': object_type,
                'data': expression_set_data,
                'name': expression_set_object_name
            }]
        }

        dfu_oi = cls.dfu.save_objects(save_object_params)[0]
        cls.rnaseq_expression_set_ref = str(dfu_oi[6]) + '/' + str(dfu_oi[0]) + '/' + str(dfu_oi[4])

        # create a real differential expression object (this is the only object cummerbund uses)
        shutil.copy('/kb/module/test/data/Ath_sampleset_cuffdiff.zip', target_dir)
        handle = cls.dfu.file_to_shock(
            { "file_path": os.path.join(target_dir,
                                        'Ath_sampleset_cuffdiff.zip'),
              "make_handle" : True } )
        cls.obj_info = cls.wsClient.save_objects(
            {"workspace": cls.getWsName(),
             "objects": [{
                 "type": "KBaseRNASeq.RNASeqDifferentialExpression",
                 "data": {
                     'alignmentSet_id': cls.rnaseq_alignment_set_ref,
                     'condition': ['WT', 'hy5'],
                     'expressionSet_id': cls.rnaseq_expression_set_ref,
                     'file': handle['handle'],
                     'genome_id': cls.genome_ref,
                     'sampleset_id': cls.sample_set_ref,
                     'tool_used': 'Cuffdiff',
                     'tool_version': '1.2.3'},
                     'name': 'test_diff_exp_matrix'}
             ]})


    ## non-local inputs on production ##
    # ws_id = 'pranjan77:1486068164203'
    # ws_obj_id = 'wt-ycdr-cuffdiff'
    ## non-local inputs on CI ##
    # ws_id = 'pranjan77:1490326083513'
    # ws_obj_id = 'Ath_sampleset_cuffdiff'

    def test_generate_cummerbund_plots(self):
        output_obj_name = 'cummer'

        cummerbundParams = {
            'workspace_name': self.__class__.ws_info[1],
            'ws_cuffdiff_id': self.__class__.obj_info[0][1],
            'ws_cummerbund_output': output_obj_name,
        }

        print('running generate_cummerbund_plots with input: ')
        pprint(cummerbundParams)

        ret = self.getImpl().generate_cummerbund_plots(self.getContext(), cummerbundParams)

        print('output: ')
        pprint(ret)
        self.assertEquals(output_obj_name, ret[0])


    def test_generate_cummerbund_plot2(self):

        output_obj_name = 'cummer2'
        
        cummerbundParams = {
            'workspace': self.__class__.ws_info[1],
            'ws_cuffdiff_id': self.__class__.obj_info[0][1],
            'ws_cummerbund_output': output_obj_name,  
            'ws_diffstat_output': 'diffstat_out'
        }

        print('running generate_cummerbund_plot2 with input: ')
        pprint(cummerbundParams)

        ret = self.getImpl().generate_cummerbund_plot2(self.getContext(), cummerbundParams)
        
        print('output: ')
        pprint(ret)
        self.assertEquals(output_obj_name, ret[0])
    

    def test_create_expression_matrix(self):
        output_obj_name = 'exp_out_obj_rep_ath_comma'

        expression_matrix_params = {
            'workspace_name': self.__class__.ws_info[1],
            'ws_cuffdiff_id': self.__class__.obj_info[0][1],
            'ws_expression_matrix_id': output_obj_name,
            'include_replicates': 1
        }

        print('running create_expression_matrix with input: ')
        pprint(expression_matrix_params)

        ret = self.getImpl().create_expression_matrix(self.getContext(), expression_matrix_params)
        
        print('output: ')
        pprint(ret)
        self.assertEquals(output_obj_name, ret)


    def test_create_interactive_heatmap_de_genes_old(self):

        output_obj_name = "expuuc"
        heat_map_params = {
            'workspace': self.__class__.ws_info[1],
            'ws_cuffdiff_id': self.__class__.obj_info[0][1],
            'ws_expression_matrix_id': output_obj_name,
            'sample1': 'WT',
            'sample2': 'ydcR',
            'q_value_cutoff': 1,
            'log2_fold_change_cutoff': 1.5,
            'num_genes': 1000
        }

        print('running create_interactive_heatmap_de_genes_old with input: ')
        pprint(heat_map_params)

        ret = self.getImpl().create_interactive_heatmap_de_genes_old(self.getContext(), heat_map_params)

        print('output: ')
        pprint(ret)
        self.assertTrue('report_name' in ret[0])
        self.assertTrue('report_ref' in ret[0])
    

    def test_create_interactive_heatmap_de_genes(self):
        output_obj_name = "exp3x"
        interactive_heat_map_params = {
            'workspace_name': self.__class__.ws_info[1],
            'ws_cuffdiff_id': self.__class__.obj_info[0][1],
            'ws_expression_matrix_id': output_obj_name,
            'logMode': 'log2',
            'removezeroes': 1,
            'condition_select': 'all_pairs',
            'sample1': 'ecoli_8083',
            'sample2': 'ecoli_8085',
            'q_value_cutoff': 0.1,
            'log2_fold_change_cutoff': 1.2,
            'num_genes': 1000
        }

        print('running create_interactive_heatmap_de_genes with input: ')
        pprint(interactive_heat_map_params)

        ret = self.getImpl().create_interactive_heatmap_de_genes(self.getContext(),
                                                                 interactive_heat_map_params)
        print('output: ')
        pprint(ret)





#start the tests if run as a script
if __name__ == '__main__':
    unittest.main()