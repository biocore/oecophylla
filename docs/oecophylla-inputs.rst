More about inputs, parameters, and environments
===============================================

Fundamentally, Oecophylla is *workflow manager*, which means it's here to tell
the computer (or cluster) what to do to move a bunch of samples through a
series of steps. We've tried to provide some sensible starting points that make
it easy to perform basic processing on standard metagenomic datasets, but
you'll need to be able to make some modifications to fit your needs.

Ultimately, you have to know how to tell Oecophylla:
  - where your data are (**input**)
  - what you want to do with them (**parameters**)
  - how to do actually run the programs (**environments**)

Each of these three elements are stored in a single file called ``config.yaml``
that Oecophylla creates in the ``output-dir``. Subsequent runs in the same
output directory will automatically use this ``config.yaml`` file if it is
found. 

You can also have Oecophylla **only** output the ``config.yaml`` (and not do
the workflow run itslef) by passing the ``--just-config`` flag.


Input data
----------

Oecophylla operates on a *files per sample* basis. It has a concept of
*samples*, and needs a way to associate *samples* with input sequence *files*.
Once it does this first association, Oecophylla will combine all the forward
and all the reverse read files per sample (for example, it the sample was run
across multiple lanes) and keep track of things from there.

There are two automatic ways and one manual way to tell Oeocophylla how to find
your input data:


The quick way
~~~~~~~~~~~~~

If all of your samples are in the same folder, and **if they follow the
standard Illumina naming convention** [1]_, you can just pass the input folder to
``oecophylla workflow`` and it will guess sample names from file names. 


..  code-block:: bash
    :caption: this will find all six samples in the included test_reads 
    directory
    
    oecophylla workflow \
    --input-dir test_data/test_reads 


The precise way
~~~~~~~~~~~~~~~

You can also pass Oecophylla the Illumina-formatted sample sheet that was used
to demultiplex the samples. This allows you to use different sample names for
your samples than what can be deduced from the read names themselves. This also
allows you to only run a subset of the samples from the run, by only including
those lines of the sample sheet. This also depends on your files being named
following standard Illumina naming conventions [1]_. 

In this case, provide the sample name *you want Oecophylla to use* in a column
in the Sample Sheet called 'Description', and then pass both the input
directory and the path to the sample sheet to Oecophylla: 

..  code-block:: bash
    :caption: this will only run two of the 6 test samples provided:
    
    oecophylla workflow \
    --input-dir test_data/test_reads \
    --sample-sheet test_data/test_config/example_sample_sheet.txt


The manual way
~~~~~~~~~~~~~~

If you want to get creative, or your files don't follow standard Illumina
naming conventions [1]_, you can just create or modify your own ``config.yaml``
file. Oecophylla will look for a ``samples`` block , with ``forward`` and
``reverse`` levels for each sample. Reads should be provided as a *matched*
list to each of these levels, as so:


..  code-block:: yaml
    :caption: this is not recommended but some of you will do it anyway

    samples:
      sample_S22205:
        forward:
        - test_data/test_reads/S22205_S104_L001_R1_001.fastq.gz
        reverse:
        - test_data/test_reads/S22205_S104_L001_R2_001.fastq.gz
      sample_S22282:
        forward:
        - test_data/test_reads/S22282_S102_L001_R1_001.fastq.gz
        reverse:
        - test_data/test_reads/S22282_S102_L001_R2_001.fastq.gz


Parameters
----------

Oecophylla wraps a lot of tools, and some subset of parameters for these tools
will be available to specify in a **parameters file**. An example parameters
file is provided in ``test_data/test_config/test_params.yml``. The parameters
file is combined with information about the samples and environments in the
single ``config.yaml`` file (which in principle should be enough to reproduce
an entire analysis).

This parameters file also includes paths to the databases used for each tool.
The included ``test_params.yml`` file includes paths to the tiny test databases
we package to verify installation. For example, the following portion of the
``test_params.yml`` file links to the test **humann2** databases, along with **Atropos** parameters suitable for trimming Kapa HyperPlus libraries:

..  code-block:: yaml
    :caption: this has *relative* file paths, because executing the test runs with the --test parameter always produces outputs with ``test_data`` linked in the output directory

    atropos: ' -a GATCGGAAGAGCACACGTCTGAACTCCAGTCAC -A GATCGGAAGAGCGTCGTGTAGGGAAAGGAGTGT
      -q 15 --minimum-length 100 --pair-filter any'
    humann2:
      aa_db: test_data/test_dbs/uniref50_mini
      nt_db: test_data/test_dbs/chocophlan_test
      other: ''

If you're executing Oecophylla on your own computer or cluster, you'll want to
download appropriate databases and create a ``params.yml`` with the appropriate
paths. We've included one set up with default databases available on our
Barnacle cluster. For example, here's the same portion of the the parameters
file in ``cluster_configs/barnacle/tool_params.yml``:

..  code-block:: yaml
    :caption: notice that this has *absolute* file paths

    atropos: ' -a GATCGGAAGAGCACACGTCTGAACTCCAGTCAC -A GATCGGAAGAGCGTCGTGTAGGGAAAGGAGTGT
      -q 15 --minimum-length 100 --pair-filter any'
    humann2:
      aa_db: /databases/humann2_data/uniref90/uniref
      nt_db: /databases/humann2_data/full_chocophlan.v0.1.1/chocophlan
      other: ''

When I'm running Oecophylla, I create a copy of my defaults parameters file in
the project output directory I'm using and modify it as necessary.


Environments
------------

Similar to the parameters file, Oecophylla needs an **environments file** to
tell the shell doing the execution of each job how to set up the environment
for that job [2]_. This file contains a one-line command sufficient to set up
the environment for each module, which is executed at the beginning of each
job run from that module. We've provided default ``envs.yml`` files in the
``test_data/test_config/test_envs.yml`` and
``cluster_configs/barnacle/envs.yml`` files suitable for running standard
analysis using the oecophylla-installed module Conda environments. They look
like this:

..  code-block:: yaml

    humann2: source activate oecophylla-humann2
    qc: source activate oecophylla-qc
    raw: source activate oecophylla-qc

Eventually, we will install some standard module environments on Barnacle
centrally using the GNU Modules system. To use these environments once they
are available, we will change the lines per-module in
``cluster_configs/barnacle/envs.yml`` to look something like this:

..  code-block:: yaml

    humann2: module load humann2
    qc: module load oecophylla-qc
    raw: module load oecophylla-qc


.. [1] as in ``sample1_S001_L001_R1_001.fastq.gz``, where ``sample1`` is 
   followed by an index, lane, read, and run number and has the ``.fastq.gz``
   extension.

.. [2] This slightly reproduces Snakemake's built-in conda environment
   specification feature. Why not use the former? We did this so that central
   execution on a shared cluster could take advantage of centrally installed
   environments per module, freeing people from having to maintain their own
   module installations. 
