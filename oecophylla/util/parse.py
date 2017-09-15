import os
import re
import pandas as pd
import copy
from io import StringIO


# Option 1 : parse samples from directory
def illumina_filenames_to_df(filepaths, pattern = None, column_names = None):
    """ Generates sample sheet from filenames using a regex pattern.

    Parameters
    ----------
    filepaths: list of str
        List of file paths to parse
    pattern: str, optional
        Regex pattern to recognize the filenames, to load into the
        sample sheet.
        default: '^((.+?)_(S\d+)_(L\d+)_(R[12])_(\d+)\.(.+))$'
    column_names: list, optional
        Column names for the generated sample sheet.  Note that this
        is assumed to be in the same ordering as the regex pattern.
        default: ['File', 'Sample', 'Index', 'Lane',
                  'Read', 'Run', 'Extension']
    Returns
    -------
    df : pd.DataFrame
       Sample sheet dataframe with all of the sample information.

    Notes
    -----
    This function is very illumina specific.
    """
    if pattern is None:
        pattern = '^((.+?)_(S\d+)_(L\d+)_(R[12])_(\d+)\.(.+))$'
    if column_names is None:
        column_names = ['File', 'Sample', 'Index', 'Lane',
                        'Read', 'Run', 'Extension']
    p = re.compile(pattern)
    df = pd.DataFrame(columns = column_names)

    for f in filepaths:
        m = p.match(f)
        if m:
            df = df.append(dict(zip(column_names, m.groups())),
                           ignore_index = True)
    return df


def extract_sample_reads(df, seq_dir,
                         sample_col='Sample',
                         read_col='Read',
                         file_col='File'):
    """ Extracts all files according to their associated samples.

    Parameters
    ----------
    df : pd.DataFrame
       Sample sheet dataframe with all of the sample information.
    seq_dir : str
       Input directory containing all of the sample files.
    sample_col : str
       Column name for the samples in the sample sheet.
    read_col : str
       Column name for the read orientation in the sample sheet.
    file_col : str
       Column name for the file name in the sample sheet.

    Returns
    -------
    dict of list of str
       Samples with a list of their forward and reverse files.

    Notes
    -----
    This function is very illumina specific, strictly assuming that
    the fwd reads are denoted by `R1` and the reverse reads are denoted
    by `R2`.
    """
    sample_reads_dict = {}

    samples = list(df[sample_col].unique())

    for s in samples:
        fwd = df.loc[(df[sample_col] == s) & (df[read_col] == 'R1'), file_col]
        rev = df.loc[(df[sample_col] == s) & (df[read_col] == 'R2'), file_col]
        f_fps = sorted(list(fwd.values))
        r_fps = sorted(list(rev.values))

        sample_reads_dict[s] = {'forward': [os.path.join(seq_dir, x) for x in f_fps],
                                'reverse': [os.path.join(seq_dir, x) for x in r_fps]}

    return sample_reads_dict


def extract_sample_paths(seq_dir):
    """ Obtain the sample paths.

    Parameters
    ----------
    seq_dir : str
       Input directory containing all of the sample files.

    Returns
    -------
    dict of list of str
       Samples with a list of their forward and reverse files.
    """
    fps = os.listdir(seq_dir)

    files_df = illumina_filenames_to_df(fps)
    sample_reads_dict = extract_sample_reads(files_df, seq_dir)

    return sample_reads_dict


def add_filter_db(sample_fp_dict, db_fp, samples = None,
                  filter_col='filter_db'):
    """ Add in a database for filtering out contaminant reads.

    This is useful for filtering out reads from other sources
    such as human DNA.

    Parameters
    ----------
    sample_fp_dict : dict of list of str
       Samples with a list of their forward and reverse files.
    db_fp : str
       Filepath of the database.
    samples : list
       List of sample names.
    filter_col : str
       Keyword name for the filtering database (default: 'filter_db')

    Returns
    -------
    dict of list of str
       Samples with a list of their forward and reverse files.
    """

    if samples is None:
        samples = set(sample_fp_dict)

    samples_dict = copy.deepcopy(sample_fp_dict)

    for s in samples_dict:
        if s in samples:
            samples_dict[s][filter_col] = db_fp
        elif filter_col in samples_dict[s]:
            continue
        else:
            samples_dict[s][filter_col] = None

    return(samples_dict)

# Option 2: read samples from sample sheet
def read_sample_sheet(f, sep='\t', comment='#'):
    """ Outputs a dataframe from a sample sheet

    Parameters
    ----------
    f : str
       File name for reading in the sample sheet information.
    sep : str
       Delimiter for parsing the pandas input.

    Returns
    -------
    data_df : pd.DataFrame
       DataFrame containing the sample sheet information.


    """
    data = False
    data_lines = ''
    with open(f) as fh:
        for line in fh:
            if data:
                if line.startswith('[') or line.strip() == '':
                    data = False
                    continue
                data_lines += line
            elif line.startswith('[Data]'):
                data = True
                continue
            else:
                continue
    data_df = pd.read_csv(StringIO(data_lines),
                          sep=sep, comment=comment)
    return(data_df)

def extract_samples_from_sample_sheet(sample_sheet_df, seq_dir,
                                      name_col='Description',
                                      sample_col='Sample',
                                      lane_col='Lane',
                                      file_col='File',
                                      read_col='Read',
                                      prefix_col='Sample_ID'):
    """ Obtains sample paths from a sample sheet.

    Parameters
    ----------
    sample_sheet_df : pd.DataFrame
       DataFrame containing the sample sheet information.
    seq_dir : str
       Input directory containing all of the sample files.
    sample_col : str
       Column name for the samples in the sample sheet.
    name_col : str
       Column name indicating the true name of the sample.
    lane_col : str
       Column name for the lane in the sample sheet.
    read_col : str
       Column name for the reads in the sample sheet.
    file_col : str
       Column name for the filename in the sample sheet.
    prefix_col : str
       Column name for the sample id in the sample sheet.

    Returns
    -------
    dict of list of str
       Samples with a list of their forward and reverse files.

    """
    sample_reads_dict = {}
    samples = list(sample_sheet_df[name_col].unique())
    fps = os.listdir(seq_dir)
    files_df = illumina_filenames_to_df(fps)

    # get the subset of sample sheet rows for that sample
    for s, sample_rows in sample_sheet_df.groupby(name_col):

        f_fps, r_fps = [], []

        # iter across subset table and find file corresponding to each row
        for idx, row in sample_rows.iterrows():
            lane = 'L{0:03d}'.format(row[lane_col])
            f_fps.extend(files_df.loc[(files_df[sample_col] == row[prefix_col]) &
                                      (files_df[lane_col] == lane) &
                                      (files_df[read_col] == 'R1'),
                                      file_col].values)

            r_fps.extend(files_df.loc[(files_df[sample_col] == row[prefix_col]) &
                                      (files_df[lane_col] == lane) &
                                      (files_df[read_col] == 'R2'),
                                      file_col].values)

        f_fps = sorted(f_fps)
        r_fps = sorted(r_fps)

        sample_reads_dict[s] = {
            'forward': [os.path.join(seq_dir, x) for x in f_fps],
            'reverse': [os.path.join(seq_dir, x) for x in r_fps]
        }

    return(sample_reads_dict)
