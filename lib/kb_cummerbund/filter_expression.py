import re
import subprocess
import math
import json
import sys
from os.path import isfile, join, exists
import os.path
from operator import itemgetter

def round_sig(x, sig=2):
    return round(x, sig-int(floor(log10(x)))-1)
def is_valid_row(sample1, sample2, sample1_name, sample2_name):
   match = 0
   if (sample1_name == sample1):
       match = match + 1
   if (sample2_name == sample1):
       match = match + 1
   if (sample1_name == sample2):
       match = match + 1
   if (sample2_name == sample2):
       match = match + 1
   if (match != 2):
       return 0
   return 1


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
              
              
   

def filter_expresssion_matrix_option(scratch,infile,outf,sample1, sample2, num_genes, pvalue_cutoff, log2fc_cutoff):
    maxvalue = get_max_fold_change_to_handle_inf (infile)
    header=0
    outfile =join (scratch,  "tmp1")
    tmpx  =  join (scratch,  "tmpx")
    fp=open(outfile, "w")
    with open(infile) as f:
     for line in f:
         header = header + 1
         if (header > 2):
           includeline=1
           linedata  = line.split("\t")
           sample1_name = linedata[4]
           sample2_name = linedata[5]

           keep_row = 1
           keep_row = is_valid_row(sample1, sample2, sample1_name, sample2_name)
           if (keep_row == 0):
              continue
           m=re.search("NOTEST",line)
           if m is not None:
              continue 
           if includeline != 0:
             fp.write(line)
    f.close()
    fp.close()
    cmd=["sort -gk 12,12",  outfile , "-o" , tmpx]
    cmdstr  = " ".join(str(x) for x in cmd)
    openedprocess = subprocess.Popen(cmdstr, shell=True, stdout=subprocess.PIPE)
    openedprocess.wait()
    #Make sure the openedprocess.returncode is zero (0)
    if openedprocess.returncode != 0:
        #logger.info("R script did not return normally, return code - "
        #    + str(openedprocess.returncode))
        return False
    diffstat = ''
    with open(tmpx) as tmp1:
        for line in tmp1:
           line=line.strip("\n")
           linedata  = line.split("\t")
           condition_1 = linedata[4]
           condition_2 = linedata[5]
           unique_key = condition_1 +"~~" + condition_2
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
           if (linedata[13] =='no'):
               continue
           if (abs(log2fc) < abs(log2fc_cutoff)):
               continue
           p_value_f =  -math.log10(float(linedata[12]))
           if (p_value_f < pvalue_cutoff):
               continue
           commasplit = linedata[2].split(",")
           for lineinfo in commasplit: 
               p_value_f = abs(p_value_f)
               log2fc = abs(log2fc)
               diffstat += lineinfo  + "\t" + str(p_value_f) + "\t" + str(log2fc) + "\n"   

        tmp2 = join (scratch ,  "tmp2")
        tmp3 = join (scratch ,  "tmp3")

        with open(tmp2, "w") as fpw:
           fpw.write(diffstat)

#        with open(tmp2) as fin:
#                lines = [line.split() for line in fin]
#        lines.sort(key=itemgetter(2))

#        with open(tmp3, 'w') as fout:
#                for el in lines:
#                      fout.write('{0}\n'.format(' '.join(el)))

        cmd=["sort -r  -gk 3,3",  tmp2, "-o" , tmp3]
        cmdstr  = " ".join(str(x) for x in cmd)
        openedprocess = subprocess.Popen(cmdstr, shell=True, stdout=subprocess.PIPE)
        openedprocess.wait()
        #Make sure the openedprocess.returncode is zero (0)
        if openedprocess.returncode != 0:
          return False

        diffstat2 = "gene\tq_value\tlog2-fold_change\n"
        with open(outf, "w") as fpd:
            i1=0
            with open(tmp3) as tmp3x:
               for linex in tmp3x:
                 if (i1 >= num_genes):
                    continue
                 i1 = i1+1
                 diffstat2 += linex
            fpd.write(diffstat2)
        if (os.path.isfile(outf)):
            return outf
        else:
            return False



#infile = '/kb/module/work/cuffdiffData/cuffdiff/gene_exp.diff'
#sample1 = 'WT'
#sample2 = 'hy5'
#num_genes = 100
#pvalue_cutoff = 2
#log2fc_cutoff=2
#outf = "outxx"

#outf = filter_expresssion_matrix_option(infile,outf,sample1, sample2, num_genes, pvalue_cutoff, log2fc_cutoff)
