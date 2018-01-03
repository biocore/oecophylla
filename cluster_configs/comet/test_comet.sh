mkdir -p test_out/cluster_logs
mkdir -p test_out/results/qc/cluster_logs
mkdir -p test_out/results/assemble/cluster_logs
mkdir -p test_out/results/raw/cluster_logs
mkdir -p test_out/results/taxonomy/cluster_logs
mkdir -p test_out/results/function/cluster_logs

oecophylla workflow \
--test \
--local-scratch /localscratch \
--cluster-config ../cluster.json \
--workflow-type profile \
--profile ./ \
--output-dir test_out \
-j 16 \
all