import pandas as pd


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