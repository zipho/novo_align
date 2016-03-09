#!/usr/bin/env python

from __future__ import print_function
import argparse
from subprocess import check_call, CalledProcessError
from json import load, dump, dumps
from os import environ, mkdir, makedirs, path
from os.path import isdir, exists
import shlex
import sys
import logging
log = logging.getLogger( __name__ )

def novo_align(output_filename, index_filename, fwd_file, rev_file ):
    #novoalign -c 8 -k -d /cip0/research/ajayi/RNA-seq_Analysis_Project_Case_Study/reference/Homo_Sapiens/out/TB_H37Rv.nix
    #         -f X165_820L8_.R1_val_1.fq  X165_820L8_.R2_val_2.fq -i PE 250,100
    #         -o SAM '@RG\tID:readgroup\tPU:platform unit\tLB:library' | samtools view -bS - > `pwd`/out/X165_820L8.bam
    #output_filename = path.join(output_directory, fwd_file.split(".")[0] + ".bam")
    param = r'@RG\tID:readgroup\tPU:platform unit\tLB:library'
    cmdline_str = "novoalign -c 8 -k -d {} -f {} {} -i PE 250, 100 -o SAM '{}' | samtools view -bS - > {}".format(
        index_filename,
        fwd_file,
        rev_file,
        param,
        output_filename)
    cmdline = newSplit(cmdline_str)
    try:
        check_call(cmdline)
    except CalledProcessError:
        print("Error running the nova-align", file=sys.stderr)

def newSplit(value):
    lex = shlex.shlex(value)
    lex.quotes = '"'
    lex.whitespace_split = True
    lex.commenters = ''
    return list(lex)

def main():
    parser = argparse.ArgumentParser(description="Generate a BAM file from the Novo Align tool")
    parser.add_argument('output_filename')
    parser.add_argument('--index_filename')
    parser.add_argument('--forward_filename')
    parser.add_argument('--reverse_filename')
    args = parser.parse_args()
   
    #a dirty way of referencing the file
    index_file_path = args.index_filename + "/" + args.index_filename.split("/")[-1]
    
    novo_align(args.output_filename, index_file_path, args.forward_filename, args.reverse_filename)

if __name__ == "__main__": main()
