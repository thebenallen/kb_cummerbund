#!/usr/bin/env RScript



#m <- .myggclust(myGenes, cluster = "both", rescaling = "row", method = dist, heatscale = c("steelblue", "white", "darkred"), heatMidpoint = 0)




myggheat<-function(object, rescaling='none', clustering='none', labCol=T, labRow=T, logMode=T, pseudocount=1.0, 
		border=FALSE, heatscale=c(low='lightyellow',mid='orange',high='darkred'), heatMidpoint=NULL,fullnames=T,replicates=FALSE,method='none',...) {
	## the function can be be viewed as a two step process
	## 1. using the rehape package and other funcs the data is clustered, scaled, and reshaped
	## using simple options or by a user supplied function
	## 2. with the now resahped data the plot, the chosen labels and plot style are built

	if(replicates){
		m=repFpkmMatrix(object,fullnames=fullnames)
	}else{
		m=fpkmMatrix(object,fullnames=fullnames)
	}
	#remove genes with no expression in any condition
	m=m[!apply(m,1,sum)==0,]
	
	## you can either scale by row or column not both! 
	## if you wish to scale by both or use a different scale method then simply supply a scale
	## function instead NB scale is a base funct
	
    if(logMode) 
    {
      m = log10(m+pseudocount)
    }
	
	## I have supplied the default cluster and euclidean distance (JSdist) - and chose to cluster after scaling
	## if you want a different distance/cluster method-- or to cluster and then scale
	## then you can supply a custom function 
	
	if(!is.function(method)){
		method = function(mat){JSdist(makeprobs(t(mat)))}	
	}

	if(clustering=='row')
		m=m[hclust(method(m))$order, ]
	if(clustering=='column')  
		m=m[,hclust(method(t(m)))$order]
	if(clustering=='both')
		m=m[hclust(method(m))$order ,hclust(method(t(m)))$order]

	## this is just reshaping into a ggplot format matrix and making a ggplot layer
	
	if(is.function(rescaling))
	{ 
		m=rescaling(m)
	} else {
		if(rescaling=='column'){
			m=scale(m, center=T)
		    m[is.nan(m)] = 0
		}
		if(rescaling=='row'){ 
			m=t(scale(t(m),center=T))
		    m[is.nan(m)] = 0
	    }
	}
	
	rows=dim(m)[1]
	cols=dim(m)[2]
	
	
	
    # if(logMode) {
    #   melt.m=cbind(rowInd=rep(1:rows, times=cols), colInd=rep(1:cols, each=rows), melt( log10(m+pseudocount)))
    # }else{
    #   melt.m=cbind(rowInd=rep(1:rows, times=cols), colInd=rep(1:cols, each=rows), melt(m))
    # }
    


    melt.m=cbind(rowInd=rep(1:rows, times=cols), colInd=rep(1:cols, each=rows), melt(m))

	g=ggplot(data=melt.m)
	
	## add the heat tiles with or without a white border for clarity
	
	if(border==TRUE)
		g2=g+geom_rect(aes(xmin=colInd-1,xmax=colInd,ymin=rowInd-1,ymax=rowInd, fill=value),colour='black')
	if(border==FALSE)
		g2=g+geom_rect(aes(xmin=colInd-1,xmax=colInd,ymin=rowInd-1,ymax=rowInd, fill=value))
	
	## add axis labels either supplied or from the colnames rownames of the matrix
	
	if(labCol==T) 
	{
		g2=g2+scale_x_continuous(breaks=(1:cols)-0.5, labels=colnames(m))
	}
	if(labCol==F) 
	{
		g2=g2+scale_x_continuous(breaks=(1:cols)-0.5, labels=rep('',cols))
	}
	
	
	if(labRow==T) 
	{
		g2=g2+scale_y_continuous(breaks=(1:rows)-0.5, labels=rownames(m))	
	}
	if(labRow==F)
	{ 
		g2=g2+scale_y_continuous(breaks=(1:rows)-0.5, labels=rep('',rows))	
	}
	
	# Get rid of the ticks, they get way too dense with lots of rows
    g2 <- g2 + theme(axis.ticks = element_blank()) 

	## get rid of grey panel background and gridlines
	
	g2=g2+theme(panel.grid.minor=element_line(colour=NA), panel.grid.major=element_line(colour=NA),
			panel.background=element_rect(fill=NA, colour=NA))
	
	##adjust x-axis labels
	g2=g2+theme(axis.text.x=element_text(angle=-90, hjust=0))

    #write(paste(c("Length of heatscale is :", length(heatscale))), stderr())
	
	if (logMode)
	{
	   legendTitle <- bquote(paste(log[10]," FPKM + ",.(pseudocount),sep=""))
	   #legendTitle <- paste(expression(plain(log)[10])," FPKM + ",pseudocount,sep="")
	} else {
	   legendTitle <- "FPKM"
	}
	
	if (length(heatscale) == 2){
	    g2 <- g2 + scale_fill_gradient(low=heatscale[1], high=heatscale[2], name=legendTitle)
	} else if (length(heatscale) == 3) {
	    if (is.null(heatMidpoint))
	    {
	        heatMidpoint = (max(m) + min(m)) / 2.0
	        #write(heatMidpoint, stderr())
	    }

	    g2 <- g2 + scale_fill_gradient2(low=heatscale[1], mid=heatscale[2], high=heatscale[3], midpoint=heatMidpoint, name=legendTitle)
	}
	
	#g2<-g2+scale_x_discrete("",breaks=tracking_ids,labels=gene_short_names)
	
	s=list("matrix"=m, "heatmap"=g2)
	## finally add the fill colour ramp of your choice (default is blue to red)-- and return
	return (s)
	
}




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
  'outmatrix', 'm', 1, "character",
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

defaultimageheight = opt$imageheight


suppressMessages(require (cummeRbund))
suppressMessages(require (rjson))



cuff=readCufflinks(opt$cuffdiff)
x=read.table(opt$genelist)
genes = as.vector(unlist(x[1]))
myGenes<-getGenes(cuff,genes)


samples = samples(cuff)$sample_name
genes.features = annotation (genes(cuff))
features = subset(genes.features, select = c(gene_id, gene_short_name))




hmap=c()
if (opt$include_replicates ==0){
hmap<-myggheat(myGenes,cluster='both', fullnames=T, replicates=F)

} else {
hmap<-myggheat(myGenes,cluster='both', fullnames=T, replicates=T)

}


opt$imageheight = length(rownames(hmap$matrix))*12

if (opt$imageheight > defaultimageheight){
    opt$imageheight = defaultimageheight
}

#png(filename = opt$outpng, width = opt$imagewidth, height = opt$imageheight, units = 'px')
#print(hmap$heatmap)
#.invisible <- dev.off()

genes.repFpkm.matrix = hmap$matrix
gene_id = rownames(genes.repFpkm.matrix)
genes.repFpkm.matrix = cbind(gene_id, genes.repFpkm.matrix)
df = genes.repFpkm.matrix
foo <- data.frame(do.call('rbind', strsplit(as.character(df$gene_id),'|',fixed=TRUE)))
colnames(foo)=c("short_gene_id", "x_id")
genes.repFpkm.matrix = cbind(foo$short_gene_id, genes.repFpkm.matrix)
genes.repFpkm.matrix$gene_id=NULL
colnames(genes.repFpkm.matrix)[1] = "gene_id"

write.table(genes.repFpkm.matrix, file =opt$outmatrix, sep="\t", row.names=F)


q(save="no")
