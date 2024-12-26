FROM nfcore/base:2.1

LABEL authors="Dat T Nguyen - ndat<at>utexas.edu" \
      description="Docker image containing all requirements for running deep learning models" 

ENV TZ='Europe/Oslo'
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


RUN apt-get update && apt-get install -y 
 

ADD environment.yml /
RUN conda install mamba -n base -c conda-forge -y
RUN mamba env create -f /environment.yml
#RUN conda clean --tarballs --yes
ENV PATH /opt/conda/envs/env/bin:$PATH

#RUN R -e "install.packages('R.utils', repos='http://cran.us.r-project.org')"
#RUN R -e "install.packages('data.table', repos='http://cran.us.r-project.org')"