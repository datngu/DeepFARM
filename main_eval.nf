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
params.models          = "$baseDir/data/*.h5"
params.test_tfr        = "$baseDir/data/*.tfr"

params.outdir          = "evaluation_results"
params.trace_dir       = "evaluation_trace_dir"




log.info """\
================================================================
                        DeepFARM evaluation
================================================================
    models              : $params.models
    test_tfr            : $params.test_tfr
    outdir              : $params.outdir
    trace_dir           : $params.trace_dir

================================================================
"""

nextflow.enable.dsl=2



workflow {
    
    Model_ch = Channel.fromPath(params.models, checkIfExists: true)
    TFR_ch = Channel.fromPath(params.test_tfr, checkIfExists: true).collect()
    EVAL_model(Model_ch, TFR_ch)

}





process EVAL_model {
    container 'ndatth/deepsea:v0.0.0'
    publishDir "${params.outdir}", mode: 'copy', overwrite: true
    memory '60 GB'
    cpus 8
    label 'with_1gpu'

    input:
    path model
    path tfr

    output:
    path("*_eval*")


    script:
    """
    base=\$(basename "$model" .h5)
    evaluate_model.py \
        --test *_fw.tfr \
        --model $model \
        --out \${base}_eval \
        --batch_size 1024

    """
}
