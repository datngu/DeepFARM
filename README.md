# DeepFARM Pipeline

A comprehensive computational pipeline for sequence-based chromatin activity modeling and regulatory impact prediction of genetic variants in farmed animals using deep learning.

## Overview

DeepFARM is part of the manuscript: "Sequence-based chromatin activity modeling and regulatory impact prediction of genetic variants in farmed animals using deep learning". This pipeline leverages the power of [Nextflow](https://www.nextflow.io/) for scalable and reproducible workflows, enabling researchers to analyze chromatin accessibility patterns and predict the regulatory impact of genetic variants in livestock species.

### Key Capabilities
- **Multi-species support**: Cattle, pig, chicken, and salmon
- **Deep learning models**: Built-in DanQ architecture for chromatin accessibility prediction
- **Genomic variant analysis**: Regulatory impact prediction for genetic variants
- **Scalable workflow**: Nextflow-based pipeline with Singularity containerization

## Repository
GitHub: [DeepFARM](https://github.com/datngu/DeepFARM)

## Author
- **Dat T Nguyen**  
- Contact: ndat@utexas.edu  

---

## Features
- Multiple learning rates and hyperparameter tuning support
- Built-in reproducibility and scalability via Nextflow and Singularity
- Pre-trained models for multiple livestock species
- Configurable genomic window sizes and chromosome selection
- Integrated validation and testing workflows

## Quick Start

### Prerequisites

#### System Requirements
- High-performance computing (HPC) environment recommended
- Linux operating system
- Sufficient storage space for genomic data and intermediate files

#### Software Dependencies
- **Nextflow** (version 21.03 or later)
- **Singularity** (for containerization)

#### Environment Setup
1. **Load required modules** (adjust for your HPC system):
   ```bash
   module load Nextflow/21.03
   module load singularity/rpm
   ```

2. **Set environment variables**:
   - `NXF_SINGULARITY_CACHEDIR`: Directory for Singularity image cache
   - `TOWER_ACCESS_TOKEN`: Token for Nextflow Tower integration (optional)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/datngu/DeepFARM.git
   cd DeepFARM
   ```

2. **Configure the pipeline**:
   - Review and customize `nextflow.config` for your HPC system
   - Adjust resource allocations, queue settings, and file paths

### Running the Pipeline

**Important**: Customize the following example based on your HPC system configuration and data paths.

```bash
# Load required modules
module load Nextflow/21.03
module load singularity/rpm

# Set environment variables
export NXF_SINGULARITY_CACHEDIR=/path/to/your/singularity/cache
export TOWER_ACCESS_TOKEN=<your_access_token>  # Optional

# Run the pipeline
nextflow run main.nf -resume -w work_dir \
    --genome /path/to/your/genome.fa \
    --chrom 29 \
    --val_chrom 21 \
    --test_chrom 25 \
    --window 200 \
    --peaks '/path/to/your/peaks/*.bed' \
    -with-tower  # Optional
```

#### Example with Cattle Data
```bash
nextflow run main.nf -resume -w work_dir \
    --genome /mnt/users/ngda/genomes/cattle/Bos_taurus.ARS-UCD1.2.dna_sm.toplevel.fa \
    --chrom 29 \
    --val_chrom 21 \
    --test_chrom 25 \
    --window 200 \
    --peaks '/mnt/SCRATCH/ngda/data/Cattle/*.bed' \
    -with-tower
```

## Configuration Parameters

### Core Parameters

| Parameter | Description | Default Value |
|-----------|-------------|---------------|
| `--genome` | Path to the reference genome FASTA file | `$baseDir/data/ref/genome.fa` |
| `--peaks` | Path to peak files (BED format) | `$baseDir/data/peak/*` |
| `--outdir` | Output directory for results | `results` |
| `--trace_dir` | Directory for trace and log files | `trace_dir` |

### Dataset Configuration

| Parameter | Description | Default Value |
|-----------|-------------|---------------|
| `--chrom` | Largest chromosome index for dataset building | `29` |
| `--val_chrom` | Chromosome used for validation | `21` |
| `--test_chrom` | Chromosome used for testing | `25` |
| `--window` | Genomic window size for analysis | `200` |

### Model Parameters

| Parameter | Description | Default Value |
|-----------|-------------|---------------|
| `--learning_rates` | Learning rates for hyperparameter tuning | `[1e-3, 1e-4, 5e-4, 5e-5]` |

**Note**: The `--chrom` parameter specifies the largest chromosome index. For example, setting `--chrom 29` will use chromosomes 1, 2, 3, ..., 28, 29 for dataset building.


## Output

- Results will be saved in the specified `--outdir` (default: `results`).
- Trace files for debugging and performance monitoring will be stored in `params.trace_dir` (default: `trace_dir`).


## Pre-trained Models

DeepFARM provides pre-trained DanQ model weights for multiple livestock species. These models have been trained on species-specific chromatin accessibility data and can be used for regulatory prediction tasks.

### Available Models

| Species | Model File | Download Link |
|---------|------------|---------------|
| Cattle | `cattle_DanQ.h5` | [Download](https://github.com/datngu/data/releases/download/v.0.0.4/cattle_DanQ.h5) |
| Chicken | `chicken_DanQ.h5` | [Download](https://github.com/datngu/data/releases/download/v.0.0.4/chicken_DanQ.h5) |
| Pig | `pig_DanQ.h5` | [Download](https://github.com/datngu/data/releases/download/v.0.0.4/pig_DanQ.h5) |
| Salmon | `salmon_DanQ.h5` | [Download](https://github.com/datngu/data/releases/download/v.0.0.4/salmon_DanQ.h5) |

### Usage

To use pre-trained models:

1. Download the appropriate model file for your species of interest
2. Place the model file in your working directory or specify the path in your pipeline configuration
3. The models can be used for regulatory impact prediction without additional training



## Troubleshooting

### Common Issues

#### Module Loading Errors
- **Issue**: `module: command not found`
- **Solution**: Ensure you're running on an HPC system with Environment Modules installed, or adapt the commands for your system

#### Singularity Cache Issues
- **Issue**: Permission errors with Singularity cache directory
- **Solution**: Ensure `NXF_SINGULARITY_CACHEDIR` points to a writable directory with sufficient space

#### Memory/Resource Errors
- **Issue**: Pipeline fails due to insufficient resources
- **Solution**: 
  - Review and adjust resource allocations in `nextflow.config`
  - Consider reducing the number of chromosomes or window size for initial testing
  - Check available memory and CPU cores on your HPC system

#### File Path Issues
- **Issue**: "No such file or directory" errors
- **Solution**: 
  - Verify all input file paths are correct and accessible
  - Use absolute paths when possible
  - Check file permissions

### Getting Help

1. Check the [Nextflow documentation](https://www.nextflow.io/docs/latest/index.html) for workflow-related issues
2. Review the `nextflow.config` file for system-specific configurations
3. Check pipeline logs in the `trace_dir` directory for detailed error messages

## Citation

**Manuscript**: "Sequence-based chromatin activity modeling and regulatory impact prediction of genetic variants in farmed animals using deep learning"

*Citation details will be updated upon publication*

