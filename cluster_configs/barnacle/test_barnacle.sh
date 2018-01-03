# bash script to execute on test data in Barnacle environment

mkdir -p test_out/cluster_logs

oecophylla workflow \
--test \
--cluster-config cluster_configs/cluster_test.json \
--local-scratch /localscratch \
--workflow-type profile \
--profile cluster_configs/barnacle \
-j 16 \
all
