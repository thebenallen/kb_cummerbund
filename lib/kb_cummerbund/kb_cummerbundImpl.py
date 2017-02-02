# -*- coding: utf-8 -*-
#BEGIN_HEADER
import simplejson
import sys
import os
import ast
import glob
import uuid
import json
import logging
import time
import subprocess
from pprint import pprint,pformat
import threading, traceback
from collections import OrderedDict
from pprint import pprint
import script_util
import script_util2
from biokbase.workspace.client import Workspace
from biokbase.auth import Token
from os.path import isfile, join, exists
import volcano_plot_data_parse_and_upload as v
try:
    from biokbase.HandleService.Client import HandleService
except:
    from biokbase.AbstractHandle.Client import AbstractHandle as HandleService

import kb_cummerbundutils
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

from GenomeAnnotationAPI.GenomeAnnotationAPIClient import GenomeAnnotationAPI




class kb_cummerbundException(BaseException):
    def __init__(self, msg):
        self.msg = msg
        def __str__(self):
            return repr(self.msg)



#END_HEADER


class kb_cummerbund:
    '''
    Module Name:
    kb_cummerbund

    Module Description:
    A KBase module: kb_cummerbund
    '''

    ######## WARNING FOR GEVENT USERS #######
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    #########################################
    VERSION = "0.0.7"
    GIT_URL = "git@github.com:kbaseapps/kb_cummerbund.git"
    GIT_COMMIT_HASH = "e25c9e0197a8471aa47c5e817a825ff11b56dd82"
    
    #BEGIN_CLASS_HEADER
    __TEMP_DIR = 'temp'
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR

        self.callbackURL = os.environ.get('SDK_CALLBACK_URL')
        if self.callbackURL == None:
                            raise ValueError ("SDK_CALLBACK_URL not set in environment")


        if 'ws_url' in config:
            self.__WS_URL = config['ws_url']
        if 'shock_url' in config:
            self.__SHOCK_URL = config['shock_url']
        if 'hs_url' in config:
            self.__HS_URL = config['hs_url']
        if 'scratch' in config:
            self.__SCRATCH = config['scratch']
        if 'rscripts' in config:
            self.__RSCRIPTS = config['rscripts']


        #logging
        self.__LOGGER = logging.getLogger('kb_cummerbund')
        if 'log_level' in config:
            self.__LOGGER.setLevel(config['log_level'])
        else:
            self.__LOGGER.setLevel(logging.INFO)
        streamHandler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("%(asctime)s - %(filename)s - %(lineno)d - %(levelname)s - %(message)s")
        formatter.converter = time.gmtime
        streamHandler.setFormatter(formatter)
        self.__LOGGER.addHandler(streamHandler)
        self.__LOGGER.info("Logger was set")

        #END_CONSTRUCTOR
        pass
    

    def generate_cummerbund_plots(self, ctx, cummerbundParams):
        """
        :param cummerbundParams: instance of type "cummerbundParams" ->
           structure: parameter "workspace_name" of type "workspace_name"
           (workspace name of the object), parameter "ws_cuffdiff_id" of type
           "ws_cuffdiff_id" (@id ws
           KBaseRNASeq.RNASeqCuffdiffdifferentialExpression), parameter
           "ws_cummerbund_output" of type "ws_cummerbund_output" (@id ws
           KBaseRNASeq.cummerbund_output)
        :returns: instance of type "ws_cummerbund_output" (@id ws
           KBaseRNASeq.cummerbund_output)
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN generate_cummerbund_plots

        params    = cummerbundParams
        returnVal = params['ws_cummerbund_output']

        #Set up workspace client
        user_token = ctx['token']
        ws_client  = Workspace(url=self.__WS_URL, token=user_token)

        #Read the input cuffdiff workspace object json file and get filehandle for cuffdiff tar file
        s_res = ws_client.get_objects([{
            'name' : params['ws_cuffdiff_id'],
            'workspace' : params['workspace_name']
            }])

        # Check if workspace has data
        if len(s_res) == 0:
            self.__LOGGER.info("Workspace did not return any objects")
            return returnVal

        cuffdiff_dir = script_util2.extract_cuffdiff_data (self.__LOGGER, self.__SHOCK_URL, self.__SCRATCH, s_res, user_token)
        self.__LOGGER.info("Cuffdiff folder = " + cuffdiff_dir)

        if (cuffdiff_dir is False):
            return returnVal

        # Run R script to run cummerbund json and update the cummerbund output json file
        # Prepare output object.
        outputobject=dict()

        # Prepare output plot list
        cummerbundplotset=[]

        # List of plots to generate
        plotlist = [
                { 'file': "dispersionplot.R",
                  'title': "Dispersion plot",
                  'description': "Dispersion plot is the quality measure of the data. It estimates deviation from threshold against counts in FPKM." },


                { 'file': "fpkmscvplot.R",
                  'title': "Genes CV plot",
                  'description': "The squared coefficient of variation plot is a normalized measure of cross-replicate variability that can be useful for evaluating the quality of RNA-seq data." },

                { 'file': "isoformscvplot.R",
                  'title': "Isoform CV plot",
                  'description': "The squared coefficient of variation plot is a normalized measure of cross-replicate variability that can be useful for evaluating the quality of RNA-seq data.Differences in CV2 can result in lower numbers of differentially expressed isoforms due to a higher degree of variability between replicate fpkm estimates." },

                { 'file': "densityplot.R",
                  'title': "Density plot",
                  'description': "The density plot shows the distribution of FPKM scores across samples" },

                { 'file': "csdensityrepplot.R",
                  'title': "Replicates density plot",
                  'description': "The replicates density plot shows the distribution of FPKM scores across sample replicates" },

                { 'file': "boxplot.R",
                  'title': "Box plots",
                  'description': "The box plots show the FPKM distribution across samples." },

                { 'file': "boxrepplot.R",
                  'title': "Box plots of replicates",
                  'description': "The box plots of replicates show the FPKM distribution across sample replicates." },

                { 'file': "pairwisescatterplots.R",
                  'title': "Pairwise scatter plots",
                  'description': "The scatterplots show differences in gene expression between two samples. If two samples are identical, all genes will fall on the mid-line." },

                 { 'file': "volcanomatrixplot.R",
                  'title': "Volcano matrix plots",
                  'description': "Volcano matrix plot is a scatter plot that also identifies differentially expressed genes (by color) between samples based on log2 fold change cut off." },

                { 'file': "pcaplot.R",
                  'title': "PCA plot",
                  'description': "Principal Component Analysis (PCA) is an informative approach for dimensionality reduction for exploring teh relationship between sample conditions." },

                { 'file': "pcarepplot.R",
                  'title': "PCA plot including replicates",
                  'description': "Principal Component Analysis (PCA) is an informative approach for dimensionality reduction for exploring teh relationship between sample conditions including replicates." },

                { 'file': "mdsplot.R",
                  'title': "Multi-dimensional scaling plot",
                  'description': "Multi-dimensional scaling plots are similar to PCA plots and useful for determining the major sources of variation in the dataset. " },

                { 'file': "mdsrepplot.R",
                  'title': "Multi-dimensional scaling plot including replicates",
                  'description': "Multi-dimensional scaling plot including replicates are  similar to PCA plots and useful for determining the major sources of variation in the dataset with replicates. These can be useful to determine any systematic bias that may be present between conditions." }
            ]

#TODO.. Giving Rplot.pdf
#                { 'file': "dendrogramplot.R",
#                  'title': "Dendrogram",
#                  'description': "Dendrogram  based on the JS (Jensen-Shannon divergence) distance" },
#
#                { 'file': "dendrogramrepplot.R",
#                  'title': "Dendrogram including replicates",
#                  'description': "Dendrogram including replicates based on the JS (Jensen-Shannon divergence) distance" },


        # Iterate through the plotlist and generate the images and json files.
        for plot in plotlist:
            status = script_util2.rplotandupload(self.__LOGGER, self.__SCRATCH, self.__RSCRIPTS,
                plot['file'], self.__SHOCK_URL, self.__HS_URL, user_token,
                cummerbundplotset, plot['title'], plot['description'], cuffdiff_dir)
            if status == False:
                self.__LOGGER.info("Problem generating image and json file - " + plot["file"])


        # Populate the output object
        outputobject['cummerbundplotSet'] = cummerbundplotset

        #TODO: Need to figure out how to get rnaseq experiment id
        outputobject['rnaseq_experiment_id'] = "rnaseq_experiment_id"
        outputobject['cuffdiff_input_id'] = params['ws_cuffdiff_id']

        res = ws_client.save_objects({
            "workspace":params['workspace_name'],
            "objects": [{
                "type":"KBaseRNASeq.cummerbund_output",
                "data":outputobject,
                "name":params["ws_cummerbund_output"]}]
            })

               

        #END generate_cummerbund_plots

        # At some point might do deeper type checking...
        if not isinstance(returnVal, basestring):
            raise ValueError('Method generate_cummerbund_plots return value ' +
                             'returnVal is not type basestring as required.')
        # return the results
        return [returnVal]

    def generate_cummerbund_plot2(self, ctx, cummerbundstatParams):
        """
        :param cummerbundstatParams: instance of type "cummerbundstatParams"
           -> structure: parameter "workspace_name" of type "workspace_name"
           (workspace name of the object), parameter "ws_cuffdiff_id" of type
           "ws_cuffdiff_id" (@id ws
           KBaseRNASeq.RNASeqCuffdiffdifferentialExpression), parameter
           "ws_cummerbund_output" of type "ws_cummerbund_output" (@id ws
           KBaseRNASeq.cummerbund_output), parameter "ws_diffstat_output" of
           type "ws_diffstat_output" (Differential stat workspace id)
        :returns: instance of type "ws_cummerbund_output" (@id ws
           KBaseRNASeq.cummerbund_output)
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN generate_cummerbund_plot2
        params    = cummerbundstatParams
        returnVal = params['ws_cummerbund_output']

        #Set up workspace client
        user_token = ctx['token']
        ws_client  = Workspace(url=self.__WS_URL, token=user_token)


        #Read the input cuffdiff workspace object json file and get filehandle for cuffdiff tar file
        s_res = ws_client.get_objects([{
            'name' : params['ws_cuffdiff_id'],
            'workspace' : params['workspace_name']
            }])
        print "Getting genome info"

        genome_ref = s_res[0]['data']['genome_id']
        #genome_ref = '2702/6/2'
        #genome_ref = '2702/26/1'
        #genome_ref = '2229/21/10'
        print genome_ref
        gaapi = GenomeAnnotationAPI(self.callbackURL, token=user_token)
        genome = gaapi.get_genome_v1({"genomes": [{"ref": genome_ref}],
                                          "included_fields": ["scientific_name"],
                                          "included_feature_fields": ["id", "function", "type"
                                                                      ]})["genomes"][0]["data"]
        genome_dict = {}
        features = genome['features']
        for feature in features:
          id = feature['id']
          try: 
            function = feature['function']
            if not function:
              function = 'Unknown'
          except:
             function = 'Unknown'
          genome_dict[id] = function


        # Check if workspace has data
        if len(s_res) == 0:
            self.__LOGGER.info("Workspace did not return any objects")
            return returnVal

        cuffdiff_dir = script_util2.extract_cuffdiff_data (self.__LOGGER, self.__SHOCK_URL, self.__SCRATCH, s_res, user_token)
        self.__LOGGER.info("Cuffdiff folder = " + cuffdiff_dir)

        if (cuffdiff_dir is False):
            return returnVal

        # Run R script to run cummerbund json and update the cummerbund output json file
        # Prepare output object.
        outputobject=dict()

        # Prepare output plot list
        cummerbundplotset=[]
        # List of plots to generate
        plotlist = [
                { 'file': "dispersionplot.R",
                  'title': "Dispersion plot",
                  'description': "Dispersion plot is the quality measure of the data. It estimates deviation from threshold against counts in FPKM." },


                { 'file': "fpkmscvplot.R",
                  'title': "Genes CV plot",
                  'description': "The squared coefficient of variation plot is a normalized measure of cross-replicate variability that can be useful for evaluating the quality of RNA-seq data." },

                { 'file': "isoformscvplot.R",
                  'title': "Isoform CV plot",
                  'description': "The squared coefficient of variation plot is a normalized measure of cross-replicate variability that can be useful for evaluating the quality of RNA-seq data.Differences in CV2 can result in lower numbers of differentially expressed isoforms due to a higher degree of variability between replicate fpkm estimates." },

                { 'file': "densityplot.R",
                  'title': "Density plot",
                  'description': "The density plot shows the distribution of FPKM scores across samples" },

                { 'file': "csdensityrepplot.R",
                  'title': "Replicates density plot",
                  'description': "The replicates density plot shows the distribution of FPKM scores across sample replicates" },

                { 'file': "boxplot.R",
                  'title': "Box plots",
                  'description': "The box plots show the FPKM distribution across samples." },

                { 'file': "boxrepplot.R",
                  'title': "Box plots of replicates",
                  'description': "The box plots of replicates show the FPKM distribution across sample replicates." },

                { 'file': "pairwisescatterplots.R",
                  'title': "Pairwise scatter plots",
                  'description': "The scatterplots show differences in gene expression between two samples. If two samples are identical, all genes will fall on the mid-line." },

                 { 'file': "volcanomatrixplot.R",
                  'title': "Volcano matrix plots",
                  'description': "Volcano matrix plot is a scatter plot that also identifies differentially expressed genes (by color) between samples based on log2 fold change cut off." },

                { 'file': "pcaplot.R",
                  'title': "PCA plot",
                  'description': "Principal Component Analysis (PCA) is an informative approach for dimensionality reduction for exploring teh relationship between sample conditions." },

                { 'file': "pcarepplot.R",
                  'title': "PCA plot including replicates",
                  'description': "Principal Component Analysis (PCA) is an informative approach for dimensionality reduction for exploring teh relationship between sample conditions including replicates." },

                { 'file': "mdsplot.R",
                  'title': "Multi-dimensional scaling plot",
                  'description': "Multi-dimensional scaling plots are similar to PCA plots and useful for determining the major sources of variation in the dataset. " },

                { 'file': "mdsrepplot.R",
                  'title': "Multi-dimensional scaling plot including replicates",
                  'description': "Multi-dimensional scaling plot including replicates are  similar to PCA plots and useful for determining the major sources of variation in the dataset with replicates. These can be useful to determine any systematic bias that may be present between conditions." }
            ]


        # Iterate through the plotlist and generate the images and json files.
        for plot in plotlist:
            status = script_util2.rplotandupload(self.__LOGGER, self.__SCRATCH, self.__RSCRIPTS,
                plot['file'], self.__SHOCK_URL, self.__HS_URL, user_token,
                cummerbundplotset, plot['title'], plot['description'], cuffdiff_dir)
            if status == False:
                self.__LOGGER.info("Problem generating image and json file - " + plot["file"])


        # Populate the output object
        outputobject['cummerbundplotSet'] = cummerbundplotset

        #TODO: Need to figure out how to get rnaseq experiment id
        outputobject['rnaseq_experiment_id'] = "rnaseq_experiment_id"
        outputobject['cuffdiff_input_id'] = params['ws_cuffdiff_id']

        res = ws_client.save_objects({
            "workspace":params['workspace_name'],
            "objects": [{
                "type":"KBaseRNASeq.cummerbund_output",
                "data":outputobject,
                "name":params["ws_cummerbund_output"]}]
            })

        infile =  join(cuffdiff_dir, "gene_exp.diff") 
        outfile = join(cuffdiff_dir, "gene_exp_diff.out") 
        x=v.volcano_plot_data_parse_and_upload(infile,outfile, genome_dict)
        with open(outfile) as f:
            statdata = json.load(f)
        res = ws_client.save_objects({
            "workspace":params['workspace_name'],
            "objects": [{
                "type":"KBaseRNASeq.DifferentialExpressionStat",
                "data":statdata,
                "name":params["ws_diffstat_output"]}]
            })
        #END generate_cummerbund_plot2

        # At some point might do deeper type checking...
        if not isinstance(returnVal, basestring):
            raise ValueError('Method generate_cummerbund_plot2 return value ' +
                             'returnVal is not type basestring as required.')
        # return the results
        return [returnVal]

    def create_expression_matrix(self, ctx, expressionMatrixParams):
        """
        :param expressionMatrixParams: instance of type
           "expressionMatrixParams" -> structure: parameter "workspace_name"
           of type "workspace_name" (workspace name of the object), parameter
           "ws_cuffdiff_id" of type "ws_cuffdiff_id" (@id ws
           KBaseRNASeq.RNASeqCuffdiffdifferentialExpression), parameter
           "ws_expression_matrix_id" of type "ws_expression_matrix_id" (@id
           ws KBaseFeatureValues.ExpressionMatrix), parameter
           "include_replicates" of type "bool" (indicates true or false
           values, false <= 0, true >=1)
        :returns: instance of type "ws_expression_matrix_id" (@id ws
           KBaseFeatureValues.ExpressionMatrix)
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN create_expression_matrix


        params    = expressionMatrixParams
        returnVal = params['ws_expression_matrix_id']
        #Set up workspace client
        user_token = ctx['token']
        workspace = params['workspace_name']
        ws_client  = Workspace(url=self.__WS_URL, token=user_token)

        #Read the input cuffdiff workspace object json file and get filehandle for cuffdiff tar file
        s_res = ws_client.get_objects([{
            'name' : params['ws_cuffdiff_id'],
            'workspace' : params['workspace_name']
            }])

        # Check if workspace has data
        if len(s_res) == 0:
            self.__LOGGER.info("Workspace did not return any objects")
            return returnVal

        cuffdiff_dir = join (self.__SCRATCH , "cuffdiffData/cuffdiff")
        cuffdiff_dir = script_util2.extract_cuffdiff_data (self.__LOGGER, self.__SHOCK_URL, self.__SCRATCH, s_res, user_token)
        self.__LOGGER.info("Cuffdiff folder = " + cuffdiff_dir)

        if (cuffdiff_dir is False):
            return returnVal

        # Run R script to get fpkmgenematrix.R

        # Prepare output object.
        outjson = False;
        #outjson = "repfpkmgenematrix.R.matrix.txt.json";

        if params['include_replicates'] ==0:
         scriptfile = "fpkmgenematrix.R"
         outjson = script_util2.generate_and_upload_expression_matrix(self.__LOGGER, self.__SCRATCH,
                    self.__RSCRIPTS, scriptfile, self.__SHOCK_URL, self.__HS_URL, user_token,
                    cuffdiff_dir, self.__WS_URL,workspace)


        else:
         scriptfile = "repfpkmgenematrix.R"
         outjson = script_util2.generate_and_upload_expression_matrix(self.__LOGGER, self.__SCRATCH,
                    self.__RSCRIPTS, scriptfile, self.__SHOCK_URL, self.__HS_URL, user_token,
                    cuffdiff_dir, self.__WS_URL,workspace)

        if outjson is False:
            self.__LOGGER.info("Creation of expression matrix failed")
            return returnVal
        with open("{0}/{1}".format(self.__SCRATCH , outjson),'r') as et:
                  eo = json.load(et)
        eo['type']='untransformed'
        genome_ref = s_res[0]['data']['genome_id']
        eo['genome_ref'] = genome_ref

        self.__LOGGER.info(workspace + self.__SCRATCH + outjson + params['ws_expression_matrix_id'])
        ws_client.save_objects({'workspace' : workspace,
            'objects' : [{ 'type' : 'KBaseFeatureValues.ExpressionMatrix',
                           'data' : eo,
                           'name' : params['ws_expression_matrix_id']
                        }]})


        #END create_expression_matrix

        # At some point might do deeper type checking...
        if not isinstance(returnVal, basestring):
            raise ValueError('Method create_expression_matrix return value ' +
                             'returnVal is not type basestring as required.')
        # return the results
        return [returnVal]

    def create_interactive_heatmap_de_genes(self, ctx, interactiveHeatmapParams):
        """
        :param interactiveHeatmapParams: instance of type
           "interactiveHeatmapParams" -> structure: parameter "sample1" of
           String, parameter "sample2" of String, parameter "logMode" of
           String, parameter "removezeroes" of String, parameter
           "condition_select" of String, parameter "q_value_cutoff" of
           Double, parameter "log2_fold_change_cutoff" of Double, parameter
           "num_genes" of Long, parameter "ws_cuffdiff_id" of type
           "ws_cuffdiff_id" (@id ws
           KBaseRNASeq.RNASeqCuffdiffdifferentialExpression), parameter
           "ws_expression_matrix_id" of type "ws_expression_matrix_id" (@id
           ws KBaseFeatureValues.ExpressionMatrix)
        :returns: instance of type "ResultsToReport" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN create_interactive_heatmap_de_genes
        fparams    = interactiveHeatmapParams
        #returnVal = "ttt"
        #Set up workspace client
        user_token = ctx['token']
        workspace = fparams['workspace_name']
        ws_client  = Workspace(url=self.__WS_URL, token=user_token)
        system_params = {}
        system_params['token'] = user_token
        system_params['ws_url'] =  self.__WS_URL
        system_params['logger'] =  self.__LOGGER
        system_params['shock_url'] =  self.__SHOCK_URL
        system_params['hs_url'] =  self.__HS_URL
        system_params['scratch'] =  self.__SCRATCH
        system_params['rscripts'] =  self.__RSCRIPTS
        system_params['workspace'] = workspace





        #Read the input cuffdiff workspace object json file and get filehandle for cuffdiff tar file
        s_res = ws_client.get_objects([{
            'name' : fparams['ws_cuffdiff_id'],
            'workspace' : fparams['workspace_name']
            }])

         #Check if workspace has data
        if len(s_res) == 0:
            self.__LOGGER.info("Workspace did not return any objects")
            return returnVal
        cuffdiff_dir = join (self.__SCRATCH , "cuffdiffData/cuffdiff")
        cuffdiff_dir = script_util2.extract_cuffdiff_data (self.__LOGGER, self.__SHOCK_URL, self.__SCRATCH, s_res, user_token)
        #cuffdiff_dir = "/kb/module/work/nnc/cuffdiff"
        self.__LOGGER.info("Cuffdiff folder = " + cuffdiff_dir)


        #if (cuffdiff_dir is False):
        #    return returnVal
        fparams['cuffdiff_dir'] = cuffdiff_dir
        fparams['infile'] = join (cuffdiff_dir, "gene_exp.diff")
        fparams['outfile'] = join(system_params['scratch'],  "gene_exp.diff.filter")


