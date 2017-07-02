FROM kbase/kbase:sdkbase.latest
MAINTAINER KBase Developer
# -----------------------------------------

# Insert apt-get instructions here to install
# any required dependencies for your module.

# RUN apt-get update

# -----------------------------------------
RUN apt-get update && apt-get -y install r-bioc-cummerbund r-cran-rjson r-cran-getopt

RUN pip install -Iv requests_toolbelt>=0.7.0
RUN pip install coverage

COPY ./ /kb/module

RUN mkdir -p /kb/module/work/tmp
RUN chmod -R 777 /kb/module

WORKDIR /kb/module
COPY ./deps /kb/deps
RUN export PYTHONPATH="${PYTHONPATH}:/kb/module/lib/kb_cummerbund"

RUN make 

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
