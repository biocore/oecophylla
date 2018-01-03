Running Oecophylla locally
==========================

For this tutorial, we'll analyze a pair of shallowly sequenced  microbiome 
samples distributed with the repository. They are located in ``oecophylla/
test_data/test_reads``.

This tutorial essentially duplicates the automatic execution of test data
above, walking you through each step.

Gather inputs
-------------

We need three inputs to execute:

1. **Input reads directory**: ``test_data/test_reads``
2. **Parameters file**: ``test_data/test_config/test_params.yml``
3. **Environment file**: ``test_data/test_config/test_envs.yml``

The *input reads* should be the gzipped raw demultiplexed Illumina reads, with 
filenames conforming to the Illumina bcl2fastq standard (e.g. 
sample_S102_L001_R1_001.fastq.gz). 

The *environment file* simply lists the commands necessary to invoke the 
correct environment for each module. The included example file specifies the 
commands necessary for the Oecophylla-installed Conda environments, but these 
can be changed if, for example, you have appropriate environments specified as 
modules on a cluster.

The *parameters file* specifies the parameters for each tool being executed, 
including paths to the relevant databases.

Information from these three files is combined by Oecophylla into a single ``
config.yaml`` configuration file and placed in the output directory of a run. 
This serves as complete record of the settings chosen for execution of a run, 
as well as instructions for restarting or extending the processing on a 
dataset for subsequent invokations of Oecophylla. 


Run QC with Oecophylla
----------------------

To run a simple workflow, executing read trimming and QC summaries, run the 
following from the Oecophylla directory:

..  code-block:: bash
    :caption: note that the backslash here is just escaping the return
    
    oecophylla workflow 
    --input-dir test_data/test_reads 
    --params test_data/test_config/test_params.yml 
    --envs test_data/test_config/test_envs.yml 
    --output-dir test_output qc"

Then go get a cup of coffee. 

\...

When you come back, you will find a directory called ``test_output``. 

Inside of ``test_output`` will be the configuration file ``config.yaml``.

Also inside of ``test_output`` will be a folder called ``results``. This 
contains... well, you know.

Take a look at the file ``test_out/results/qc/multiQC_per_sample/
multiqc_report.html``. This is a portable HTML-based summary of the FastQC 
quality information from each of your samples. 


Run additional modules
----------------------

Now that you have initiated an Oecophylla run, you can call subsequent modules 
without providing paths for the three above inputs. Simply providing the 
output directory and module to execute will be enough: Oecophylla will find 
the ``config.yaml`` file in the output directory, and pick up where it left 
off. 

To continue with the ``taxonomy`` and ``function`` modules on the previous 
outputs, you can now simply run:

..  code-block:: bash

    oecophylla workflow --output_dir test_output taxonomy function

Oecophylla will find the outputs from the ``qc`` module, using these cleaned 
reads as inputs to the next steps.


Results
-------

The ``results`` directory will contain a separate folder for each module in 
the analysis workflow. 

These modules each will list per-sample outputs---for example, trimmed reads 
or assembled contigs---in per-sample directories within the module directory. 

Combined outputs---for example, the MultiQC summaries or combined biom table 
taxonomic summaries---will be found in their own dictories within the primary 
module directory.
