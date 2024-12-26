#!/usr/bin/env nextflow
/*
========================================================================================
                          DeepFARM
========================================================================================
                DeepFARM Pipeline with nextflow.
                https://github.com/datngu/DeepFARM
                Author: Dat T Nguyen
                Contact: ndat<at>utexas.edu
----------------------------------------------------------------------------------------
*/





/*
 Define the default parameters
*/ 
params.genome          = "$baseDir/data/ref/genome.fa"
params.peaks           = "$baseDir/data/peak/*"

params.outdir          = "results"
params.trace_dir       = "trace_dir"

// running options
params.chrom           = 29 
params.val_chrom       = 21
params.test_chrom      = 25
params.window          = 200

params.learning_rates  = [1e-3, 1e-4, 5e-4, 5e-5]




log.info """\
================================================================
                        DeepFARM
================================================================
    genome              : $params.genome
    peaks               : $params.peaks
    outdir              : $params.outdir
    trace_dir           : $params.trace_dir


    chrom               : $params.chrom
    test_chrom          : $params.test_chrom
    val_chrom           : $params.val_chrom 
    window              : $params.window



================================================================
"""

nextflow.enable.dsl=2



workflow {
    
    // hyper params:learning rates
    Learning_rate_ch = channel.from(params.learning_rates)
    Chrom_ch = channel.from(1..params.chrom)

    INDEX_genome(params.genome)
    BIN_genome(INDEX_genome.out)

    ch_peaks = channel.fromPath(params.peaks, checkIfExists: true)

    BED_mapping(BIN_genome.out, ch_peaks)
    
    LABEL_generating(BED_mapping.out.collect())
    
    TFR_data_generating(LABEL_generating.out, BIN_genome.out, params.genome, Chrom_ch)
    
    DANQ_training(TFR_data_generating.out.collect(), Learning_rate_ch)
    DEEPSEA_training(TFR_data_generating.out.collect(), Learning_rate_ch)

    // Mymodel_training(TFR_data_generating.out, Learning_rate_ch)
}






// preprocessing data



process INDEX_genome {
    container 'ndatth/deepsea:v0.0.0'
    publishDir "${params.outdir}/genome", mode: 'symlink', overwrite: true
    memory '8 GB'
    cpus 1

    input:
    path "genome.fa"

    output:
    path("genome.fa*")


    script:
    """
    samtools faidx genome.fa
    """
}


process BIN_genome {
    container 'ndatth/deepsea:v0.0.0'
    publishDir "${params.outdir}/bed_files", mode: 'symlink', overwrite: true
    memory '8 GB'
    cpus 1

    input:
    path genome

    output:
    path("genome_window.bed")


    script:
    """
    generate_coordinate_onebed.py --genome genome.fa.fai --out genome_window.bed --window $params.window --chrom $params.chrom
    """
}


process BED_mapping {
    container 'ndatth/deepsea:v0.0.0'
    publishDir "${params.outdir}/bed_files", mode: 'symlink', overwrite: true
    memory '8 GB'
    cpus 1

    input:
    path bed_path
    path peak

    output:
    path("positive_${peak}")


    script:
    """
    bedtools intersect -a $bed_path -b ${peak} -wo -f 0.50 > positive_${peak}
    """
}


process LABEL_generating {
    container 'ndatth/deepsea:v0.0.0'
    publishDir "${params.outdir}/peak_labels", mode: 'symlink', overwrite: true
    memory '32 GB'
    cpus 1

    input:
    path bed_path

    output:
    path("*.txt.gz")


    script:
    """
    generate_seq_labels.py --input positive_* --out '.'
    """
}



process TFR_data_generating {
    container 'ndatth/deepsea:v0.0.0'
    publishDir "${params.outdir}/tfr_data", mode: 'symlink', overwrite: true
    memory '16 GB'
    cpus 2
    

    input:
    path lab
    path bed
    path genome
    val chr

    output:
    path("*.tfr")


    script:
    """

    generate_tfr.py --label ${chr}.txt.gz --bed $bed --genome $genome --pad_scale 5 --out ${chr}
  
    """
}


process DANQ_training{
    container 'ndatth/deepsea:v0.0.0'
    publishDir "${params.outdir}/train", mode: 'symlink', overwrite: true
    memory '60 GB'
    cpus 8
    label 'with_1gpu'
    

    input:
    path tfr
    val lr

    output:
    path("DanQ_model*")


    script:
    """
    mv ${params.val_chrom}_fw.tfr ${params.val_chrom}_fw.val
    mv ${params.val_chrom}_rc.tfr ${params.val_chrom}_rc.val

    mv ${params.test_chrom}_fw.tfr ${params.test_chrom}_fw.test
    mv ${params.test_chrom}_rc.tfr ${params.test_chrom}_rc.test
    
    train_danq.py --train *.tfr --val *_fw.val --out DanQ_model_${lr} --batch_size 1024 --lr ${lr}

    """
}


process DEEPSEA_training {
    container 'ndatth/deepsea:v0.0.0'
    publishDir "${params.outdir}/train", mode: 'copy', overwrite: true
    memory '60 GB'
    cpus 8
    label 'with_1gpu'
    

    input:
    path tfr
    val lr

    output:
    path("DeepSEA_model*")


    script:
    """
    mv ${params.val_chrom}_fw.tfr ${params.val_chrom}_fw.val
    mv ${params.val_chrom}_rc.tfr ${params.val_chrom}_rc.val

    mv ${params.test_chrom}_fw.tfr ${params.test_chrom}_fw.test
    mv ${params.test_chrom}_rc.tfr ${params.test_chrom}_rc.test
    
    train_deepsea.py --train *.tfr --val *_fw.val --out DeepSEA_model_${lr} --batch_size 1024 --lr ${lr}

    """
}

