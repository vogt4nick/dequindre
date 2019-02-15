#!/bin/bash

echo install conda=4.6...
conda install conda=4.6

echo install dequindre into base environment...
pip install $DEQUINDRE_DIR/packages/dequindre-0.2.0.tar.gz

for env in $DEQUINDRE_DIR/conda-envs/*.yml; do 
    echo create $env...
    conda env create -f $env 
done;
conda info -e