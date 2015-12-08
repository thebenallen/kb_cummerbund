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

	params=cummerbundParams

	#Set up workspace client
	user_token=ctx['token']
	ws_client=Workspace(url=self.__WS_URL, token=user_token)

        #Read the input cuffdiff workspace object json file and get filehandle for cuffdiff tar file
	#try:
	s_res= ws_client.get_objects(
				[{'name' : params['ws_cuffdiff_id'],
				  'workspace' : params['workspace_name']}])
	cuffdiff_shock_id = s_res[0]['data']['file']['id']
	cuffdiff_file_name = s_res[0]['data']['file']['file_name']
	#cuffdiff_file_name =None 
	filesize=None
	returnVal=params['ws_cummerbund_output']
#except Exception,e:
 #               raise kb_cummerbundException("Error Downloading ws_cuffdiff_id from the workspace {0},{1}".format(params['ws_cuffdiff_id'],e))
	#Download tar file
	#dx=script_util.download_file_from_shock(self.__LOGGER, self.__SHOCK_URL, cuffdiff_shock_id, cuffdiff_file_name, self.__SCRATCH, filesize, user_token)
	#Decompress tar file and keep it in a directory
	#------TO DO--------------------------
	#use something like input_file = os.path.join(cufflinks_dir,"accepted_hits.bam")
	tarfile=self.__SCRATCH + '/' + cuffdiff_file_name
	#dx=script_util2.untar_files(self.__LOGGER, tarfile, self.__SCRATCH)
	#run R script to run cummerbund json and update the cummerbund output json file
	#-------To DO ------------
 	#Fix so that the path is not hardcoded like this
	cuffdiff_dir = self.__SCRATCH + '/' + 'cuffdiff'
	#post the json file to workspace as cummerbundoutput typed object
	#outpng = self.__SCRATCH + '/' + "dispersionplot.png"
	#outjson = self.__SCRATCH + '/' + "dispersionplot.json"
	#dispersionscript = self.__RSCRIPTS + '/' +'dispersionplot.R'
	#dispersionplot = " --cuffdiff_dir={0} --outpng={1} --outjson={2}".format(cuffdiff_dir,outpng,outjson)
        #diroption = "--cuffdiff_dir="+cuffdiff_dir
        #png = "--outpng=" + outpng	
	#jsonfile="--outjson=" + outjson
       	#subprocess.call(["Rscript", dispersionscript, diroption, png, jsonfile])
        outputobject=dict()
        listplots=[]
        dispersionplotinfo=script_util2.rplotandupload(self.__LOGGER, self.__SCRATCH, self.__RSCRIPTS, "dispersionplot.R", self.__SHOCK_URL, self.__HS_URL, user_token )

	listplots.append({"png_handle": dispersionplotinfo["png_handle"],
			 "png_json_handle": dispersionplotinfo["png_json_handle"],
			  "plot_title": "Dispersion plot",
			  "plot_description": "Dispersion plot"})

        pcaplotinfo=script_util2.rplotandupload(self.__LOGGER, self.__SCRATCH, self.__RSCRIPTS, "pcaplot.R", self.__SHOCK_URL, self.__HS_URL, user_token )

	listplots.append({"png_handle":pcaplotinfo["png_handle"],
			 "png_json_handle":pcaplotinfo["png_json_handle"],
			  "plot_title": "PCA plot",
			  "plot_description": "PCA plot"})



        fpkmscvplot=script_util2.rplotandupload(self.__LOGGER, self.__SCRATCH, self.__RSCRIPTS, "fpkmscvplot.R", self.__SHOCK_URL, self.__HS_URL, user_token )

	listplots.append({"png_handle":fpkmscvplot["png_handle"],
			 "png_json_handle":fpkmscvplot["png_json_handle"],
			  "plot_title": "FPKM SCV plot",
			  "plot_description": "FPKM SCV plot"})


        outputobject["cummerbundplotSet"]=listplots

       #----------TO DO---------------
        # Need to figure out how to get rnaseq experiment id

        outputobject["rnaseq_experiment_id"]="rnaseq_experiment_id"
        outputobject["cuffdiff_input_id"]=params['ws_cuffdiff_id']
     
        res= ws_client.save_objects(
		{"workspace":params['workspace_name'],
		"objects": [{
		"type":"KBaseRNASeq.cummerbund_output",
		"data":outputobject,
		"name":params["ws_cummerbund_output"]
		}]
		}) 
        #END generate_cummerbund_plots

        # At some point might do deeper type checking...
        if not isinstance(returnVal, basestring):
            raise ValueError('Method generate_cummerbund_plots return value ' +
                             'returnVal is not type basestring as required.')
        # return the results
        return [returnVal]
