import os
import pandas as pd


def combine_bracken(dir_bracken_reports):
    """Combines bracken counts for several samples into one table.

    Parameters
    ----------
    dir_bracken_reports : str
        Pathname of directory that contains bracken abundance estimation files
        per samples.

    Returns
    -------
    Pandas.DataFrame with rows for features, columns for samples.
    Feature labels are NCBI taxonomy IDs.

    Notes
    -----
    We don't know which files in the given directory are bracken abundance
    estimation files.
    Therefore, we iterate over all files and try to a) parse the file as a tab
    separated table and b) check if the second column is named 'taxonomy_id'.
    More information about the file format:
    https://ccb.jhu.edu/software/bracken/index.shtml?t=manual
    """
    samples = []
    # walking over the given directory.
    # We don't know which files are actual bracken abundance estimation files.
    for _file in next(os.walk(dir_bracken_reports))[2]:
        try:
            sample_abund = pd.read_csv(dir_bracken_reports + '/' + _file,
                                       sep='\t', index_col=1)
        except IndexError:
            continue
        # we assume the file is a bracken abundance estimation file, if
        # a) it can be parsed by pandas
        # b) it's index is named 'taxonomy_id'
        if sample_abund.index.name != 'taxonomy_id':
            # this file does not look like a bracken Abundance Estimation file,
            # thus it will be skipped
            continue

        # we are collecting the bracken estimated kraken assigned read numbers
        sample_counts = sample_abund['new_est_reads']

        # infer sample name from filename and remove file extension if present
        sample_counts.name = os.path.splitext(_file)[0]

        # add resulting pd.Series to our collection of samples
        samples.append(sample_counts)

    # return a merged pd.DataFrame of all absolute estimated assigned reads
    return pd.concat(samples, axis=1).fillna(0).astype(int)
