import pandas as pd
import biom
from biom.util import biom_open


def combine_profiles(profiles):
    """Combines profiles for several samples into one table.

    Parameters
    ----------
    profiles : iterable((str, str))
        An iterable of tuples, where the second component is the filepath
        pointing to a profile (format: feature<tab>count), while the first
        component defines a sample name for the profile.

    Returns
    -------
    Pandas.DataFrame with rows for features, columns for samples.
    """
    samples = [pd.read_table(file, index_col=0, names=[name])
               for name, file in profiles]
    return pd.concat(samples, axis=1).fillna(0).astype(int)


def combine_bracken(bracken_outputs):
    """Combines bracken counts for several samples into one table.

    Parameters
    ----------
    bracken_outputs : Iterable((str, str))
        An iterable of tuples, where the second component is the filepath
        pointing to a bracken output files, the first component defines a
        sample name for the bracken output.

    Returns
    -------
    Pandas.DataFrame with rows for features, columns for samples.
    Feature labels are NCBI taxonomy IDs. Sample labels are obtained from first
    components of passed iterable.

    Notes
    -----
    More information about the bracken file format:
    https://ccb.jhu.edu/software/bracken/index.shtml?t=manual
    """
    samples = []
    # walking over the given directory.
    # We don't know which files are actual bracken abundance estimation files.
    for (samplename, _file) in bracken_outputs:
        sample_abund = pd.read_csv(_file, sep='\t', index_col=1)

        # we are collecting the bracken estimated kraken assigned read numbers
        sample_counts = sample_abund['new_est_reads']

        # infer sample name from filename and remove file extension if present
        sample_counts.name = samplename

        # add resulting pd.Series to our collection of samples
        samples.append(sample_counts)

    # return a merged pd.DataFrame of all absolute estimated assigned reads
    return pd.concat(samples, axis=1).fillna(0).astype(int)


def pandas2biom(file_biom, table):
    """ Writes a Pandas.DataFrame into a biom file.

    Parameters
    ----------
    file_biom: str
        The filename of the BIOM file to be created.
    table: a Pandas.DataFrame
        The table that should be written as BIOM.

    Returns
    -------
    Nothing
    """
    bt = biom.Table(table.values,
                    observation_ids=list(map(str, table.index)),
                    sample_ids=table.columns)

    with biom_open(file_biom, 'w') as f:
        bt.to_hdf5(f, "example")
