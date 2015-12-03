if [ -z "$(which Rscript)" ]; then
  apt-get install r-base
fi
R -q -e 'source("http://bioconductor.org/biocLite.R")'
R -q -e 'biocLite("BiocUpgrade")'
R -q -e 'if (!require("cummeRbund")) biocLite("cummeRbund")'

R -q -e '.libPaths("/kb/runtime/lib/R/library"); install.packages(c("plyr", "reshape2", "ggplot2", "Gviz"));  source("http://bioconductor.org/biocLite.R");biocLite("BiocUpgrade"); if (!require("cummeRbund")) biocLite("cummeRbund");'

