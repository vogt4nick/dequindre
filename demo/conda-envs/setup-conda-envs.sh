#!/bin/bash

echo install conda=4.6 python=3.6...
conda install conda=4.6 python=3.6

echo install dequindre into base environment...
pip install $HOMEDIR/packages/dequindre-0.1.1.tar.gz

for env in $HOMEDIR/conda-envs/*.yml; do 
    echo create $env...
    conda env create -f $env 
done;
conda info -e