#        fparams['condition_select'] ="all_pairs"
#        fparams['logMode'] = 0
#        fparams['removezeroes'] = 0

        #User selects 3 options None, All , pair.
        #If the user has selected None, no filtering based on sample is done
        #If the user has selected All, all pairwise options are taken into account
        #If ths uer has selecte pair, only one pair will be taken care of

        #fparams['condition_select']  
        # 0 for all condition pairs, 1 for a certain pair selected
        fparams['pairs']=0
        if (fparams['condition_select'] == 'no_condition_filter_selected'):
           fparams['pairs']=0
        if (fparams['condition_select'] == 'selected_pair'):
           fparams['pairs']=1
        if (fparams['condition_select'] == 'all_pairs'):
           fparams['pairs']=2

        fparams['logModetmp'] = 'log2'
        if (fparams['logMode']=='fpkm'):
            fparams['logModetmp'] = 0
        if (fparams['logMode']=='log2'):
            fparams['logModetmp'] = 2
        if (fparams['logMode']=='log10'):
            fparams['logModetmp'] = 10






        print fparams
        rparams = {}
        
        rparams['cuffdiff_dir'] = fparams['cuffdiff_dir']
        rparams['outpng'] = join (system_params['scratch'], "heatmap.png")
        rparams['imageheight'] = 1600
        rparams['imagewidth'] = 800
        rparams['plotscript'] = join(system_params['rscripts'], "heatmapplotinteractive.R")
        rparams['include_replicates'] = 1
        rparams['pairs'] = fparams ['pairs']
        rparams['logMode'] = fparams['logModetmp']
        rparams['removezeroes'] = fparams['removezeroes']
        rparams['outmatrix'] = join (system_params['scratch'], "outmatrix")
        reportObj = {}

        provenance = [{}]
        if 'provenance' in ctx:
            provenance = ctx['provenance']
        # add additional info to provenance here, in this case the input data object reference
        provenance[0]['input_ws_objects']=[workspace+'/'+fparams['ws_cuffdiff_id']]
       
        report = ""
        if (fparams['pairs'] != 0):

           try:
                filtered_matrix = script_util2.filter_expression_matrix(fparams, system_params)
                self.__LOGGER.info("matrix is " + filtered_matrix)
                fparams['infile'] = join (system_params['scratch'], "gene_exp.diff.filter")
                fparams['outfile'] = join(system_params['scratch'],  "gene_exp.diff.filter.genelist")
                genelist_filtered_matrix_file = script_util2.get_gene_list_from_filter_step(fparams)
                rparams['genelist'] = filtered_matrix
           except:
                report += "There was an error in creating expression matrix"
                report += "No differentially expressed genes were found"
                report += "Please change / double check  your filtering criteria"

	        reportObj = {
		    'objects_created':[],
		    'text_message':report
		}

		reportName = 'create_interactive_heatmap_de_genes_'+str(hex(uuid.getnode()))
		report_info = ws_client.save_objects({
		    'workspace':fparams['workspace_name'],
		    'objects':[
			 {
			  'type':'KBaseReport.Report',
			  'data':reportObj,
			  'name':reportName,
			  'meta':{},
			  'hidden':1, # important!  make sure the report is hidden
			  'provenance':provenance
			 }
		    ] })[0]  
		print('saved Report: '+pformat(report_info))

		returnVal = { "report_name" : reportName,"report_ref" : str(report_info[6]) + '/' + str(report_info[0]) + '/' + str(report_info[4]) }

                return [returnVal]


        try:
	    # Prepare output object.
	    outjson = False;
     

	    roptstr_basic_heatmap_rep = script_util2.get_command_line_heatmap_basic (rparams)

	    # Run R script to run cummerbund json and update the cummerbund output json file
	    # Prepare output object.
	    outputobject=dict()




	    # Prepare output plot list
	    cummerbundplotset=[]

	    # List of plots to generate
	    plotlist = [
		      
		    { 'roptstr': roptstr_basic_heatmap_rep,
		      'title': "Heatmap",
		      'description': "Heatmap", 
		      'exp' : fparams['ws_expression_matrix_id']
		      }

		]
	    fparams['cummerbundplotset'] = cummerbundplotset
	    # Iterate through the plotlist and generate the images and json files.
	    for plot in plotlist:
		fparams['title'] = plot['title']
		fparams['description'] = plot['description']


		status = script_util2.rplotanduploadinteractive(system_params,fparams, rparams, plot['roptstr'])
		if status == False:
		       self.__LOGGER.info("Problem generating image and json file - " + plot["roptstr"])
		else:
		      self.__LOGGER.info(status)

		      outjson = status
		      with open("{0}/{1}".format(self.__SCRATCH , outjson),'r') as et2:
			eo2 = json.load(et2)
			genome_ref = s_res[0]['data']['genome_id']
			eo2['type']=fparams['logMode']
			eo2['genome_ref'] = genome_ref
			self.__LOGGER.info(workspace + self.__SCRATCH + outjson + plot['exp'])
			res = ws_client.save_objects({'workspace' : workspace,
			       'objects' : [{ 'type' : 'KBaseFeatureValues.ExpressionMatrix',
			       'data' : eo2,
			       'name' : plot['exp']
			 }]})

                        info=res[0]
                        report = "Successfully created expression matrix"
			reportObj = {
			    'objects_created':[{
			     'ref': str(info[6]) +'/' + str(info[0]) + '/' + str(info[4]),
                             'description': 'Expression matrix'
			     }],
			    'text_message':report
			   }

        except:
		report += "There was an error in generating expression matrix"
	        reportObj = {
		    'objects_created':[],
		    'text_message':report
		}

	reportName = 'create_interactive_heatmap_de_genes_'+str(hex(uuid.getnode()))
	report_info = ws_client.save_objects({
	    'workspace':fparams['workspace_name'],
	    'objects':[
		 {
		  'type':'KBaseReport.Report',
		  'data':reportObj,
		  'name':reportName,
		  'meta':{},
		  'hidden':1, # important!  make sure the report is hidden
		  'provenance':provenance
		 }
	    ] })[0]  
	print('saved Report: '+pformat(report_info))

	returnVal = { "report_name" : reportName,"report_ref" : str(report_info[6]) + '/' + str(report_info[0]) + '/' + str(report_info[4]) }

