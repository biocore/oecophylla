import unittest
import pandas as pd
from oecophylla.util.parse import parse_filenames_to_df
import pandas.util.testing as pdt


class TestParse(unittest.TestCase):

    def test_parse_filenames_to_df(self):
        fnames = [
            'S22205_S104_L001_R1_001.fastq.gz',
            'S22400_S101_L001_R1_001.fastq.gz',
            'S22205_S104_L001_R2_001.fastq.gz',
            'S22400_S101_L001_R2_001.fastq.gz',
            'S22207_S103_L001_R1_001.fastq.gz',
            'S22401_S100_L001_R1_001.fastq.gz',
            'S22207_S103_L001_R2_001.fastq.gz',
            'S22401_S100_L001_R2_001.fastq.gz',
            'S22282_S102_L001_R1_001.fastq.gz',
            'S22402_S105_L001_R1_001.fastq.gz',
            'S22282_S102_L001_R2_001.fastq.gz',
            'S22402_S105_L001_R2_001.fastq.gz'
        ]
        df = parse_filenames_to_df(fnames)
        exp_df = pd.DataFrame(
            {
                'File': fnames,
                'Sample': ['S22205', 'S22400', 'S22205', 'S22400',
                           'S22207', 'S22401', 'S22207', 'S22401',
                           'S22282', 'S22402', 'S22282', 'S22402'],
                'Index': ['S104', 'S101', 'S104', 'S101', 'S103',
                          'S100', 'S103', 'S100', 'S102', 'S105',
                          'S102', 'S105'],
                'Lane': ['L001']*12,
                'Read':[ 'R1', 'R1', 'R2', 'R2', 'R1', 'R1', 'R2',
                         'R2', 'R1', 'R1', 'R2', 'R2'],
                'Run':['001', '001', '001', '001', '001', '001',
                       '001', '001', '001', '001', '001', '001'],
                'Extension': ['fastq.gz']*12
            }
        )
        exp_df = exp_df.reindex(columns= ['File', 'Sample', 'Index', 'Lane',
                                          'Read', 'Run', 'Extension'])

        pdt.assert_frame_equal(df, exp_df)


if __name__ == '__main__':
    unittest.main()
