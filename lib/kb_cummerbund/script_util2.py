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


def untar_files(logger, src_fn, dst_path):
    """
    Extract all index files into an output zip file on disk.
    """
    tar = tarfile.open(src_fn)
    tar.extractall(dst_path)
    tar.close()

def rplotandupload (logger, scratch, rscripts, plotscript, shock_url, hs_url, token, cummerbundplotset, title, description):
    """
    Prepare URIs and call R script to generate image, json files.
    Upload the generated image and json files to Shock
    Get Shock handles and prepare cummerbundplotset object and append
        to user provided list.
    """


    # Base location for the cuffdiff data
    cuffdiff_dir     = join(scratch, "cuffdiff")
    #Check if directory exists.
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

    ropts.append("--cuffdiff_dir", cuffdiff_dir)
    ropts.append("--outpng", outpng)
    ropts.append("--outjson", outjson)

    # Make call to execute the system.
    openedprocess = subprocess.Popen(ropts, shell=True, stdout=subprocess.PIPE)
    openedprocess.wait()
    #Make sure the openedprocess.returncode is zero (0)
    if openedprocess.returncode != 0:
        logger.info("R script did not return normally, return code - "
            + openedprocess.returncode)
        return False

    # Upload image file and get the shock handle
    png_handle = script_util.create_shock_handle( logger,
       outpng, shock_url, hs_url, "png", token )
    #Check for the return value and if error take measure.
    if png_handle.id == "":
        logger.info("Could not create Shock handle")
        return False

    # Upload json file and get the shock handle
    json_handle = script_util.create_shock_handle( logger,
       outjson, shock_url, hs_url, "json", token )
    #Check for the return value and if error take measure.
    if json_handle.id == "":
        logger.info("Could not create Shock handle")
        return False

    # Create a return list
    cummerbundplot = {
        "png_handle"       : png_handle,
        "png_json_handle"  : json_handle,
        "plot_title"       : title,
        "plot_description" : description
    }
    cummerbundplotset.append(cummerbundplot)

    return True

