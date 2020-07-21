from __future__ import print_function
from __future__ import division

import argparse
import json
import os
import sys
import platform
import subprocess
import time
import shutil
from copy import deepcopy
from multiprocessing import cpu_count

import r2g
from r2g import errors


def log(info, verbose=False, attr='info'):
    if attr == 'debug' and verbose is False:
        pass
    else:
        print("[{}] {}".format(
            time.strftime("%m-%d-%Y %H:%M:%S", time.localtime()),
            info)
        )


def stamp():
    return time.strftime("%m%d%y%H%M%S", time.localtime())


def bytes2str(b):
    """In Python 3, subprocess.check_output will return a bytes class."""
    return str(b.decode("utf-8"))


def remove_files_dirs(items):
    for item in items:
        try:
            shutil.rmtree(item)
        except shutil.NotADirectoryError:
            os.remove(item)


def processing(current, total, info, mode="fraction"):
    if str(current) != str(total):
        end_chr = ""
    else:
        end_chr = "\n"
    if mode == "percent":
        process = "{}%".format(round(current/total*100, 1))
    else:
        process = "{}/{}".format(current, total)
    print("\r[{}] {}: {}".format(
        time.strftime("%m-%d-%Y %H:%M:%S", time.localtime()),
        info,
        process
    ), end=end_chr),
    sys.stdout.flush()


def parse_arguments(raw_args, version):
    parser = argparse.ArgumentParser()
    parser.add_argument("-V", "--version",
                        help="Print the version.",
                        action="version",
                        version="R2G (reads2gene) {}".format(version))
    parser.add_argument("-v", "--verbose",
                        help="Print detailed log.",
                        action="store_true",
                        default=False)
    parser.add_argument("-r", "--retry",
                        help="Number of times to retry, default: 5. Enabling "
                             "it without any numbers will force it to keep "
                             "retrying.",
                        metavar="INT",
                        nargs="?",
                        default="5")
    parser.add_argument('--cleanup',
                         action="store_true",
                         help="Clean up all intermediate files and only retain "
                              "the final assembled contig file in FASTA format.")
    # 1. Online mode:
    parser.add_argument("-o", "--outdir",
                        help="Specify an output directory.",
                        metavar="DIR",
                        default=os.getcwd())
    # 1.1 NCBI options:
    ncbi = parser.add_argument_group("NCBI options")
    ncbi.add_argument("-s", "--sra",
                      help='Choose SRA accessions (comma-separated without '
                           'blank space), usually whose prefix is "SRX" (e.g. '
                           'SRX4977164).',
                      required=True,
                      metavar="SRA")
    ncbi.add_argument("-q", "--query",
                      help="Submit either a FASTA file or nucleotide "
                           "sequences.",
                      required=True,
                      metavar="SEQUENCE")
    ncbi.add_argument("-p", "--program",
                      help="Specify a blast program: blastn, tblastn, or "
                           "tblastx, default: blastn.",
                      choices=["blastn", "tblastn", "tblastx"],
                      default="blastn",
                      metavar="BLAST")
    ncbi.add_argument("-m", "--max_num_seq",
                      help="Maximum number of aligned sequences to retrieve "
                           "(the actual number of alignments may be greater "
                           "than this), default: 1000.",
                      type=int,
                      default="1000",
                      metavar="INT")
    ncbi.add_argument("-e", "--evalue",
                      default=1e-3,
                      help="Expected number of chance matches in a random "
                           "model, default: 1e-3.",
                      metavar="FLOAT")
    ncbi.add_argument("-c", "--cut",
                      help="Cut sequences and query them respectively to "
                           "prevent weaker matches from being ignored, "
                           "default: 70,20",
                      default="70,20",
                      metavar="FRAGMENT,OVERLAP")
    # 1.2 Trinity options:
    trinity = parser.add_argument_group("Trinity options")
    trinity.add_argument("-t", "--CPU",
                         help="Number of CPU threads to use, default: "
                              "{}.".format(cpu_count()),
                         default=cpu_count(),
                         type=int,
                         metavar="INT")
    trinity.add_argument("--max_memory",
                         help='Suggest max Gb of memory to use by Trinity, '
                              'default: 4G',
                         type=str.upper,
                         metavar="RAM",
                         default="4G")
    trinity.add_argument("--min_contig_length",
                         help="Minimum assembled contig length to report, "
                              "default: 150.",
                         default=150,
                         type=int,
                         metavar="INT")
