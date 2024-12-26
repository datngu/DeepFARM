#!/usr/bin/env python
from keras.models import load_model, Model
#from tqdm import tqdm
import numpy as np
import pandas as pd
import tensorflow as tf
import argparse
import os, sys, pysam

## functions

## fast way to do one-hot encoding - added N

embed = np.zeros([256, 4], np.float16)
embed[ord('A')] = np.array([1, 0, 0, 0])
embed[ord('C')] = np.array([0, 1, 0, 0])
embed[ord('G')] = np.array([0, 0, 1, 0])
embed[ord('T')] = np.array([0, 0, 0, 1])
embed[ord('N')] = np.array([0, 0, 0, 0])
embed[ord('a')] = np.array([1, 0, 0, 0])
embed[ord('c')] = np.array([0, 1, 0, 0])
embed[ord('g')] = np.array([0, 0, 1, 0])
embed[ord('t')] = np.array([0, 0, 0, 1])
embed[ord('n')] = np.array([0, 0, 0, 0])
embed[ord('.')] = np.array([.25, .25, .25, .25])
embed = tf.convert_to_tensor(embed)


def one_hot_encode_seq(dna_input, numpy = False,  name = "encode_seq"):
  with tf.name_scope(name):
    b = bytearray()
    b.extend(map(ord, str(dna_input)))
    t = tf.convert_to_tensor(b)
    t = tf.cast(t, tf.int32)
    encoded_dna = tf.nn.embedding_lookup(embed, t)
  if numpy == True: 
    return encoded_dna.numpy()
  else:
    return encoded_dna


## fast way to do reverse complement
tab = str.translate("ATGCatgc", "TACGtacg")
def reverse_complement_table(seq):
    return seq.translate(tab)[::-1]


# reading vcf and convert to Pandas df
def vcf2df(vcf_path):
    vcf_file = pysam.VariantFile(vcf_path)
    records = []
    for record in vcf_file:
        chrom = record.chrom
        pos = record.pos
        id = record.id
        ref = record.ref
        alt = record.alts[0]
        records.append([chrom, pos, pos, id, ref, alt])

    return pd.DataFrame(records, columns=['chr', 'pos', 'end', 'id', 'ref', 'alt'])

def read_gvf_txt(file_path):
    df = pd.read_table(file_path, header = 0)
    df['chr'] = df['chr'].astype('str')
    return df


def get_seq(vcf_df, idx, delta=500):
    
    chr = vcf_df.chr[idx]
    pos = vcf_df.pos[idx]-1
    ref = vcf_df.ref[idx]
    alt = vcf_df.alt[idx]
    try:
        seq = ref_genome.fetch(chr, pos-delta, pos+delta)
    except ValueError:
        seq = 'N'*delta*2
        alt_seq = 'N'*delta*2
        return seq, alt_seq
    
    if len(ref) == len(alt):
        alt_seq = seq[:delta] + alt + seq[delta + len(alt):]
    # DEL
    if len(ref) > len(alt):
        alt_seq = seq[:delta] + alt + 'N'*(len(ref)- len(alt)) + seq[delta + len(alt) + (len(ref)- len(alt)):]
    # INL
    if len(ref) < len(alt):
        alt_seq = seq[:delta] + alt + seq[delta + 1:]
        alt_seq = alt_seq[:len(seq)]
    
    # handle error with seq length
    if len(seq) != delta*2: seq = 'N'*delta*2
    if len(alt_seq) != delta*2: alt_seq = 'N'*delta*2

    return seq, alt_seq


def score_variant_block(df_vcf):
    ref_list = []
    alt_list = []
    df_vcf = df_vcf.reset_index() 
    for i in df_vcf.index:
        ref, alt = get_seq(df_vcf, i)
        ref_list.append(one_hot_encode_seq(ref))
        alt_list.append(one_hot_encode_seq(alt))
    
    ref_list = tf.stack(ref_list)
    alt_list = tf.stack(alt_list)
    ref_pred = model.predict(ref_list, batch_size = 128, verbose = 0)
    alt_pred = model.predict(alt_list, batch_size = 128, verbose = 0)
    dif = ref_pred - alt_pred
    max_score = dif.max(1)
    mean_score = dif.mean(1)
    sum_score = dif.sum(1)
    stat_df = pd.DataFrame({'max_score': max_score, 'mean_score': mean_score, 'sum_score' : sum_score})
    df_dif = pd.DataFrame(dif)
    df_dif.columns = cols[0]
    df_dif_merged = pd.concat([df_vcf, stat_df, df_dif], axis=1)
    #df_dif_merged.to_csv(out_name, sep = '\t', index=None)
    return df_dif_merged


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Predict variant impact of genomic variant)", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--model", help = "trained model (tensorflow, h5 format)", required = True)
    parser.add_argument("--cols", help = "used to label output columns , txt file contains lablels for each column predicited, each line correspond a track", required = True)
    parser.add_argument("--vcf", help = "VCF input, chromosme must be encoded as number {1,2,..}", required = True)
    parser.add_argument("--genome", help = "Genome fasta file, typically download from ensemble, chromosme must be encoded as number {1,2,..}", required = True)
    parser.add_argument("--out", default = "predicted_variant_impact.txt", help = "output txt file")


    args = parser.parse_args()
    vcf_file = args.vcf
    genome_file = args.genome
    model_file = args.model 
    col_file = args.cols
    out_file = args.out
    model = load_model(model_file)

    #df = vcf2df(vcf_file)
    # Load variant file
    if vcf_file.endswith('txt'):
        df = read_gvf_txt(vcf_file)
    elif vcf_file.endswith('vcf.gz'):
        df = vcf2df(vcf_file)
    else:
        raise ValueError('Variant file must end with ".txt" or ".vcf.gz"')

    ref_genome = pysam.FastaFile(genome_file)
    cols = pd.read_csv(col_file, header=None)

    jobs = list(range(0, len(df), 512))
    jobs[-1] = len(df)

    
    #res_all = []
    #for i in tqdm(range(1, len(jobs))):
    for i in range(1, len(jobs)):
        s = jobs[i-1]
        e = jobs[i]
        my_df = df.iloc[s:e, :]
        scores = score_variant_block(my_df)
        scores = scores.drop("index", axis = 1)
        #res_all.append(scores)
        if i == 1:
            scores.to_csv(out_file, sep = '\t', index=False)
        else:
            scores.to_csv(out_file, mode='a', sep = '\t', index=False, header=False)

