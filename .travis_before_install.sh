#!/bin/bash

TRINITY=2.8.5
SRA=2.10.0
PYTHON=3.7.4

wget -qO /tmp/miniconda.sh $1
bash /tmp/miniconda.sh -bfp $PWD/miniconda3
export PATH=$PATH:$PWD/miniconda3/bin
conda config --add channels bioconda
conda config --add channels conda-forge

if [ "$TRAVIS_OS_NAME" = "osx" ]; then
	wget -qO /tmp/trinity.tar.gz https://github.com/trinityrnaseq/trinityrnaseq/archive/Trinity-v${TRINITY}.tar.gz
	tar -zxvf /tmp/trinity.tar.gz && cd trinityrnaseq-Trinity-v${TRINITY}
	export PATH=/usr/local/bin:$PATH
	make CXX=g++-9 CC=gcc-9 && make plugins CXX=g++-9 CC=gcc-9 && cd ..
	conda install -qy numpy coverage codecov python-coveralls sra-tools=$SRA bowtie2=2.3.5 jellyfish=2.2.10 salmon=1.0.0 samtools=1.9 python=$PYTHON
fi

if [ "$TRAVIS_OS_NAME" = "linux" ]; then
	conda install -qy numpy coverage codecov python-coveralls sra-tools=$SRA trinity=$TRINITY 
fi

conda clean -ayq