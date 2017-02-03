import re
import subprocess
import math
import json
import sys
import os.path

def round_sig(x, sig=2):
    return round(x, sig-int(floor(log10(x)))-1)

def get_max_fold_change_to_handle_inf(infile):
    header=0
    maxvalue={}

    with open(infile) as f:
     for line in f:
         header = header + 1
         if (header > 2):
           includeline=1
           linedata  = line.split("\t")
           m=re.search("NOTEST",line)
           if m is not None:
               includeline=0
           m=re.search("inf",line)
           if m is not None:
               includeline=0
           if includeline==1:
             condition_1 = linedata[4]
             condition_2 = linedata[5]
             unique_key = condition_1 +"~~" + condition_2
             log2fc = abs(float(linedata[9]))
             try:
               currentmax  = maxvalue[unique_key] 
	     except KeyError:
                currentmax  = log2fc
                maxvalue[unique_key] = currentmax
             if (log2fc > currentmax): 
                 maxvalue[unique_key] = log2fc
                 currentmax = log2fc
             
    return maxvalue    
              
def parse_gene_exp_diff (infile,outfile):
  fp = open(outfile, "w")
  with open(infile) as tmp1:
    for line in tmp1:
      linedata = line.split("\t")
      m = re.search(",", linedata[2])
      if m is not None:
        count = linedata[2].split(",")
        valx = ",".join(count)
        for value in count:
           linedata[2] = value
           linex = "\t".join(linedata)
           fp.write(linex)
      else:
           fp.write(line)
  fp.close()
  return outfile

   

def volcano_plot_data_parse_and_upload(infile,outf,genome_dict):
    maxvalue = get_max_fold_change_to_handle_inf (infile)
    infileparse = parse_gene_exp_diff(infile, "infile.out")              
    print maxvalue
    header=0
    outfile="tmp"
    fp=open(outfile, "w")
    with open(infileparse) as f:
     for line in f:
         header = header + 1
         if (header > 2):
           includeline=1
           linedata  = line.split("\t",1)
           m=re.search("NOTEST",line)
           if m is not None:
               includeline=0
           #m=re.search("inf",line)
           #if m is not None:
           #    includeline=0
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

           try: 
             function = genome_dict[linedata[2]]
           except KeyError:
             function = 'Unknown'

           log2fc = linedata[9]
           log2fc_table = linedata[9]
           m=re.search("inf",log2fc)
           if m is None:
               log2fc = float(log2fc)
           else:
               m=re.search("-inf", log2fc)
               if m is None:
                 log2fc_table =  "inf"
                 log2fc = abs(maxvalue[unique_key])
               else:
                  log2fc_table = "-inf"
                  log2fc = -abs(maxvalue[unique_key])
           stats = {"gene": linedata[2] , 
                    "gene_function": function, 
                    "log2fc_text": log2fc_table,
                    "log2fc_f": log2fc,
                    "p_value": float(linedata[12]),
                    "p_value_f": -math.log10(float(linedata[12])),
                    "significant": linedata[13],
                    "value_1": math.log((float(linedata[7])+1),2),
                    "value_2": math.log((float(linedata[8])+1),2),
                    "locus":linedata[3]}
           if (linedata[2] != '-'):
               condition_pair_dict[unique_key]["voldata"].append(stats) 

        counter=0
        for unique_key in condition_pair_dict:
            voldata= condition_pair_dict[unique_key]["voldata"]
            conditions=unique_key.split("~~")
            condition_1 = conditions[0]
            condition_2 = conditions[1]
            data = {"condition_1":condition_1, "condition_2": condition_2, "voldata":voldata}
            diffstat["condition_pairs"].append(data)
            diffstat["unique_conditions"] = unique_conditions_array
            counter = counter + 1
        fpw=open(outf, "w")
        fpw.write( json.dumps(diffstat))
        if (os.path.isfile(outf)):
            return outf
        else:
            return False
         

