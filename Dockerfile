FROM kbase/sdkbase:latest
MAINTAINER KBase Developer
# -----------------------------------------

# Insert apt-get instructions here to install
# any required dependencies for your module.

# RUN apt-get update

# -----------------------------------------

COPY ./ /kb/module

RUN mkdir -p /kb/module/work

RUN apt-get update && apt-get -y install r-bioc-cummerbund 

WORKDIR /kb/module
COPY ./deps /kb/deps

RUN make



ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
