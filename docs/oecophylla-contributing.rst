Contributing Oecophylla modules
===============================

A module is a set of related Snakemake rules, along with installation 
instructions. 

To contribute a new module *foo*, you need a folder in ``./oecophylla`` that 
contains:

 1. **foo.rule**: a Snakemake-formatted file containing the rules for the module
 2. **foo.yaml**: a Conda environment file for installing dependencies for the module
 3. **foo.sh**: a Bash script for installing the module
 4. **README.md**: a Markdown file describing the steps performed by the module


The rule file
-------------

The rule file should be Snakemake formatted, and in the same idiom as the other
module rule files already in the repository. 

The rule file should have a series of rules that execute discrete computational 
steps, with names prefixed by the module name. At the end of the file, you 
should have a 'top-level' rule that has as inputs all necessary outputs from 
other rules in the module to produce the desired endpoint. 

For example, for module ``foo`` you might have something like this:

..  code-block:: yaml

    rule foo_step1:
        input:
            file.txt
        output:
            file.foo.txt
        run:
            shell('foo {input} > {output}')

    rule foo_step2:
        input: 
            file.foo.txt
        output:
            file.bar.txt
        run:
            shell('bar {input} > {output}')

    rule foo:
        input:
            file.bar.txt

Check the `Snakemake documentation <http://snakemake.readthedocs.io>`__ for 
specifics on formatting Snakemake rules.


The module environment
----------------------

Rules can be executed in their own environment, allowing tools with potentially
conflicting dependences to execute in the workflow.

In Oecophylla, we are specifying the environment for a rule's execution with
a line at the beginning of a shell execution block that executes the commands
necessary to initialize that environment. The necessary command is passed into
the ``params`` object in the rule specification from the ``config.yaml`` file.
This enables the use of multiple mechanisms for specifying environments -- for
example, a centralized install on a cluster could use ``module load foo`` while
a local test installation could use ``source activate oecophylla-foo``. 

To specify the environment, make sure to access the corresponding declaration
in your ``config.yaml`` file in the ``params`` portion of the Snakemake rule, and
then pass that during the shell execution block, as so:


..  code-block:: yaml

    rule foo1:
        input:
            file.txt
        output:
            file.foo.txt
        params:
            env = config['envs']['foo']
            # 'foo' here is a string in the config.yaml, and should evaluate
            # as a bash command -- e.g., source activate foo
        run:
            shell("""
                  set +u; {params.env}; set -u

                  foo {input} > {output})
                  """)

Note that any Python surrounding the ``shell()`` code block will be executed
within the base Oecophylla environment. 


The environment install
-----------------------

For purposes of testing and installation, we are requiring that each module
contains a script sufficient to install the environment. The script should be
named ``[module].sh`` and placed in the module directory. 

Ideally you can get away with a single Conda yaml file for each module. But if
necessary, it is also possible to have multiple yaml files for different
rules/tools in the module.
