#!/usr/bin/env python

from __future__ import print_function
import argparse
from subprocess import check_call, CalledProcessError
from json import load, dump, dumps
from os import environ, mkdir, makedirs, path
from os.path import isdir, exists
import shlex
import sys

def novo_align(output_directory, index_filename, fwd_file, rev_file ):
    if exists(output_directory) and not isdir(output_directory):
        print("Output directory path already exists but is not a directory: {}".format(output_directory),
              file=sys.stderr)
    elif not exists(output_directory):
        mkdir(output_directory)

    #novoalign -c 8 -k -d /cip0/research/ajayi/RNA-seq_Analysis_Project_Case_Study/reference/Homo_Sapiens/out/TB_H37Rv.nix
    #         -f X165_820L8_.R1_val_1.fq  X165_820L8_.R2_val_2.fq -i PE 250,100
    #         -o SAM '@RG\tID:readgroup\tPU:platform unit\tLB:library' | samtools view -bS - > `pwd`/out/X165_820L8.bam

    output_filename = path.join(output_directory, fwd_file.split(".")[0] + ".bam")

    cmdline_str = "novoalign -c 8 -k -d {} -f {} {} -i PE 250, 100 -o SAM '@RG\tID:readgroup\tPU:platform unit\tLB:library' | samtools view -bS - > {}".format(
        index_filename,
        fwd_file,
        rev_file,
        output_filename)
    cmdline = shlex.split(cmdline_str)
    try:
        check_call(cmdline)
    except CalledProcessError:
        print("Error running the nova-align", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Generate a BAM file from the Novo Align tool")
    parser.add_argument('output_filename')
    parser.add_argument('--index_filename')
    parser.add_argument('--forward_filename')
    parser.add_argument('--reverse_filename')
    args = parser.parse_args()

    filename = args.output_filename
    print("=============================")
    print(args.__dict__)

    params = load(open(filename, 'rb'))
    output_directory = params['output_data'][0]['extra_files_path']
    makedirs(output_directory)

    novo_align(output_directory, args.index_filename, args.forward_filename, args.reverse_filename)

if __name__ == "__main__": main()
