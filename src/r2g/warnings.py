def w1():
    return " Warning: since some of fastq files are paired but some are " \
           "not, all fastq files will be taken as singled-end files while " \
           "being fed to Trinity."


def w2(sra, spotN, spotX, retry, err):
    return "Warning: couldn't fetch sequences from the spots {} - {} in the " \
           "sra {} after {} retries. Skipped. Errors from fastq-dump below " \
           "must be investigated: {}".format(sra, spotN, spotX, retry, err)
