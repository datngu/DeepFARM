# DeepFARM Pipeline

This pipeline is part of the manuscript: "Sequence-based chromatin activity modeling and regulatory impact prediction of genetic variants in farmed animals using deep learning". The computational pipeline leverages the power of [Nextflow](https://www.nextflow.io/) for scalable and reproducible workflows.  

## Repository
GitHub: [DeepFARM](https://github.com/datngu/DeepFARM)

## Author
- **Dat T Nguyen**  
- Contact: ndat<@>utexas.edu  

---

## Features
- Supports multiple learning rates and hyperparameter tuning.
- Built-in reproducibility and scalability via Nextflow and Singularity.  

## Quick Start

### Requirements
- **Modules**:
  - `Nextflow/21.03`
  - `singularity/rpm`
- Environment variables:
  - Set `NXF_SINGULARITY_CACHEDIR` for Singularity.
  - Provide a valid `TOWER_ACCESS_TOKEN` for Nextflow Tower integration.

### Running the Pipeline

Please customize it based on your HPC system and don't forget to look at the file nextflow.config.

```bash
## load modules
module load Nextflow/21.03
module load singularity/rpm

## export env variables
export NXF_SINGULARITY_CACHEDIR=/mnt/users/ngda/software/singularity
export TOWER_ACCESS_TOKEN=<your_access_token>

## run the pipeline
nextflow run main.nf -resume -w work_dir \
    --genome /mnt/users/ngda/genomes/cattle/Bos_taurus.ARS-UCD1.2.dna_sm.toplevel.fa \
    --chrom 29 \
    --val_chrom 21 \
    --test_chrom 25 \
    --window 200 \
    --peaks '/mnt/SCRATCH/ngda/data/Cattle/*.bed' \
    -with-tower


```

### Parameters and defaut setting

- `params.genome`: Path to the genome file (default: `$baseDir/data/ref/genome.fa`).
- `params.peaks`: Path to peak files (default: `$baseDir/data/peak/*`).
- `params.outdir`: Output directory (default: `results`).
- `params.trace_dir`: Directory for trace files (default: `trace_dir`).
- `params.chrom`: The largest chromosome index used to build dataset (default: `29`, this mean chromosome 1,2,3,...,28,29 are used)
- `params.val_chrom`: Chromosome for validation (default: `21`).
- `params.test_chrom`: Chromosome for testing (default: `25`).
- `params.window`: Window size for genomic analysis (default: `200`).
- `params.learning_rates`: Learning rates for model tuning (default: `[1e-3, 1e-4, 5e-4, 5e-5]`).


### Output

- Results will be saved in the specified `--outdir` (default: `results`).
- Trace files for debugging and performance monitoring will be stored in `params.trace_dir` (default: `trace_dir`).

### Citation

TBA

