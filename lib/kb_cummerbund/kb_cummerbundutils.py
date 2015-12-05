import script_utils
import subprocess
from zipfile import ZipFile
from os import listdir
from os.path import isfile, join
from biokbase.workspace.client import Workspace

def readcuffdiff(wsid, objid):
    """
    Read the input cuffdiff workspace object json file
    Returning -
        Shock id
    """

    """ Steps:
    1. Initialize workspace client
    2. Prepare workspace reference with wsid and objid
    3. Call remote end to get the json object
    4. Lookup shock id
    5. Return shock id
    """

def downloaduncompresstar(shock_id, token, scratch):
    """
    Download tar file
    Decompress tar file and keep it in a directory
    Returning -
        Local location of the directory.
    """

    """ Steps:
    1. Create complete shock URL
    2. Prepare the downloadable folder in scratch
    3. Prepare the filename for the downloadable file.
    4. Call download_file_from_shock routine from script_utils
    5. Return the prepared folder name.
    """

def compute(plottypes, inputfolder, cuffdiffinputfile):
    """
    Main compute function to generate pngs and json files.
    It is also upload the resources into workspace.
    Returning -
        Consolidated object of all the runs.
    """

    """ Steps:
    1. Prepare the consolidated return object.
    2. Iterate over all users selected plot types.
    3. Prepare image path
    4. Prepare json file path
    5. Prepare rcmd for the selected plot type.
    6. Run runscriptwait function to generate image and json files.
    7. Check for the return value of the runscriptwait function
    8. Check for the existance of image and json files.
    9. Upload image and json files and get the shock handles.
    10. Update the return object with the shock handles.
    11. Return the return object.
    """


def runscriptwait(rcmd):
    """
    run R script to run cummerbund json and update the cummerbund output json file
    Returning -
        Status of the command
    Note: This is a blocking command, the function will return only after the Rscript is done.
    """

    """ Steps:
    1. Use script_utils to execute the script.
    2. Wait and send the cmd return code.
    """

def posttoworkspace():
    """
    post the json file to workspace as cummerbundoutput typed object
    Returning -
        
    """

    