#   Dosen't work in Trinity >2.6.6 or <1.10.0:
#    trinity.add_argument("-k", "--KMER_SIZE",
#                         help="K-mer size for Trinity, maximum: 32, default: "
#                              "25.",
#                         default=25,
#                         type=int,
#                         metavar="INT")
    trinity.add_argument("--trim",
                         help="Run Trimmomatic to qualify and trim reads, "
                              "default: disabled. Using this option without "
                              "any parameters will trigger preset settings in "
                              "Trinity for Trimmomatic. See Trinity for more "
                              "help.",
                         nargs="?",
                         default=False,
                         metavar="Trimmomatic paramters")
    trinity.add_argument("--stage",
                         help="Stop Trinity after the stage you chose, "
                              "default: butterfly (the final stage)",
                         choices=["no_trinity", "jellyfish", "inchworm",
                                  "chrysalis", "butterfly"],
                         default="butterfly",
                         type=str.lower)
    # TODO:
    # 2. Local mode:
#    local = subparser.add_parser("local")
#    local.add_argument("-q", "--query",
#                       help="Submit either a FASTA file or nucleotide "
#                            "sequences.",
#                       required=True,
#                       metavar="SEQUENCE")
#    local.add_argument("-o", "--outdir",
#                       help="Specify an output directory.",
#                       metavar="DIR",
#                       default=os.getcwd())
#
#    # 2.1 Aligner:
#    aligner = local.add_argument_group("Aligner options")
#    aligner.add_argument("--aligner",
#                         help="Choose a program to align sequences, default:"
#                              " blastx",
#                         default="blastx",
#                         type=str.lower)
    # End of TODO

    args_dict = vars(parser.parse_args(raw_args))  # dict
    try:
        args_dict['retry'] = int(args_dict['retry'])
    except TypeError:
        args_dict['retry'] = float('inf')
    return args_dict


def _ask_yes_or_no(hint):
    choice = input(hint).strip().upper()
    if choice in ['', "Y", "YES"]:
        choice = True
    else:
        choice = False
    return choice


# To use unittest.mock:
def _input_trinity_dir():
    return input("Input the directory of Trinity: ")


# To use unittest.mock:
def _input_fastq_dump_dir():
    return input("Input the directory of fastq-dump: ")


