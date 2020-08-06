
# Reads to Genes (r2g)

![PyPI](https://img.shields.io/pypi/v/r2g.alpha?logo=pypi&style=plastic) ![pyver](https://img.shields.io/pypi/pyversions/r2g.alpha?logo=python&style=plastic) ![travis](https://img.shields.io/travis/yangwu91/r2g.alpha?logo=travis&style=plastic) ![Codecov](https://img.shields.io/codecov/c/gh/yangwu91/r2g.alpha?logo=codecov&style=plastic) ![docker](https://img.shields.io/docker/cloud/build/yangwu91/r2g.alpha?logo=docker&style=plastic) ![licence](https://img.shields.io/github/license/yangwu91/r2g.alpha?logo=open-source-initiative&style=plastic)

<div align=center><img src="https://raw.githubusercontent.com/yangwu91/r2g.alpha/master/docs/icon.png" alt="icon"/></div>

### 

**Reads to genes**, or **r2g**, is a Python-based light-weight pipeline to find and assemble target homologous genes in species with poor genome assemblies or even without genome assemblies. Very common personal computers without high-end specs nor tons of sequencing data stored can run it adequately. 

## Implementation

### Manually installation
#### Required third-party applications
Three third-party software packages including [NCBI SRA Toolkit](https://github.com/ncbi/sra-tools), [Trinity](https://github.com/trinityrnaseq/trinityrnaseq), and [selenium/standalone-chrome docker](https://github.com/SeleniumHQ/docker-selenium/tree/trunk/StandaloneChrome) (or [chromedriver](https://chromedriver.chromium.org/downloads) with [Chrome web browser](https://www.google.com/chrome/)) are required while running. *N.B.* the Trinity software package doesn’t have pre-compiled binary files for Windows users.

#### Pypi
The r2g pipeline was written in Python, and it can be installed by one command as follows:

```
pip install r2g
```

### Docker (recommended)

We also built a docker image with all required software packages installed and
configured, which can be installed by one command as follows:

```
docker pull yangwu91/r2g:latest
```

This is **recommended** as it is compatible with most common operating systems including
Linux, Windows and macOS.

## Usage

After installation, detailed usage will be printed by the command:

```
r2g --help
```

Or:

```
docker run -it --dns 8.8.8.8 -v /dir/to/your/folder:/opt/data yangwu91/r2g:latest --help
```

In the command, the option `-v /dir/to/your/folder:/opt/data` will mount your folder `/dir/to/your/folder` onto the docker. 

Please check out the detailed options:

```
Optional arguments:
  -h, --help            show this help message and exit
  -V, --version         Print the version.
  -v, --verbose         Print detailed log.
  -r [INT], --retry [INT]
                        Number of times to retry, default: 5. Enabling it without any numbers will force it to keep retrying.
  --cleanup             Clean up all intermediate files and only retain the final assembled contig file in FASTA format.
  -o DIR, --outdir DIR  Specify an output directory.

NCBI options:
  -s SRA, --sra SRA     Choose SRA accessions (comma-separated without blank space), usually whose prefix is "SRX" (e.g. SRX4977164).
  -q SEQUENCE, --query SEQUENCE
                        Submit either a FASTA file or nucleotide sequences.
  -p BLAST, --program BLAST
                        Specify a blast program: blastn, tblastn, or tblastx, default: blastn.
  -m INT, --max_num_seq INT
                        Maximum number of aligned sequences to retrieve (the actual number of alignments may be greater than this), default: 1000.
  -e FLOAT, --evalue FLOAT
                        Expected number of chance matches in a random model, default: 1e-3.
  -c FRAGMENT,OVERLAP, --cut FRAGMENT,OVERLAP
                        Cut sequences and query them respectively to prevent weaker matches from being ignored, default: 70,20

Trinity options:
  -t INT, --CPU INT     Number of CPU threads to use, default: 64.
  --max_memory RAM      Suggest max Gb of memory to use by Trinity, default: 4G
  --min_contig_length INT
                        Minimum assembled contig length to report, default: 150.
  --trim [Trimmomatic paramters]
                        Run Trimmomatic to qualify and trim reads, default: disabled. Using this option without any parameters will trigger preset settings in Trinity for Trimmomatic. See Trinity for more help.
  --stage {no_trinity,jellyfish,inchworm,chrysalis,butterfly}
                        Stop Trinity after the stage you chose, default: butterfly (the final stage)
```

## Example 1: finding "inexistent" *S6K* gene in a mosquito species

We applied the r2g pipeline to search the gene *S6K* (`AAEL018120` from *Aedes aegypti*) in *Aedes albopictus* SRA experiment `SRX885420` (https://www.ncbi.nlm.nih.gov/sra/SRX885420) using the engine `blastn`. Detailed workflow is described as follows:

### Get the sequence of a homologous gene from a well-studied species

Download nucleotide/protein sequences of *Aedes aegypti S6K* from VectorBase, Ensembl, NCBI or other online databases, and let’s say it was saved as the file `/opt/data/AAEL018120-RE.S6K.fasta`.

![lure](https://raw.githubusercontent.com/yangwu91/r2g.alpha/master/docs/20191024163424.png)

### Select a public SRA database for the species to be investigated

Select a proper SRA experiment for *Aedes albopictus* (e.g. `SRX885420`). Some genes only express in specific tissues or at specific time. Make sure the gene you are interested in indeed expresses in the SRA experiment(s) you selected.

![fishing spot](https://raw.githubusercontent.com/yangwu91/r2g.alpha/master/docs/20191024155211.png)

### Run the r2g pipeline

Run the r2g pipeline. Here, we chopped the query (`/opt/data/AAEL018120.fa`) into 80-base fragments overlapping 50 bases. The command line is as follows:

```
r2g -o /dir/to/your/S6K_q-aae_s-SRX885420_c-80.50_p-blastn -s SRX885420 -q /dir/to/your/AAEL018120-RE.S6K.fasta --cut 80,50 -p blastn
```

Or:

```
docker run -it --dns 8.8.8.8 -v /dir/to/your/folder:/opt/data yangwu91/r2g:latest -o /opt/data/S6K_q-aae_s-SRX885420_c-80.50_p-blastn -s SRX885420 -q /dir/to/your/folder/AAEL018120-RE.S6K.fasta --cut 80,50 -p blastn
```

### Check out the result

The sequence file in FASTA format of the predicted *Aedes albopictus S6K* is in the folder `/dir/to/your/folder/S6K_q-aae_s-SRX885420_c-80.50_p-blastn/`. Please verify the sequences by the PCR amplification if necessary.



