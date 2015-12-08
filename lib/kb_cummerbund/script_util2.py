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
from os.path import isfile, join
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

def rplotandupload (logger, scratch,rscripts, plotscript,shock_url, hs_url, token, listplots, title, description):
	cuffdiff_dir = scratch + '/' + 'cuffdiff'
        #post the json file to workspace as cummerbundoutput typed object
        outpng = scratch + '/' + plotscript + ".png"
        outjson = scratch + '/' + plotscript + ".json"
        dispersionscript = rscripts + '/' + plotscript
        diroption = "--cuffdiff_dir="+cuffdiff_dir
        png = "--outpng=" + outpng
        jsonfile="--outjson=" + outjson
        subprocess.call(["Rscript", dispersionscript, diroption, png, jsonfile])
        plotinfo=dict()
	png_handle=script_util.create_shock_handle(logger,outpng,shock_url,hs_url,".png",token)
	png_json_handle=script_util.create_shock_handle(logger,outjson,shock_url,hs_url,".json",token)
	listplots.append({"png_handle":png_handle,
                         "png_json_handle": png_json_handle,
                          "plot_title": title,
                          "plot_description": description})
        return listplots	
