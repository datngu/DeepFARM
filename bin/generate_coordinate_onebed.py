#!/usr/bin/env python

import sys
import gzip
import argparse
import pandas as pd
import numpy as np


parser = argparse.ArgumentParser(description = "Generating genome coordinate bed files (DeepSea style) for extracting sequences", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--genome", help = "genome faidx input (index of genome fasta)", required = True)
parser.add_argument("--out", default = "genome_window.bed", help = "output bed files of windows")
parser.add_argument('--window', type=int, default = 200, help = 'window length for slipting the genome')
parser.add_argument('--chrom', type=int, default = 29, help = 'number of top contigs considered, for example salmon genome has 29 chroms')

args = parser.parse_args()

genome = args.genome
out = args.out
window = args.window
chrom = args.chrom

# genome = 'data_genome/Salmo_salar.Ssal_v3.1.dna.toplevel.fa.fai'
# out = 'genome_windows.bed'
# window = 200
# chrom = 30

df = pd.read_csv(genome, sep="\t", header=None)
df = df.iloc[:chrom,:]


fo = open(out, 'w')
for i in range(chrom):
    row = df.loc[i]
    bin = list(range(0, row[1], window))
    start = bin[0:-1]
    end = bin[1:]
    chr = [row[0] for _ in range(len(start))]

    for c, s, e in zip(chr, start, end):
        s = str(s)
        e = str(e)
        id = '_'.join([c,s,e])
        line = '\t'.join([c,s,e,id])
        fo.writelines(line + '\n')
    
    print(f'done chromosome {i+1}')

fo.close()

# ./generate_coordinate_onebed.py --genome data_genome/Salmo_salar.Ssal_v3.1.dna.toplevel.fa.fai
