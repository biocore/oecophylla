Installing Oecophylla
=====================

Installing the Oecophylla wrapper
---------------------------------

To install the workflow environment, download the Oecophylla repository from
GitHub:

.. code-block:: bash

   git clone https://github.com/biocore/oecophylla.git


Then, change to the ``oecophylla`` directory and run the install script:

.. code-block:: bash

   cd oecophylla

   bash install.sh


This script is just there for convenience, and creates a Conda environment,
activates it, and pip installs the repository with the 'editable' flag, so
that subsequent git updates to the repository will be reflected. You can
**alternatively** run these commands directly: 

.. code-block:: bash
   :caption: **Don't actually run this** if you've already run install.sh

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

   oecophylla install --all


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

