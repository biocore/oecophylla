import os
import unittest
import pandas as pd
from oecophylla.util.parse import (illumina_filenames_to_df,
                                   extract_sample_reads,
                                   add_filter_db,
                                   extract_sample_paths)
import pandas.util.testing as pdt


class TestParse(unittest.TestCase):

    def test_illumina_filenames_to_df(self):
        fnames =[
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
        df = illumina_filenames_to_df(fnames)
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

    def test_extract_sample_reads(self):
        fnames =[
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

        df = pd.DataFrame({
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
        seq_dir = '%s/../../../test_data/test_reads' % os.path.abspath(
            os.path.dirname(__file__))
        d = extract_sample_reads(df, seq_dir,
                                 sample_col='Sample',
                                 read_col='Read',
                                 file_col='File')
        exp_d ={
            'S22401': {
                'forward': ['%s/S22401_S100_L001_R1_001.fastq.gz' % seq_dir],
                'reverse': ['%s/S22401_S100_L001_R2_001.fastq.gz' % seq_dir]},
            'S22400': {
                'forward': ['%s/S22400_S101_L001_R1_001.fastq.gz' % seq_dir],
                'reverse': ['%s/S22400_S101_L001_R2_001.fastq.gz' % seq_dir]},
            'S22402': {
                'forward': ['%s/S22402_S105_L001_R1_001.fastq.gz' % seq_dir],
                'reverse': ['%s/S22402_S105_L001_R2_001.fastq.gz' % seq_dir]},
            'S22205': {
                'forward': ['%s/S22205_S104_L001_R1_001.fastq.gz' % seq_dir],
                'reverse': ['%s/S22205_S104_L001_R2_001.fastq.gz' % seq_dir]},
            'S22207': {
                'forward': ['%s/S22207_S103_L001_R1_001.fastq.gz' % seq_dir],
                'reverse': ['%s/S22207_S103_L001_R2_001.fastq.gz' % seq_dir]},
            'S22282': {
                'forward': ['%s/S22282_S102_L001_R1_001.fastq.gz' % seq_dir],
                'reverse': ['%s/S22282_S102_L001_R2_001.fastq.gz' % seq_dir]}}

        self.assertDictEqual(d, exp_d)


    def test_extract_sample_paths_db(self):
        seq_dir = '%s/../../../test_data/test_reads' % os.path.abspath(
            os.path.dirname(__file__))
        d = extract_sample_paths(seq_dir)
        exp_d ={
            'S22401': {
                'forward': ['%s/S22401_S100_L001_R1_001.fastq.gz' % seq_dir],
                'reverse': ['%s/S22401_S100_L001_R2_001.fastq.gz' % seq_dir]},
            'S22400': {
                'forward': ['%s/S22400_S101_L001_R1_001.fastq.gz' % seq_dir],
                'reverse': ['%s/S22400_S101_L001_R2_001.fastq.gz' % seq_dir]},
            'S22402': {
                'forward': ['%s/S22402_S105_L001_R1_001.fastq.gz' % seq_dir],
                'reverse': ['%s/S22402_S105_L001_R2_001.fastq.gz' % seq_dir]},
            'S22205': {
                'forward': ['%s/S22205_S104_L001_R1_001.fastq.gz' % seq_dir],
                'reverse': ['%s/S22205_S104_L001_R2_001.fastq.gz' % seq_dir]},
            'S22207': {
                'forward': ['%s/S22207_S103_L001_R1_001.fastq.gz' % seq_dir],
                'reverse': ['%s/S22207_S103_L001_R2_001.fastq.gz' % seq_dir]},
            'S22282': {
                'forward': ['%s/S22282_S102_L001_R1_001.fastq.gz' % seq_dir],
                'reverse': ['%s/S22282_S102_L001_R2_001.fastq.gz' % seq_dir]}}

        self.assertDictEqual(d, exp_d)


    def test_add_filter_db(self):
        seq_dir = '%s/../../../test_data/test_reads' % os.path.abspath(
            os.path.dirname(__file__))

        sample_fp_dict ={
            'S22401': {
                'forward': ['%s/S22401_S100_L001_R1_001.fastq.gz' % seq_dir],
                'reverse': ['%s/S22401_S100_L001_R2_001.fastq.gz' % seq_dir]},
            'S22400': {
                'forward': ['%s/S22400_S101_L001_R1_001.fastq.gz' % seq_dir],
                'reverse': ['%s/S22400_S101_L001_R2_001.fastq.gz' % seq_dir]},
            'S22402': {
                'forward': ['%s/S22402_S105_L001_R1_001.fastq.gz' % seq_dir],
                'reverse': ['%s/S22402_S105_L001_R2_001.fastq.gz' % seq_dir]},
            'S22205': {
                'forward': ['%s/S22205_S104_L001_R1_001.fastq.gz' % seq_dir],
                'reverse': ['%s/S22205_S104_L001_R2_001.fastq.gz' % seq_dir]},
            'S22207': {
                'forward': ['%s/S22207_S103_L001_R1_001.fastq.gz' % seq_dir],
                'reverse': ['%s/S22207_S103_L001_R2_001.fastq.gz' % seq_dir]},
            'S22282': {
                'forward': ['%s/S22282_S102_L001_R1_001.fastq.gz' % seq_dir],
                'reverse': ['%s/S22282_S102_L001_R2_001.fastq.gz' % seq_dir]}}

        d = add_filter_db(sample_fp_dict, db_fp='db', samples = None,
                           filter_col='filter_db')

        exp_d ={
            'S22401': {
                'forward': ['%s/S22401_S100_L001_R1_001.fastq.gz' % seq_dir],
                'reverse': ['%s/S22401_S100_L001_R2_001.fastq.gz' % seq_dir],
                'filter_db': 'db'
            },
            'S22400': {
                'forward': ['%s/S22400_S101_L001_R1_001.fastq.gz' % seq_dir],
                'reverse': ['%s/S22400_S101_L001_R2_001.fastq.gz' % seq_dir],
                'filter_db': 'db'
            },
            'S22402': {
                'forward': ['%s/S22402_S105_L001_R1_001.fastq.gz' % seq_dir],
                'reverse': ['%s/S22402_S105_L001_R2_001.fastq.gz' % seq_dir],
                'filter_db': 'db'
            },
            'S22205': {
                'forward': ['%s/S22205_S104_L001_R1_001.fastq.gz' % seq_dir],
                'reverse': ['%s/S22205_S104_L001_R2_001.fastq.gz' % seq_dir],
                'filter_db': 'db'
            },
            'S22207': {
                'forward': ['%s/S22207_S103_L001_R1_001.fastq.gz' % seq_dir],
                'reverse': ['%s/S22207_S103_L001_R2_001.fastq.gz' % seq_dir],
                'filter_db': 'db'
            },
            'S22282': {
                'forward': ['%s/S22282_S102_L001_R1_001.fastq.gz' % seq_dir],
                'reverse': ['%s/S22282_S102_L001_R2_001.fastq.gz' % seq_dir],
                'filter_db': 'db'
            }
        }
        self.assertDictEqual(d, exp_d)


if __name__ == '__main__':
    unittest.main()
