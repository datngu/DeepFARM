#!/usr/bin/env python

import pandas as pd
import numpy as np
import argparse
import os, sys



parser = argparse.ArgumentParser(description = "Generating seq lables (DeepSea style)", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--input", nargs='+', help = "List of bed files after applying 'bedtools intersect'", required = True)
parser.add_argument("--out", default = "./label", help = "Output label matrix directory: each file 'chrid.txt.gz' contains lables for 1 chromosome, each column is a epigentic profile, lables are 0 or 1, each row is a sequence")


args = parser.parse_args()

input = args.input
out = args.out

# input = 'data/processed_salmon/*'
# out = './label'

# create output directory
if not os.path.exists(out): os.makedirs(out)


paths = sorted(input)
files = [os.path.basename(path) for path in paths]
#paths = [os.path.join(input, fi) for fi in files]


def process_all_files(paths):
    #all_chroms = set()
    all_ids = dict()
    count = 0
    for path in paths:
        f = open(path, 'rt')
        for l in f:
            tem = l.split('\t')
            chr = tem[0]
            if all_ids.get(chr, 'none') == 'none':
                all_ids[chr] = set()
                all_ids[chr].add(tem[3])
            else:
                all_ids[chr].add(tem[3])
        
        f.close()
        count += 1
        if count % 10 == 0: print(f'done reading {count}/{len(files)} files!') 
        
    return all_ids


def process_file(path, chr):
    res = []
    f = open(path, 'rt')
    for l in f:
        tem = l.split('\t')
        if tem[0] == chr: res.append(tem[3])
    f.close()
    return res

def create_lable_each_chrom(chr_ids, chr, out_fn = 'test.txt.gz'):
    chr_ids = list(chr_ids)
    #chr = chr_ids[0].split('_')[0]
    res = pd.DataFrame(np.zeros(shape = [len(chr_ids), len(files)], dtype = int))
    res.index = chr_ids
    res.columns = files
    count = 0
    for file, path in zip(files, paths):
        ids = process_file(path, chr)
        res.loc[ids, file] = 1
        count += 1
        if count % 10 == 0: print(f'done processing {count}/{len(files)} files!') 

    print(f'writing output!')
    res.to_csv(out_fn, compression = 'gzip', sep = '\t')



all_inputs = process_all_files(paths)

for chr in all_inputs.keys():
    chr_ids = all_inputs[chr]
    out_fn = f'{out}/{chr}.txt.gz'
    print(f'Processing chr {chr}...')
    create_lable_each_chrom(chr_ids, chr, out_fn)



# ./generate_seq_labels.py --input data/processed_salmon/* --out test