#	return [returnVal]


        #returnVal = fparams['ws_expression_matrix_id']

        #END create_interactive_heatmap_de_genes

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method create_interactive_heatmap_de_genes return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def create_interactive_heatmap_de_genes_old(self, ctx, heatmapParams):
        """
        :param heatmapParams: instance of type "heatmapParams" -> structure:
           parameter "sample1" of String, parameter "sample2" of String,
           parameter "q_value_cutoff" of Double, parameter
           "log2_fold_change_cutoff" of Double, parameter "num_genes" of
           Long, parameter "ws_cuffdiff_id" of type "ws_cuffdiff_id" (@id ws
           KBaseRNASeq.RNASeqCuffdiffdifferentialExpression), parameter
           "ws_expression_matrix_id1" of type "ws_expression_matrix_id" (@id
           ws KBaseFeatureValues.ExpressionMatrix), parameter
           "ws_expression_matrix_id2" of type "ws_expression_matrix_id" (@id
           ws KBaseFeatureValues.ExpressionMatrix), parameter
           "ws_cummerbund_output" of type "ws_cummerbund_output" (@id ws
           KBaseRNASeq.cummerbund_output)
        :returns: instance of type "ResultsToReport" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN create_interactive_heatmap_de_genes_old
        fparams    = heatmapParams
        #returnVal = "ttt"
        #Set up workspace client
        user_token = ctx['token']
        workspace = fparams['workspace_name']
        ws_client  = Workspace(url=self.__WS_URL, token=user_token)
        system_params = {}
        system_params['token'] = user_token
        system_params['ws_url'] =  self.__WS_URL
        system_params['logger'] =  self.__LOGGER
        system_params['shock_url'] =  self.__SHOCK_URL
        system_params['hs_url'] =  self.__HS_URL
        system_params['scratch'] =  self.__SCRATCH
        system_params['rscripts'] =  self.__RSCRIPTS
        system_params['workspace'] = workspace




        #Read the input cuffdiff workspace object json file and get filehandle for cuffdiff tar file
        s_res = ws_client.get_objects([{
            'name' : fparams['ws_cuffdiff_id'],
            'workspace' : fparams['workspace_name']
            }])

         #Check if workspace has data
        if len(s_res) == 0:
            self.__LOGGER.info("Workspace did not return any objects")
            return returnVal
        cuffdiff_dir = join (self.__SCRATCH , "cuffdiffData/cuffdiff")
        cuffdiff_dir = script_util2.extract_cuffdiff_data (self.__LOGGER, self.__SHOCK_URL, self.__SCRATCH, s_res, user_token)
        #cuffdiff_dir = "/kb/module/work/nnc/cuffdiff"
        self.__LOGGER.info("Cuffdiff folder = " + cuffdiff_dir)


        #if (cuffdiff_dir is False):
        #    return returnVal
        fparams['cuffdiff_dir'] = cuffdiff_dir
        fparams['infile'] = join (cuffdiff_dir, "gene_exp.diff")
        fparams['outfile'] = join(system_params['scratch'],  "gene_exp.diff.filter")


        fparams['pairs']=1
        fparams['logModetmp'] = 2



        rparams = {}
        
        rparams['cuffdiff_dir'] = fparams['cuffdiff_dir']
        rparams['outpng'] = join (system_params['scratch'], "heatmap.png")
        rparams['imageheight'] = 1600
        rparams['imagewidth'] = 800
        rparams['plotscript'] = join(system_params['rscripts'], "heatmapplotinteractive.R")
        rparams['include_replicates'] = 1
        rparams['pairs'] = fparams ['pairs']
        rparams['logMode'] = fparams['logModetmp']
        rparams['removezeroes'] = 1
        rparams['outmatrix'] = join (system_params['scratch'], "outmatrix")
        reportObj = {}

        provenance = [{}]
        if 'provenance' in ctx:
            provenance = ctx['provenance']
        # add additional info to provenance here, in this case the input data object reference
        provenance[0]['input_ws_objects']=[workspace+'/'+fparams['ws_cuffdiff_id']]
       
        report = ""
        if (fparams['pairs'] != 0):
        
           try:
                filtered_matrix = script_util2.filter_expression_matrix(fparams, system_params)
                self.__LOGGER.info("matrix is " + filtered_matrix)
                fparams['infile'] = join (system_params['scratch'], "gene_exp.diff.filter")
                fparams['outfile'] = join(system_params['scratch'],  "gene_exp.diff.filter.genelist")
                genelist_filtered_matrix_file = script_util2.get_gene_list_from_filter_step(fparams)
                rparams['genelist'] = filtered_matrix
           except:
                report += "There was an error in creating expression matrix"
                report += "No differentially expressed genes were found"
                report += "Please change / double check  your filtering criteria"

	        reportObj = {
		    'objects_created':[],
		    'text_message':report
		}

		reportName = 'create_interactive_heatmap_de_genes_old_'+str(hex(uuid.getnode()))
		report_info = ws_client.save_objects({
		    'workspace':fparams['workspace_name'],
		    'objects':[
			 {
			  'type':'KBaseReport.Report',
			  'data':reportObj,
			  'name':reportName,
			  'meta':{},
			  'hidden':1, # important!  make sure the report is hidden
			  'provenance':provenance
			 }
		    ] })[0]  
		print('saved Report: '+pformat(report_info))

		returnVal = { "report_name" : reportName,"report_ref" : str(report_info[6]) + '/' + str(report_info[0]) + '/' + str(report_info[4]) }

                return [returnVal]


        try:
	    # Prepare output object.
	    outjson = False;
     

	    roptstr_basic_heatmap_rep = script_util2.get_command_line_heatmap_basic (rparams)

	    # Run R script to run cummerbund json and update the cummerbund output json file
	    # Prepare output object.
	    outputobject=dict()




	    # Prepare output plot list
	    cummerbundplotset=[]

	    # List of plots to generate
	    plotlist = [
		      
		    { 'roptstr': roptstr_basic_heatmap_rep,
		      'title': "Heatmap",
		      'description': "Heatmap", 
		      'exp' : fparams['ws_expression_matrix_id']
		      }

		]
	    fparams['cummerbundplotset'] = cummerbundplotset
	    # Iterate through the plotlist and generate the images and json files.
	    for plot in plotlist:
		fparams['title'] = plot['title']
		fparams['description'] = plot['description']


		status = script_util2.rplotanduploadinteractive(system_params,fparams, rparams, plot['roptstr'])
		if status == False:
                    self.__LOGGER.info("Problem generating image and json file - " + plot["roptstr"])
                    report = "Error: Please select a different cutoff criteria. None of the genes passed fold change and q-value-cutoff. "
                    report += "Failed to created expression  matrix with differentially expressed genes. " +  fparams['ws_expression_matrix_id'] + " No genes to show on heatmap."
                    reportObj = {
                    'objects_created':[],
                    'text_message':report
                    }
                    reportName = 'create_interactive_heatmap_de_genes_old_'+str(hex(uuid.getnode()))
                    report_info = ws_client.save_objects({
                        'workspace':fparams['workspace_name'],
                        'objects':[
                        {
                        'type':'KBaseReport.Report',
                        'data':reportObj,
                        'name':reportName,
                        'meta':{},
                        'hidden':1, # important!  make sure the report is hidden
                        'provenance':provenance
                    }
                    ] })[0]  
                    print('saved Report: '+pformat(report_info))

                    returnVal = { "report_name" : reportName,"report_ref" : str(report_info[6]) + '/' + str(report_info[0]) + '/' + str(report_info[4]) }

                    return [returnVal]


		else:
                      
		      self.__LOGGER.info(status)

		      outjson = status
		      self.__LOGGER.info('xxxxxx1')
		      with open("{0}/{1}".format(self.__SCRATCH , outjson),'r') as et2:

			eo2 = json.load(et2)
			genome_ref = s_res[0]['data']['genome_id']
			eo2['type']='log2_level'
			eo2['genome_ref'] = genome_ref
		        self.__LOGGER.info('xxxxxx2')
			self.__LOGGER.info(workspace + self.__SCRATCH + outjson + plot['exp'])
			res = ws_client.save_objects({'workspace' : workspace,
			       'objects' : [{ 'type' : 'KBaseFeatureValues.ExpressionMatrix',
			       'data' : eo2,
			       'name' : plot['exp']
			 }]})
                        info=res[0]
                        self.__LOGGER ('done uploading exp')
                        report = "Successfully created expression matrix"
			reportObj = {
			    'objects_created':[{
			     'ref': str(info[6]) +'/' + str(info[0]) + '/' + str(info[4]),
                             'description': 'Expression matrix'
			     }],
			    'text_message':report
			   }

        except:
		report += "There was an error in generating expression matrix"
	        reportObj = {
		    'objects_created':[],
		    'text_message':report
		}


	reportName = 'create_interactive_heatmap_de_genes_old_'+str(hex(uuid.getnode()))
	report_info = ws_client.save_objects({
	    'workspace':fparams['workspace_name'],
	    'objects':[
		 {
		  'type':'KBaseReport.Report',
		  'data':reportObj,
		  'name':reportName,
		  'meta':{},
		  'hidden':1, # important!  make sure the report is hidden
		  'provenance':provenance
		 }
	    ] })[0]  
	print('saved Report: '+pformat(report_info))

	returnVal = { "report_name" : reportName,"report_ref" : str(report_info[6]) + '/' + str(report_info[0]) + '/' + str(report_info[4]) }


        #END create_interactive_heatmap_de_genes_old

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method create_interactive_heatmap_de_genes_old return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK", 'message': "", 'version': self.VERSION, 
                     'git_url': self.GIT_URL, 'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
