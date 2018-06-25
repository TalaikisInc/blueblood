#!/bin/bash

conda create --name blueblood python==3.6
source activate blueblood
conda install tensorflow -y
pip install -r requirements.txt
source deactivate
