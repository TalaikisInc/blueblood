#!/bin/bash

conda create --name blueblood python==3.7
source activate blueblood
conda install tensorflow -y
conda install pymc3 -y
conda install cython -y
pip install -r requirements.txt
source deactivate
