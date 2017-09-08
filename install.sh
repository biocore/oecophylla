#!/bin/bash

# runs setup of base environment and database installs

# create conda env
conda env create --name oecophylla -f environment.yml

conda env create --name shotgun-humann2 -f envs/shotgun-humann2.yaml
conda env create --name shotgun-qc -f envs/shotgun-qc.yaml
# conda env create --name shotgun-shogun -f envs/shotgun-shogun.yaml
# currently shogun is a hack, running the install script until we 
# have stable conda install
bash envs/shotgun-shogun.sh

# download UTree binary and add to path
wget https://github.com/knights-lab/UTree/releases/download/v1.2/utree_1.2_linux.zip
unzip utree_1.2_linux.zip -d utree
chmod 755 utree/utree*

# unzip test db
bunzip2 test_data/shogun_test_db/phix.ctr.bz2