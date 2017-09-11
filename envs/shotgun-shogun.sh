conda env create --name shotgun-shogun -f envs/shotgun-shogun.yaml

source activate shotgun-shogun

echo $CONDA_PREFIX

mkdir -p $CONDA_PREFIX/etc/conda/activate.d
mkdir -p $CONDA_PREFIX/etc/conda/deactivate.d

touch $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
touch $CONDA_PREFIX/etc/conda/deactivate.d/env_vars.sh

echo "#!/bin/sh" >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
echo "export OLD_PATH=$PATH" >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
echo "export PATH=$PATH:$PWD/utree" >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh


echo "#!/bin/sh" >> $CONDA_PREFIX/etc/conda/deactivate.d/env_vars.sh
echo "export PATH=$OLD_PATH" >> $CONDA_PREFIX/etc/conda/deactivate.d/env_vars.sh
echo "unset OLDPATH" >> $CONDA_PREFIX/etc/conda/deactivate.d/env_vars.sh

