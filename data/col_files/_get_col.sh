
#outdir=/mnt/ScratchProjects/Aqua-Faang/dat_projects/dl_project/


get_col() {
    spec=$1
    outdir=/mnt/ScratchProjects/Aqua-Faang/dat_projects/dl_project/
    file=/mnt/ScratchProjects/Aqua-Faang/dat_projects/dl_project/${spec}_deepfarm/results/peak_labels/10.txt.gz
    zcat "$file" | head -n 1 | tr '\t' '\n' | awk '{gsub("positive_", ""); print}' > "$outdir/${spec}_colnames.txt"
}

get_col "salmon"
get_col "pig"
get_col "cattle"