def preflight(args):
    """Pre-flight check and configure"""
    def _file2json(f):
        with open(f, 'r') as inf:
            return json.loads(inf.read())

    def _check_app(path, app):
        """Check if the app exists and is executable"""
        path_app = os.path.join(str(path), str(app))
        if not os.path.isfile(path_app):
            raise errors.InputError("No such file: {}. Please try again "
                                    "later. Abort.".format(path_app))
        else:
            if not os.access(path_app, os.X_OK):
                raise errors.InputError("{} is not executable. Please try "
                                        "again later. Abort.".format(path_app))
            else:
                return True

    def _check_config(config_file):
        try:
            re_config = False
            config_dict = _file2json(config_file)
            for item in config_dict.items():
                try:
                    _ = _check_app(item[1], item[0])
                except errors.InputError:
                    re_config = True
                    break
        except (ValueError, IOError):
            re_config = True
        if os.path.isfile(config_file):
            if os.access(config_file, os.W_OK):
                writable = True
            else:
                writable = False
        else:
            if os.access(os.path.split(config_file)[0], os.W_OK):
                writable = True
            else:
                writable = False
        return re_config, writable

    def _check_sequences(seq):
        alphabets = [
            "ACDEFGHIKLMNPQRSTVWYBXZJUO",  # ambiguous protein
            "GATCRYWSMKHBVDNU"              # ambiguous nucleotide (DNA & RNA)
        ]
        # convert to dict:
        for i in range(len(alphabets)):
            alphabet = {}
            for chr in alphabets[i]:
                alphabet[chr] = None
            alphabets[i] = deepcopy(alphabet)
        if seq.strip()[0] == ">":
            seq = ''.join(seq.strip().split('\n')[1:]).upper()
        else:
            seq = ''.join(seq.strip().split('\n')).upper()
        is_seq = [True, True]
        for i in range(2):
            for letter in seq:
                if letter not in alphabets[i]:
                    is_seq[i] = False
                    break
        return is_seq

    # Check the query file:
    if os.path.isfile(args['query']):
        with open(args['query'], 'r') as inf:
            fasta = inf.read().rstrip('\n').lstrip('>').split('\n>')
            seq = ''
            for q in fasta:
                seq += ''.join(q.strip().split('\n')[1:])
    else:
        seq = args['query'].strip()
    if _check_sequences(seq) == [False, False]:
        raise errors.InputError(
            'Your query sequences are not proteins, nor nucleotides, nor an '
            'accessible file: "{}"'.format(args['query'])
        )

    system = platform.system().lower()
    if system[:3] == 'win':
        find = 'where'  # Windows
    else:
        find = 'which'  # including Linux and Darwin
    app_json = {}.fromkeys(['fastq-dump'])
    if args['stage'] != 'no_trinity':
        app_json['Trinity'] = None
    checked = []
    config_files = [
        os.path.abspath(os.path.join(r2g.__path__[0], "path.json")),
        os.path.abspath(os.path.join(os.path.expanduser('~'), ".r2g.path.json"))
    ]
    log(config_files, args['verbose'], 'debug')
    for cfg in config_files:
        checked.append(_check_config(cfg))
        log("Check config files: {} - {}".format(
            cfg,
            _check_config(cfg)
        ), args['verbose'], 'debug')
    if checked[0][0] is False:
        app_json = _file2json(config_files[0])
        log("Applying the config file: {}".format(config_files[0]))
    elif checked[0][0] is True and checked[1][0] is False:
        app_json = _file2json(config_files[1])
        log("Applying the config file: {}".format(config_files[1]))
    else:
        need_save = False
        input_dir = {
            "Trinity": _input_trinity_dir,
            "fastq-dump": _input_fastq_dump_dir
        }
        for app in app_json.keys():
            configured = False
            try:
                path = os.path.split(bytes2str(subprocess.check_output(
                    [find, app])
                ).strip())[0]
                app_json[app] = path
            except subprocess.CalledProcessError:
                need_save = True
                choice = _ask_yes_or_no(
                    "Couldn't find {} in your $PATH. Configure it manually "
                    "now? ([Y]/N) ".format(app)
                )
                if choice:
                    path = input_dir[app]()
                    while not configured:
                        try:
                            _ = _check_app(path, app)
                        except (ValueError, IOError):
                            log(
                                '"{}": No such file or not executable, please '
                                'try again.'.format(
                                    os.path.join(path, app)
                                )
                            )
                            path = input_dir[app]()
                        else:
                            app_json[app] = path
                            configured = True
                else:
                    log("Aborted by the user.")
                    sys.exit(1)
        if need_save:
            if checked[0] == (True, True) and checked[1][0] is True:
                config_file = config_files[0]
            elif checked[0] == (True, False) and checked[1] == (True, True):
                config_file = config_files[1]
            else:
                config_file = None
                log("Don't have permission to save the config. You may have "
                    "to re-config it next time.")
            if config_file is not None:
                choice = _ask_yes_or_no(
                    "Do you want to keep the config file? ([Y]/N) ".format(
                        config_file
                    )
                )
                if choice:
                    with open(config_file, 'w') as outf:
                        log("The config file was saved as {}".format(
                            config_file
                        ))
                        json.dump(app_json,
                                  outf,
                                  indent=4,
                                  separators=(',', ': ')
                                  )
                else:
                    log("The config file is not saved. You may have to "
                        "re-config it next time.")
    return app_json
