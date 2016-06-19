import re
import subprocess
import math
import json
infile="../cuffdiffData/cuffdiff/gene_exp.diff"	

def filter_notest_inf(infile):
    header=0
    outfile="tmpx"
    fp=open(outfile, "w")
    with open(infile) as f:
     for line in f:
         header = header + 1
         if (header > 2):
           includeline=1
           linedata  = line.split("\t",1)
           m=re.search("NOTEST",line)
           if m is not None:
               includeline=0
           m=re.search("inf",line)
           if m is not None:
               includeline=0
           if includeline != 0:
             fp.write(line)
    f.close()
    fp.close()
    cmd=["sort -gk 12,12", "tmp -o tmpx"]
    cmdstr  = " ".join(str(x) for x in cmd)
    openedprocess = subprocess.Popen(cmdstr, shell=True, stdout=subprocess.PIPE)
    openedprocess.wait()
    #Make sure the openedprocess.returncode is zero (0)
    if openedprocess.returncode != 0:
        #logger.info("R script did not return normally, return code - "
        #    + str(openedprocess.returncode))
        return False

    with open("tmpx") as tmp1:
        condition_pair_dict={}
        diffstat = {}
        diffstat["condition_pairs"] = []
        unique_conditions_dict={}
        unique_conditions_array=[]
        voldata=[]
        count=0
        for line in tmp1:
           line=line.strip("\n")
           linedata  = line.split("\t")
           condition_1 = linedata[4]
           condition_2 = linedata[5]
           try:
              val = unique_conditions_dict[condition_1]
           except KeyError:
              unique_conditions_array.append(condition_1)
              unique_conditions_dict[condition_1] =1
           try:
              val = unique_conditions_dict[condition_2]
           except KeyError:
              unique_conditions_array.append(condition_2)
              unique_conditions_dict[condition_2] =1

           unique_key = condition_1 +"~~" + condition_2
           condition_pair_count_dict = {}
           try:
	      value = condition_pair_dict[unique_key] 
	   except KeyError:
              condition_pair_dict[unique_key]={} 
              condition_pair_dict[unique_key]["voldata"] =[] 
           stats = {"gene": linedata[1] , 
                    "function": "", 
                    "log2fc": float(linedata[9]),
                    "log2fc_f": float(linedata[9]),
                    "log2fc_fa": float(linedata[9]),
                    "p_value": float(linedata[11]),
                    "p_value_f": -math.log10(float(linedata[11])),
                    "significant": linedata[13],
                    "value_1": float(linedata[7]),
                    "value_2": float(linedata[8]),
                    "locus":linedata[3]}
           condition_pair_dict[unique_key]["voldata"].append(stats) 

        counter=0
        for unique_key in condition_pair_dict:
            voldata= condition_pair_dict[unique_key]["voldata"]
            #print voldata
            #print "\n\n\n\n"
            conditions=unique_key.split("~~")
            condition_1 = conditions[0]
            condition_2 = conditions[1]
            data = {"condition_1":condition_1, "condition_2": condition_2, "voldata":voldata}
            diffstat["condition_pairs"].append(data)
            diffstat["unique_conditions"] = unique_conditions_array
           # ={"condition_1":condition_1, 
            #        "condition_2": condition_2, 
             #       "voldata":voldata}
            counter = counter + 1
        print json.dumps(diffstat)
'''

#print condition_pair_dict
'''
filter_notest_inf(infile)
