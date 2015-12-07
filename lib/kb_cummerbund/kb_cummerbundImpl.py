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
	#cuffdiff_file_name = s_res[0]['data']['file']['file_name']
	cuffdiff_file_name =None 
	filesize=None
	returnVal=params['ws_cummerbund_output']
#except Exception,e:
 #               raise kb_cummerbundException("Error Downloading ws_cuffdiff_id from the workspace {0},{1}".format(params['ws_cuffdiff_id'],e))
	#Download tar file
	dx=script_util.download_file_from_shock(self.__LOGGER, self.__SHOCK_URL, cuffdiff_shock_id, cuffdiff_file_name, self.__SCRATCH, filesize, user_token)
	#Decompress tar file and keep it in a directory
	#run R script to run cummerbund json and update the cummerbund output json file
	#post the json file to workspace as cummerbundoutput typed object
	

        #END generate_cummerbund_plots

        # At some point might do deeper type checking...
        if not isinstance(returnVal, basestring):
            raise ValueError('Method generate_cummerbund_plots return value ' +
                             'returnVal is not type basestring as required.')
        # return the results
        return [returnVal]
