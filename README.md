# Reads to Genes (r2g)

![PyPI](https://img.shields.io/pypi/v/r2g?logo=pypi&style=plastic) ![py_ver](https://img.shields.io/pypi/pyversions/r2g?logo=python&style=plastic) ![travis](https://img.shields.io/travis/yangwu91/r2g?logo=travis&style=plastic) ![Codecov](https://img.shields.io/codecov/c/gh/yangwu91/r2g?logo=codecov&style=plastic) ![docker](https://img.shields.io/docker/cloud/build/yangwu91/r2g?logo=docker&style=plastic) ![licence](https://img.shields.io/github/license/yangwu91/r2g?logo=open-source-initiative&style=plastic)

<div align=center><img src="https://raw.githubusercontent.com/yangwu91/r2g/master/images/banner.png" alt="banner"/></div>

[TOC]

## Introduction

**Reads to genes**, or **r2g**, is a computationally lightweight and homology-based pipeline that allows rapid identification of genes or gene families from raw sequence databases in the absence of an assembly, by taking advantage of  over 10,000 terabases of sequencing data for all kinds of species deposited in  [Sequence Read Archive](https://www.ncbi.nlm.nih.gov/sra) hosted by [National Center for Biotechnology Information](https://www.ncbi.nlm.nih.gov/), which can be effectively run on **most common computers without high-end specs**.

## Implementation

### Pull the Docker image (recommended)

Please follow the instruction [here](https://docs.docker.com/get-docker/) to download and install Docker based on your operating system before running the Docker image. This is **recommended** as it is compatible with most common operating systems including Linux, macOS and Windows.

Then, pull the r2g Docker image with all required software packages installed and configured by one command as follows:

```
docker pull yangwu91/r2g:latest
```

Now, you are good to go.

### Manually installation

#### Required third-party applications

The r2g required 3 third-party software packages including [NCBI SRA Toolkit](https://github.com/ncbi/sra-tools), [Trinity](https://github.com/trinityrnaseq/trinityrnaseq), and [Google Chrome web browser](https://www.google.com/chrome/) with [ChromeDriver](https://chromedriver.chromium.org/downloads) (or [selenium/standalone-chrome](https://github.com/SeleniumHQ/docker-selenium/tree/trunk/StandaloneChrome) Docker image). 

##### NCBI SRA Toolkit

Download pre-built binaries for **all platforms** [here](https://github.com/ncbi/sra-tools/wiki/01.-Downloading-SRA-Toolkit) or compile the source code [here](https://github.com/ncbi/sra-tools/releases) by yourself.

For **Linux** and **macOS** users, it also can be installed using [Conda](https://docs.conda.io/en/latest/) via the [Bioconda](https://bioconda.github.io/) channel:

```bash
conda install -c bioconda sra-tools
```

##### Trinity

Follow the [instruction](https://github.com/trinityrnaseq/trinityrnaseq/wiki/Installing-Trinity) to compile the source code. Please note that Trinity has its own dependencies, including [samtools](https://github.com/samtools/samtools), [Python 3](https://www.python.org/) with [NumPy](https://numpy.org/install/), [bowtie2](http://bowtie-bio.sourceforge.net/bowtie2/index.shtml), [jellytfish](http://www.genome.umd.edu/jellyfish.html), [salmon](https://salmon.readthedocs.io/en/latest/salmon.html), and [trimmomatic](http://www.usadellab.org/cms/?page=trimmomatic).

For **Linux** users, Trinity can be installed easily using Conda, and you would never worry about other dependencies:

```bash
conda install -c bioconda trinity=2.8.5 numpy samtools=1.10
```

The Trinity **Version 2.8.5** has been fully tested, and theoretically, the later versions should work too.

##### Google Chrome web browser with ChromeDriver

First, please install [Google Chrome web browser](https://www.google.com/chrome/). Second, please download the corresponding version of [ChromeDriver](https://chromedriver.chromium.org/downloads). 

Or, you can simply run [selenium/standalone-chrome](https://github.com/SeleniumHQ/docker-selenium/tree/trunk/StandaloneChrome) Docker image in background (make sure you have the permission to bind the 4444 port on local host):

```bash
docker run -d -p 4444:4444 -v /dev/shm:/dev/shm selenium/standalone-chrome
```

#### Installing the r2g package
The r2g package has been deposited to PyPI, so it can be installed as follows:

```
pip install r2g
```

After installing the dependencies and r2g package, now you are good to go.

## Usage

Detailed usage will be printed by the command:

```bash
docker run -it yangwu91/r2g:latest --help
```

Or:

```bash
r2g --help
```

```
Optional arguments:
  -h, --help            show this help message and exit
  -V, --version         Print the version.
  -v, --verbose         Print detailed log.
  -r [INT], --retry [INT]
                        Number of times to retry.Enabling it without any numbers will force it to keep retrying. Default: 5.
  --cleanup             Clean up all intermediate files and only retain the final assembled contig file in FASTA format.
  -o DIR, --outdir DIR  Specify an output directory. Default: current working directory.
  -W DIR, --browser DIR
                        Temporarily overwrite the local path or the remote address of the chrome webdriver. E.g., /path/to/chromedriver or http://127.0.0.1:4444/wd/hub
  -P SCHEME://IP:PORT, --proxy SCHEME://IP:PORT
                        Set up proxies. Http and socks are allowed, but authentication is not supported yet (still testing).

NCBI options:
  -s SRA, --sra SRA     Choose SRA accessions (comma-separated without blank space). E.g., "SRX885418" (an SRA experiment) or "SRR1812886,SRR1812887" (SRA runs)
  -q SEQUENCE, --query SEQUENCE
                        Submit either a FASTA file or nucleotide sequences.
  -p BLAST, --program BLAST
                        Specify a BLAST program: tblastn, tblastx, or blastn (including megablast, blastn, and discomegablast). Default: blastn.
  -m INT, --max_num_seq INT
                        Maximum number of aligned sequences to retrieve (the actual number of alignments may be greater than this). Default: 1000.
  -e FLOAT, --evalue FLOAT
                        Expected number of chance matches in a random model. Default: 1e-3.
  -c FRAGMENT,OVERLAP, --cut FRAGMENT,OVERLAP
                        Cut sequences and query them respectively to prevent weaker matches from being ignored. Default: 70,20 (nucleotides), or 24,7 (amino acids)

Trinity options:
  -t INT, --CPU INT     Number of CPU threads to use. Default: the total number of your computer.
  --max_memory RAM      Suggest max Gb of memory to use by Trinity. Default: 4G.
  --min_contig_length INT
                        Minimum assembled contig length to report. Default: 150.
  --trim [TRIM_PARAM]   Run Trimmomatic to qualify and trim reads. Using this option without any parameters will trigger preset settings in Trinity for Trimmomatic. See Trinity for more help. Default: disabled.
  --stage {no_trinity,jellyfish,inchworm,chrysalis,butterfly}
                        Stop Trinity after the stage you chose. Default: butterfly (the final stage).
```

### Specific options for running the Docker image

While executing the Docker image, some specific options are required: `-v /dev/shm:/dev/shm`, `-v /path/to/your/workspace:/workspace`, and `-u $UID`. 

* The option `-v /dev/shm:/dev/shm` shares host's memory to avoid applications crashing inside a Docker container. 

- The option `-v /path/to/your/workspace:/workspace` mounts the local directory `/path/to/your/workspace` (specify your own) to the working directory `/workspace` (don't change it) inside a Docker container, which is the input and output directory.

- The option `-u $UID` sets the owner of the Docker outputs. Ignoring it will raise permission errors.

Let's say there is a folder named `r2g_workspace` in your home `/home/user`. As a result, the the simplest full command to run a Docker image should be:

```bash
docker run -it -v /dev/shm:/dev/shm -v /home/user/r2g_workspace:/workspace -u $UID yangwu91/r2g:latest -o OUTPUT -q /home/user/r2g_workspace/QUERY.fasta -s SRXNNNNNN
```

After that, you can check out the results in the folder `/home/user/r2g_workspace/OUTPUT/`.

### An example: finding "inexistent" *S6K* gene in a mosquito species

We applied the r2g pipeline to search the gene *S6K* (`AAEL018120` from *Aedes aegypti*) in *Aedes albopictus* SRA experiment `SRX885420` (https://www.ncbi.nlm.nih.gov/sra/SRX885420) using the engine `blastn`. Detailed workflow is described as follows:

#### Get the sequence of a homologous gene from a well-studied species

Download nucleotide/protein sequences of *Aedes aegypti S6K* from VectorBase, Ensembl, NCBI or other online databases, and let’s say it was saved as the file `/home/user/r2g_orkspace/AAEL018120-RE.S6K.fasta`.

![lure](https://raw.githubusercontent.com/yangwu91/r2g/master/images/20191024163424.png)

#### Select a public SRA database for the species to be investigated

Select a proper SRA experiment for *Aedes albopictus* (e.g. `SRX885420`). Some genes only express in specific tissues or at specific time. Make sure the gene you are interested in indeed expresses in the SRA experiment(s) you selected.

![fishing spot](https://raw.githubusercontent.com/yangwu91/r2g/master/images/20191024155211.png)

#### Run the r2g pipeline

Run the r2g pipeline. Here, we chopped the query (`/home/user/r2g_workspace/AAEL018120-RE.S6K.fasta`) into 80-base fragments overlapping 50 bases. The command line is as follows:

```bash
r2g -o /home/user/r2g_workspace/S6K_q-aae_s-SRX885420_c-80.50_p-blastn -s SRX885420 -q /home/user/r2g_workspace/AAEL018120-RE.S6K.fasta --cut 80,50 -p blastn
```

Or:

```bash
docker run -it -v /dev/shm:/dev/shm -v /home/user/r2g_workspace:/workspace -u $UID yangwu91/r2g:latest -o /home/user/r2g_workspace/S6K_q-aae_s-SRX885420_c-80.50_p-blastn -s SRX885420 -q /home/user/r2g_workspace/AAEL018120-RE.S6K.fasta --cut 80,50 -p blastn
```

#### Check out the result

The sequence file in FASTA format of the predicted *Aedes albopictus S6K* is in the folder `/home/user/r2g_workspace/S6K_q-aae_s-SRX885420_c-80.50_p-blastn/`. Please verify the sequences by the PCR amplification if necessary.