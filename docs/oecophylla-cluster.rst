Running Oecophylla on a cluster
===============================

The previous commands will run Oecophylla locally, on the machine that is 
executing the Oecophylla script. However, because shotgun datasets tend to be 
huge, you will most likely want to run your analysis on a cluster. 

Snakemake (and thus Oecophylla) are built to run in a cluster environment.

There are currently two primary ways to run Oecophylla on a cluster: generic
cluster execution (currently enabled with Torque/PBS and SLURM schedulers)
and **cluster profile** execution.


Generic cluster execution
-------------------------

In this mode, Snakemake will create a script for each job and submit it to the
cluster scheduler. It will then watch for the expected output files for the
job. When it finds them, it will consider the job done and move on to the next.
Snakemake will launch as as many jobs in parallel as possible, up to the limit
specified with the -j/--jobs flag. 

Note: In this mode, Snakemake has no direct awareness of the job status: 
sometimes, this can lead to unexpected behavior.


Gather inputs
~~~~~~~~~~~~~

As for local execution, you will need input data, a parameters file, and an 
environment file. (Note that the environment file may be modified to specify 
global environment configuration commands [i.e. using GNU Modules] rather than 
the Oecophylla-installed Conda environments.)

In addition, you will need a ``cluster.json`` file, which specifies the 
resources to request from the cluster job scheduler for each rule.

These may need to be modified for the specific cluster you are using. We've 
provided some example files suitable for running full-sized datasets on the 
Knight Lab's *Barnacle* compute cluster:

1. **Input reads directory**: ``test_data/test_reads``
2. **Parameters file**: ``cluster_configs/barnacle/tool_params.yml``
3. **Environment file**: ``cluster_configs/barnacle/envs.yml``
4. **Cluster file**: ``cluster_configs/cluster.json``

We have also provided a ``cluster.json`` file containing defaults that should
be suitable for most instances of the job execution. Note that running on
datasets with fewer sequences will demand fewer resources for some jobs, and it
may be possible to execute more efficiently by changing these defaults.


Run the Oecophylla launch script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Running Oecophylla from the cluster is otherwise identical to running locally, 
with the exception that you must specify a cluster workflow type with the ``
--workflow-type`` parameter and provide a path to a ``cluster.json`` file with 
the ``--cluster-config`` parameter.

You will also want to provide a path to your local scratch space for cluster
execution---this is typically a fast hard drive located in the cluster node
itself, and saves the cluster from having to write certain types of data to
the networked cluster filesystem. On our Barnacle cluster, this local scratch
space is accessed at ``/localscratch``. Oecophylla jobs are all optimized to
use local scratch space wherever possible.

From the Barnacle login node, enter the main Oecophylla Conda environment and 
run the following command:

..  code-block:: bash
    :caption: note that the backslash here is just escaping the return
        
    oecophylla workflow \\
    --workflow-type torque \\
    --cluster-config cluster_configs/cluster.json \\
    --input-dir test_data/test_reads \\
    --params cluster_configs/barnacle/tool_params.yml \\
    --envs cluster_configs/barnacle/envs.yml \\
    --jobs 16 \\
    --local-scratch /localscratch \\
    --output-dir cluster_test qc

Note that we have specified ``--workflow-type torque``. This tells Oecophylla 
to submit jobs to the cluster using the ``qsub`` command, which is appropriate 
to Barnacle. Other valid options are ``slurm`` (e.g. Comet uses the Slurm job 
scheduler), ``local`` (the default), and ``profile``.


Cluster execution using 'profiles'
----------------------------------

To simplify execution in specific cluster environments, it is also possible to
provide Oecophylla/Snakemake with a path to a cluster profile directory.

This directory contains configuration information particular to a specific
cluster, simplifying execution and allowing tweaks to improve performance and
reliability. This can include, for example, cluster status scripts that allow
Snakemake to query the scheduler directly for updates on job status.

Note that we have also included cluster-specific environment (``envs.yml``)
and parameters (``tool_params.yml``) files. These may include things like the
correct paths to centralized database installations or centralized environment
config commands, and are suggested as starting points for running your own
data on these clusters.


Run the Oecophylla launch script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Available cluster configuration profiles are found in ``cluster_configs``. To 
use a specific cluster profile, provide the directory path to Oecophylla using 
the ``--profile`` flag, and pass 'profile' to the ``--workflow-type`` flag:

..  code-block:: bash

    oecophylla workflow \\
    --workflow-type profile \\
    --profile cluster_configs/barnacle \\
    --cluster-config cluster_configs/cluster.json \\
    --input-dir test_data/test_reads \\
    --params cluster_configs/barnacle/tool_params.yml \\
    --envs cluster_configs/barnacle/envs.yml \\
    --local-scratch /localscratch \\
    --output-dir cluster_test qc

Note that in this case, the number of simultaneous jobs is being specified in
the file ``cluster_configs/barnacle/config.yaml``, along with other
cluster-specific Snakemake configuration values. 


Running the built-in cluster profile test script
------------------------------------------------

The above examples are very similar to how you would execute on test data: you
manually specify filepaths for each required file.

However, if you just want to run a quick test to make sure everything is
working, there are included test scripts for each of the cluster profiles.
These will run using the ``--test`` flag in Oecophylla, and thus will write
outputs to ``<oecophylla directory>/test_out`` and use the included minimal
test databases.

If you run these, make sure to install the test databases first using
``oecophylla install --tests``.

You can execute the test scripts as so:

..  code-block:: bash

    bash cluster_configs/barnacle/test_barnacle.sh

This will try to run *all* available steps using Barnacle profile and the
included test data and test databases.


Notes on cluster execution
--------------------------

Execution on a cluster presents some specific challenges to the Snakemake
job tracking system. The following are some things to keep in mind:

Filesystem latency
~~~~~~~~~~~~~~~~~~

Cluster filesystems can have *latency*, meaning that it can take some time
after a file is written by a job before it is seen by the main Snakemake
process. This can cause problems if Snakemake sees a job finish but can't find
its outputs.

You can have Snakemake allow additional time to deal with latency by passing
'--latency-wait/-w' to Snakemake using the '--snakemake-args' flag as so:

``--snakemake-args '-w 90'``

When executing in profile mode with the ``cluster_configs/barnacle`` profile, 
the latency wait parameter is set to 90 by default.


Cluster logs
~~~~~~~~~~~~

By default, the cluster will write stdout and stderr to log files. The very
large number of these small log files can cause problems on cluster
filesystems, so by default Oecophylla sends them to ``/dev/null`` instead of
saving them.

In some cases, saving these log files can help diagnose errors in execution. To
enable this, you will need to set ``output`` and ``error`` values in the
``cluster.json`` file. (The provided ``cluster.json`` files point to
``/dev/null``.)

..  code-block:: json

    "__default__": {
        "time"      : "4:00:00",
        "n"         : 1,
        "mem"       : 4,
        "output"    : "cluster_logs/{rule}.{wildcards}.out",
        "error"     : "cluster_logs/{rule}.{wildcards}.err"
    },

You can do this for the ``__default__`` item, in which case all jobs will save
cluster log files, or leave ``__default__`` as ``/dev/null`` and add ``output``
and ``error`` values for specific jobs.

**In generic mode:**
 - set ``output`` and ``error`` values in cluster.json
 - add the ``--cluster-logs`` flag when executing ``oecophylla workflow``

**In profile mode:**
  - set ``output`` and ``error`` values in cluster.json in profile dir

In both cases, **make sure the specified cluster_logs directory exists** prior
to execution.
