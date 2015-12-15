import sys
import os
import json
import re
import io
import urllib
import hashlib
import requests
import logging
import shutil
import time
import traceback
from requests_toolbelt import MultipartEncoder
from multiprocessing import Pool
#from functools import partial
import subprocess
from zipfile import ZipFile
from os import listdir
from os.path import isfile, join, exists
import tarfile
import script_util
try:
    from biokbase.HandleService.Client import HandleService
except:
    from biokbase.AbstractHandle.Client import AbstractHandle as HandleService

from biokbase.workspace.client import Workspace

import biokbase.Transform.script_utils as script_utils

def untar_files(logger, src_fn, dst_path):
    """
    Extract all index files into an output zip file on disk.
    """

    #Check if file exists.
    if exists(src_fn) == False:
        logger.info("Tar file does not exists")
        return False

    # Open archive
    tar = tarfile.open(src_fn)

    # Extract archive
    tar.extractall(dst_path)
    tar.close()

    return True

def rplotandupload (logger, scratch, rscripts, plotscript, shock_url, hs_url, token, cummerbundplotset, title, description, cuffdiff_dir):
    """
    Prepare URIs and call R script to generate image, json files.
    Upload the generated image and json files to Shock
    Get Shock handles and prepare cummerbundplotset object and append
        to user provided list.
    """

    #Check if data directory exists.
    if exists(cuffdiff_dir) == False:
        logger.info("Cuffdiff directory does not exists")
        return False

    # Generated image location
    outpng           = join(scratch,  plotscript) + ".png"
    #Need to check if its already present
    if exists(outpng):
        logger.info("PNG file already exists")
        return False

    # Generated json location
    outjson          = join(scratch,  plotscript) + ".json"
    #Need to check if its already present
    if exists(outjson):
        logger.info("JSON file already exists")
        return False

    # Location of the R script to be executed
    computescript    = join(rscripts, plotscript)
    #Check if it exists
    if exists(computescript) == False:
        logger.info("R script does not exists")
        return False

    # Generate command to be executed.
    ropts            = ["Rscript", computescript]

    ropts.append("--cuffdiff_dir")
    ropts.append(cuffdiff_dir)

    ropts.append("--outpng")
    ropts.append(outpng)

    ropts.append("--outjson")
    ropts.append(outjson)


    # Make call to execute the system.
    roptstr = " ".join(str(x) for x in ropts)
    openedprocess = subprocess.Popen(roptstr, shell=True, stdout=subprocess.PIPE)
    openedprocess.wait()
    #Make sure the openedprocess.returncode is zero (0)
    if openedprocess.returncode != 0:
        logger.info("R script did not return normally, return code - "
            + str(openedprocess.returncode))
        return False

    # Upload image file and get the shock handle
    png_handle = script_util.create_shock_handle( logger,
       outpng, shock_url, hs_url, "png", token )
    #Check for the return value and if error take measure.
    if png_handle["id"] == "":
        logger.info("Could not create Shock handle")
        return False

   #TODO Removed all json handle related stuff. fix it later
    # Upload json file and get the shock handle
   # json_handle = script_util.create_shock_handle( logger,
   #    outjson, shock_url, hs_url, "json", token )
    #Check for the return value and if error take measure.
  #  if json_handle["id"] == "":
   #     logger.info("Could not create Shock handle")
    #    return False

    # Create a return list
    #TODO fix this "png_json_handle"  : json_handle,
    cummerbundplot = {
        "png_handle"       : png_handle,
        "plot_title"       : title,
        "plot_description" : description
    }
    cummerbundplotset.append(cummerbundplot)

    return True


def extract_cuffdiff_data (logger, shock_url, scratch, s_res, user_token):

        returnVal = False
       # Get input data Shock Id and Filename.
        cuffdiff_shock_id = s_res[0]['data']['file']['id']
        cuffdiff_file_name = s_res[0]['data']['file']['file_name']


        filesize = None

        dx = script_util.download_file_from_shock( logger,
            shock_url, cuffdiff_shock_id, cuffdiff_file_name,
            scratch, filesize, user_token)

        #cuffdiff_file_name =None

        #Decompress tar file and keep it in a directory
        tarfile = join(scratch, cuffdiff_file_name)
        dstnExtractFolder = join(scratch, "cuffdiffData")

        if not os.path.exists(dstnExtractFolder):
            os.makedirs(dstnExtractFolder)

        untarStatus = untar_files(logger, tarfile, dstnExtractFolder)
        if untarStatus == False:
            logger.info("Problem extracting the archive")
            return returnVal

        foldersinExtractFolder = os.listdir(dstnExtractFolder)

        if len(foldersinExtractFolder) == 0:
            logger.info("Problem extracting the archive")
            return returnVal

        # Run R script to run cummerbund json and update the cummerbund output json file
        cuffdiff_dir = join(dstnExtractFolder, foldersinExtractFolder[0])

        return cuffdiff_dir


def generate_and_upload_expression_matrix (logger, scratch, rscripts, scriptfile, shock_url, hs_url, token, cuffdiff_dir, ws_url, workspace):
        TSV_to_FeatureValue = "trns_transform_TSV_Exspression_to_KBaseFeatureValues_ExpressionMatrix"
        returnVal = False
        if exists(cuffdiff_dir) == False:
            logger.info("Cuffdiff directory does not exists")
            return False

        #generate expression matrix
        #input = Rscript fpkmgenematrix.R cuffdiff_dir outpath(os.join)

        outmatrix =  join (scratch, scriptfile) + ".matrix.txt"
        outmatrix2 =  scriptfile + ".matrix.txt"
        outjson =    scriptfile + ".matrix.txt.json"

        computescript = join (rscripts, scriptfile)
        if (exists(computescript) == False):
                logger.info("Rscript does not exist")
                return False
        #Generate command to be executed
        ropts = ["Rscript", computescript]

        ropts.append("--cuffdiff_dir")
        ropts.append(cuffdiff_dir)

        ropts.append("--out")
        ropts.append(outmatrix)


        roptstr = " ".join(str(x) for x in ropts)

        #Run Rscript to generate Expression matrix
        openedprocess = subprocess.Popen (roptstr, shell=True, stdout=subprocess.PIPE)
        openedprocess.wait()

        if openedprocess.returncode !=0:
            logger.info("R script did not return normally, return code -"
                + str(openedprocess.returncode))
            return False

        #convert expression matrix TSV to json
        cmd_expression_json = [TSV_to_FeatureValue,
                                    '--workspace_service_url', ws_url,
                                    '--workspace_name', workspace,
                                    '--object_name', outmatrix,
                                    '--working_directory', scratch,
                                    '--input_directory', scratch,
                                    '--output_file_name', outjson ]

        logger.info (" ".join(cmd_expression_json))
        tool_process = subprocess.Popen (" ".join (cmd_expression_json), stderr=subprocess.PIPE, shell=True)
        stdout, stderr = tool_process.communicate()

        if stdout is not None and len(stdout) > 0:
            logger.info(stdout)
        if stderr is not None and len(stderr) > 0:
            logger.info(stderr)

        if tool_process.returncode != 0:
           return False

        return outjson
