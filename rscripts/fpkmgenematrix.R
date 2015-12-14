#!/usr/bin/env RScript


suppressMessages(require("getopt"))

options(showWarnCalls=FALSE)
options(showErrorCalls=FALSE)

spec = matrix(c(
  'cuffdiff_dir', 'c', 1, "character",
  'out'      , 'p', 1, "character",
  'help'        , 'h', 0, "logical"
), byrow=TRUE, ncol=4);
opt = getopt(spec);

if ( !is.null(opt$help) ) {
  cat(getopt(spec, usage=TRUE));
  q(status=1);
}

suppressMessages(require (cummeRbund))
suppressMessages(require (rjson))

cuff<-readCufflinks(opt$cuffdiff_dir)

samples = samples(cuff)$sample_name
genes.features = annotation (genes(cuff))
features = subset(genes.features, select = c(gene_id, gene_short_name))
genes.fpkm.matrix = fpkmMatrix(genes(cuff))
gene_id = rownames(genes.fpkm.matrix)
genes.fpkm.matrix = cbind(gene_id, genes.fpkm.matrix)
fpkmMatrix = merge(features, genes.fpkm.matrix, by.x = "gene_id", by.y = "gene_id")
fpkmMatrix$gene_id=NULL
write.table (fpkmMatrix, file=opt$out,   sep="\t", row.names=F)
q(save="no")
