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


genes.repFpkm.matrix = repFpkmMatrix(genes(cuff))
gene_id = rownames(genes.repFpkm.matrix)
genes.repFpkm.matrix = cbind(gene_id, genes.repFpkm.matrix)
repFpkmMatrix = merge(features, genes.repFpkm.matrix, by.x = "gene_id", by.y = "gene_id")

repFpkmMatrix$gene_id=NULL
write.table (repFpkmMatrix, file=opt$out,   sep="\t", row.names=F)
q(save="no")
