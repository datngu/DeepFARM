#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --nodes=1                
#SBATCH --job-name=val-ck   
#SBATCH --mem=4G                
#SBATCH --partition=gpu
#SBATCH --mail-user=nguyen.thanh.dat@nmbu.no
#SBATCH --mail-type=ALL


#module load git/2.23.0-GCCcore-9.3.0-nodocs
module load Nextflow/24.04.2
module load singularity/rpm


#genome='/mnt/users/ngda/genomes/pig/Sus_scrofa.Sscrofa11.1.dna.toplevel.fa'

export NXF_SINGULARITY_CACHEDIR=/mnt/users/ngda/sofware/singularity
export $TOWER_ACCESS_TOKEN

test_chrom=25

mkdir -p trained_results
cp results/train/* trained_results
cp results/tfr_data/${test_chrom}_fw.tfr trained_results


chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
random_chars=$(printf "%s" "${chars:RANDOM%${#chars}:1}${chars:RANDOM%${#chars}:1}")

nextflow run main_eval.nf -resume \
    -w work_dir_eval \
    -name eval_chicken_${random_chars} \
    --test_tfr "$PWD/trained_results/${test_chrom}_fw.tfr" \
    --models "$PWD/trained_results/*.h5" \
    -with-tower