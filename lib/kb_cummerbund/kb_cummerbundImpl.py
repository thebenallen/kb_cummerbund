#BEGIN_HEADER

import simplejson
import sys
import os
import ast
import glob
import json
import logging
import time
import subprocess
import threading, traceback
from collections import OrderedDict
from pprint import pprint
import script_util
import script_util2
from biokbase.workspace.client import Workspace
from biokbase.auth import Token
from os.path import isfile, join, exists

try:
    from biokbase.HandleService.Client import HandleService
except:
    from biokbase.AbstractHandle.Client import AbstractHandle as HandleService




import kb_cummerbundutils




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
    #BEGIN_CLASS_HEADER
    __TEMP_DIR = 'temp'
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
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
                  'description': "Dispersion plot" },


                { 'file': "fpkmscvplot.R",
                  'title': "Genes CV plot",
                  'description': "Genes squared coefficient of variation plot" },

                { 'file': "isoformscvplot.R",
                  'title': "Isoform CV plot",
                  'description': "Isoform coefficient of variation plot" },

                { 'file': "densityplot.R",
                  'title': "Density plot",
                  'description': "Distribution of FPKM scores across samples" },

                { 'file': "csdensityrepplot.R",
                  'title': "Replicates density plot",
                  'description': "Distribution of FPKM scores across sample replicates" },

                { 'file': "boxplot.R",
                  'title': "Box plots",
                  'description': "Box plots of FPKM distribution" },

                { 'file': "boxrepplot.R",
                  'title': "Box plots of replicates",
                  'description': "Box plots of FPKM distribution of replicates" },

                { 'file': "pairwisescatterplots.R",
                  'title': "Pairwise scatter plots",
                  'description': "Pair-wise scatterplots (FPKMs)" },

                 { 'file': "volcanomatrixplot.R",
                  'title': "Volcano matrix plots",
                  'description': "Volcano matrix plots" },

                { 'file': "pcaplot.R",
                  'title': "PCA plot",
                  'description': "PCA plot" },

                { 'file': "pcarepplot.R",
                  'title': "PCA plot including replicates",
                  'description': "PCA plot including replicates" },

                { 'file': "mdsplot.R",
                  'title': "Multi-dimensional scaling plot",
                  'description': "Multi-dimensional scaling plot" },

                { 'file': "mdsrepplot.R",
                  'title': "Multi-dimensional scaling plot including replicates",
                  'description': "Multi-dimensional scaling plot including replicates" }
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

    def create_expression_matrix(self, ctx, expressionMatrixParams):
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN create_expression_matrix

        # ctx is the context object
        # return variables are: returnVal
        #BEGIN generate_cummerbund_plots

        params    = cummerbundParams
        returnVal = params['ws_expression_matrix_id']

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

        # Run R script to get fpkmgenematrix.R
          
        # Prepare output object.

        
	status = script_util2.generate_and_upload_expression_matrix(self.__LOGGER, self.__SCRATCH, self.__RSCRIPTS,
                plot['file'], self.__SHOCK_URL, self.__HS_URL, user_token,
                cummerbundplotset, plot['title'], plot['description'], cuffdiff_dir)
            if status == False:
                self.__LOGGER.info("Problem generating expression matrix json file - " + plot['file'])

       status =   script_util2.generate_and_upload_expression_matrix(self.__LOGGER, self.__SHOCK_URL, self.__SCRATCH, s_res, user_token, params['include_replicated'])

        if (result_method_success is False):
            self.__LOGGER.info("Creation of expression matrix failed")
#END create_expression_matrix

        # At some point might do deeper type checking...
        if not isinstance(returnVal, basestring):
            raise ValueError('Method create_expression_matrix return value ' +
                             'returnVal is not type basestring as required.')
        # return the results
        return [returnVal]
