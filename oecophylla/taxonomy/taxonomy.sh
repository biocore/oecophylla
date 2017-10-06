#!/bin/bash
set -e

# the MetaPhlAn package contains the whole database, which is huge
# uncomment only when tests are necessary
conda env create --name oecophylla-metaphlan2 -f oecophylla-metaphlan2.yaml --quiet > /dev/null

conda env create --name oecophylla-kraken -f oecophylla-kraken.yaml --quiet > /dev/null

conda env create --name oecophylla-centrifuge -f oecophylla-centrifuge.yaml --quiet > /dev/null

# currently shogun is a hack, running the install script until we
# have stable conda install
conda env create --name oecophylla-shogun -f oecophylla-shogun.yaml --quiet > /dev/null

source activate oecophylla-shogun

echo $CONDA_PREFIX

cd $CONDA_PREFIX/bin

wget https://github.com/knights-lab/UTree/releases/download/v2.0c/utree-search_gg
chmod 755 utree-search_gg

wget https://github.com/knights-lab/BURST/releases/download/v0.99.4a/burst_linux_DB15
chmod 755 burst_linux_DB15