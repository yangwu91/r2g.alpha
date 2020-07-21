FROM continuumio/miniconda3
MAINTAINER wuyang@drwu.ga

ENV PY_VER=3.7
ENV TRINITY_VER=2.8.5
ENV SRA_VER=2.10.0

WORKDIR /opt

RUN conda config --add channels bioconda && \
    conda config --add channels conda-forge && \
    # Trinity and sratoolkit:
    conda install -yq trinity=$TRINITY_VER sra-tools=$SRA_VER numpy && \
    # r2g:
    git clone https://github.com/yangwu91/r2g.alpha.git && \
    cd r2g.alpha && \
    pip install -q . && \
    # Clean:
    conda clean -ayq

ENTRYPOINT ["/opt/conda/bin/r2g"]