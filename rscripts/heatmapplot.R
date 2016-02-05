#!/usr/bin/env RScript


suppressMessages(require("getopt"))

options(showWarnCalls=FALSE)
options(showErrorCalls=FALSE)

spec = matrix(c(
  'genelist', 'g', 1, "character",
  'cuffdiff', 'c', 1, "character",
  'outpng', 'o', 1, "character",
  'imageheight', 'i', 1, "character",
  'imagewidth', 'w', 1, "character",
  'include_replicates', 'r', 1, "character",
  'help'        , 'h', 0, "logical"
), byrow=TRUE, ncol=4);
opt = getopt(spec);

if ( !is.null(opt$help) ) {
  cat(getopt(spec, usage=TRUE));
  q(status=1);
}

suppressMessages(require (cummeRbund))
suppressMessages(require (rjson))

opt$imageheight = as.numeric(opt$imageheight)
opt$imagewidth = as.numeric(opt$imagewidth)

opt$include_replicates = as.numeric(opt$include_replicates)



cuff=readCufflinks(opt$cuffdiff)
x=read.table(opt$genelist)
genes = as.vector(unlist(x[1]))
myGenes<-getGenes(cuff,genes)

png(filename = opt$outpng, width = opt$imagewidth, height = opt$imageheight, units = 'px')

hmap=c()
if (opt$include_replicates ==0){
hmap<-csHeatmap(myGenes,cluster='both', fullnames=T)
} else {
hmap<-csHeatmap(myGenes,cluster='both', fullnames=T, replicates=T)
}
print(hmap)
.invisible <- dev.off()
#write(toJSON(disp$data), file=opt$outjson)
q(save="no")
