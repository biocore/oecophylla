# bash script to execute on test data in Barnacle environment

mkdir -p test_out/cluster_logs

oecophylla workflow \
--test \
--cluster-config cluster_configs/cluster_test.json \
--local-scratch '/scratch/$USER/$SLURM_JOB_ID' \
--workflow-type profile \
--profile cluster_configs/comet \
-j 16 \
all
