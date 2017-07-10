# ratsnake_shotgun
Snakemake testbed for shotgun integration into Qiita

## Installation

To install the workflow environment, run `bash install.sh` from the `ratsnake_shotgun` directory. 

## Test data execution

To run on a simple set of test data, run:

```bash
export PATH=$PATH:$PWD/utree
source activate ratsnake_shotgun
snakemake all --use-conda --cores 2
```