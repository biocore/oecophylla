# bash script to execute on test data in Barnacle environment

oecophylla workflow \
--test \
--cluster-config cluster.json \
--local-scratch /localscratch \
--workflow-type profile \
--profile ./ \
--output-dir ../barnacle_test_out \
-j 16 \
all