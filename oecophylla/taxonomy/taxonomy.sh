#!/bin/bash
set -e

# the MetaPhlAn package contains the whole database, which is huge
# uncomment only when tests are necessary
# conda env create --name oecophylla-metaphlan2 -f oecophylla-metaphlan2.yaml --quiet > /dev/null

conda env create --name oecophylla-kraken -f oecophylla-kraken.yaml --quiet > /dev/null

# comment out all old shogun installation scripts

# currently shogun is a hack, running the install script until we
# have stable conda install
# conda env create --name oecophylla-shogun -f oecophylla-shogun.yaml --quiet > /dev/null

# source activate oecophylla-shogun

# echo $CONDA_PREFIX

# mkdir -p $CONDA_PREFIX/etc/conda/activate.d
# mkdir -p $CONDA_PREFIX/etc/conda/deactivate.d

# touch $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
# touch $CONDA_PREFIX/etc/conda/deactivate.d/env_vars.sh

# echo "#!/bin/sh" >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
# echo "export OLD_PATH=$PATH" >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
# echo "export PATH=$PATH:$PWD/utree" >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh


# echo "#!/bin/sh" >> $CONDA_PREFIX/etc/conda/deactivate.d/env_vars.sh
# echo "export PATH=$OLD_PATH" >> $CONDA_PREFIX/etc/conda/deactivate.d/env_vars.sh
# echo "unset OLDPATH" >> $CONDA_PREFIX/etc/conda/deactivate.d/env_vars.sh


# download UTree binary and add to path
# if hash wget 2>/dev/null; then
#     wget --quiet https://github.com/knights-lab/UTree/releases/download/v1.2/utree_1.2_linux.zip
# else
#     curl -s -L -o utree_1.2_linux.zip https://github.com/knights-lab/UTree/releases/download/v1.2/utree_1.2_linux.zip
# fi
# unzip utree_1.2_linux.zip -d utree > /dev/null
# chmod 755 utree/utree*
