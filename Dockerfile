FROM kbase/kbase:sdkbase.latest
MAINTAINER KBase Developer
# -----------------------------------------

# Insert apt-get instructions here to install
# any required dependencies for your module.

# RUN apt-get update

# -----------------------------------------

RUN apt-get update && apt-get -y install r-bioc-cummerbund r-cran-rjson r-cran-getopt


RUN \
  . /kb/dev_container/user-env.sh && \
  cd /kb/dev_container/modules && \
  rm -rf jars && \
  rm -rf transform && \
  git clone https://github.com/kbase/jars && \
  git clone https://github.com/kbase/transform && \
  cd /kb/dev_container/modules/jars && \
  make deploy && \
  cd /kb/dev_container/modules/transform && \
  make && make deploy

COPY ./ /kb/module

RUN mkdir -p /kb/module/work/tmp

WORKDIR /kb/module
COPY ./deps /kb/deps
RUN export PYTHONPATH="${PYTHONPATH}:/kb/module/lib/kb_cummerbund"


RUN make 


ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
