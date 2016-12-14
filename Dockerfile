FROM kbase/kbase:sdkbase.latest
MAINTAINER KBase Developer
# -----------------------------------------

# Insert apt-get instructions here to install
# any required dependencies for your module.

# RUN apt-get update

# -----------------------------------------

RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 \
    git mercurial subversion

RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
    wget --quiet https://repo.continuum.io/miniconda/Miniconda2-4.1.11-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh

RUN apt-get install -y curl grep sed dpkg && \
    TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` && \
    curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb && \
    dpkg -i tini.deb && \
    rm tini.deb && \
    apt-get clean

ENV PATH /opt/conda/bin:$PATH

RUN conda config --add channels conda-forge ;\
conda config --add channels defaults ; \
conda config --add channels r ;\
conda config --add channels bioconda ;

RUN conda install -y bioconductor-ballgown 
RUN conda install  -y bioconductor-cummerbund 
RUN conda install  -y r-getopt 
RUN conda install  -y r-rjson 



RUN \
 pip install -Iv requests_toolbelt>=0.7.0

COPY ./ /kb/module

RUN mkdir -p /kb/module/work/tmp

WORKDIR /kb/module
COPY ./deps /kb/deps
RUN export PYTHONPATH="${PYTHONPATH}:/kb/module/lib/kb_cummerbund"


RUN make 


ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
