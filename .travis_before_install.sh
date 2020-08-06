#!/bin/bash

PYTHON=3.8.5

wget -qO /tmp/miniconda.sh $1
bash /tmp/miniconda.sh -bfp /opt/miniconda3
export PATH=$PATH:/opt/miniconda3/bin
conda config --add channels bioconda
conda config --add channels conda-forge

if [ "$TRAVIS_OS_NAME" = "osx" ]; then
	wget -qO /tmp/trinity.tar.gz https://github.com/trinityrnaseq/trinityrnaseq/releases/download/${TRINITY}/trinityrnaseq-${TRINITY}.FULL.tar.gz
	tar -zxvf /tmp/trinity.tar.gz && cd trinityrnaseq-v${TRINITY}
	export PATH=/usr/local/bin:$PATH
	make CXX=g++ CC=gcc && make plugins CXX=g++ CC=gcc && cd ..
	# The version of sra-tools in macOS channel is not the latest, so don't specify it here.
	# The default version of samtools is 1.4, which doesn't work, so set it to the latest (1.10).
	conda install -qy python=$PYTHON sra-tools samtools=1.10 numpy bowtie bowtie2 kmer-jellyfish salmon trimmomatic
fi

if [ "$TRAVIS_OS_NAME" = "linux" ]; then
	conda install -qy sra-tools=$SRA trinity=$TRINITY numpy
fi

conda clean -ayq