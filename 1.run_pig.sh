#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --nodes=1                
#SBATCH --job-name=DS-pig   
#SBATCH --mem=4G                
#SBATCH --partition=gpu
#SBATCH --mail-user=nguyen.thanh.dat@nmbu.no
#SBATCH --mail-type=ALL


module load git/2.23.0-GCCcore-9.3.0-nodocs
#module load Nextflow/21.03
module load Nextflow/24.04.2
module load singularity/rpm


genome='/mnt/users/ngda/genomes/pig/Sus_scrofa.Sscrofa11.1.dna.toplevel.fa'

export NXF_SINGULARITY_CACHEDIR=/mnt/users/ngda/sofware/singularity
export $TOWER_ACCESS_TOKEN


nextflow run main.nf -resume -w work_dir \
    --genome ${genome} \
    --chrom 18 \
    --val_chrom 16 \
    --test_chrom 17 \
    --window 200 \
    --peaks '/mnt/SCRATCH/ngda/data/Pig/*.bed' \
    -with-tower