Installing Oecophylla
=====================

Installing the Oecophylla wrapper
---------------------------------

To install the workflow environment, download the Oecophylla repository from
GitHub:

.. code-block:: bash

   git clone https://github.com/biocore/oecophylla.git


Then, run ``bash install.sh`` from the ``oecophylla`` directory.

This will execute the following commands: 

.. code-block:: bash

   conda env create --name oecophylla -f environment.yml

   source activate oecophylla

   pip install -e .


Installing modules
------------------

The code to execute module commands is all located in the Oecophylla repository.
The actual tools called by these modules, however, must be installed separately
in their own environemnts. 

Oecophylla can install these per-module environments automatically using Conda.
To see a list of modules available to install, make sure you are in the
Oecophylla conda environment, and then execute:

.. code-block:: bash

   oecophylla install --avail


You can install all of these modules by executing:

.. code-block:: bash

   oecophylla install all


Fair warning: installing all modules will take a bit of time. 

To install a specific set of modules, you can specify them directly as
positional arguments. For example:

.. code-block:: bash

   oecophylla install qc taxonomy


will install the ``qc`` and ``taxonomy`` module Conda environments.


Test data execution
-------------------

We have included a minimal set of example data and test databases sufficient
to execute a test run of the workflow. 

To run these test data, you will need to first install the test databases:

.. code-block:: bash

   oecophylla install --tests


You can then run the test data on any module that you have installed,
specifying only the desired output directory and the module to test:

.. code-block:: bash

   oecophylla workflow --test -o test_out qc taxonomy

