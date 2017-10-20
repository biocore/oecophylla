from unittest import TestCase, main
from tempfile import mkstemp

import pandas as pd
from pandas.util.testing import assert_frame_equal
from skbio.util import get_data_path
import biom

from oecophylla.taxonomy.parser import (combine_profiles,
                                        extract_level,
                                        combine_centrifuge,
                                        combine_bracken,
                                        pandas2biom)


class TaxonomyParserTest(TestCase):
    def test_combine_profiles(self):
        exp = pd.read_table(get_data_path('shogun/combined.phylum.tsv'),
                            index_col=0)
        obs = combine_profiles(
            [('sampleA', get_data_path('shogun/phylum/sampleA.txt')),
             ('sampleB', get_data_path('shogun/phylum/sampleB.txt'))])
        assert_frame_equal(obs[sorted(obs.columns)].sort_index().astype(int),
                           exp[sorted(exp.columns)].sort_index().astype(int))

    def test_extract_level(self):
        # test extracting phyla and families from MetaPhlAn output
        table = pd.read_table(get_data_path('metaphlan2/combined.tsv'),
                              index_col=0)
        for level in ('phylum', 'family'):
            obs = extract_level(table, level[0], delim='|')
            exp = pd.read_table(get_data_path('metaphlan2/combined.%s.tsv'
                                              % level), index_col=0)
            assert_frame_equal(obs[sorted(obs.columns)].sort_index(),
                               exp[sorted(exp.columns)].sort_index())
        # test extracting genera and translating into TaxIDs
        with open(get_data_path('metaphlan2/dic.genus.txt'), 'r') as f:
            dic = dict(x.split('\t') for x in f.read().splitlines())
        obs = extract_level(table, 'g', delim='|', dic=dic)
        exp = pd.read_table(get_data_path('metaphlan2/combined.genus.taxid'
                                          '.tsv'), index_col=0)
        exp.index = exp.index.map(str)
        assert_frame_equal(obs[sorted(obs.columns)].sort_index(),
                           exp[sorted(exp.columns)].sort_index())
        # test if there are duplicated taxon names
        table = pd.read_table(get_data_path('metaphlan2/combined_w_dup.tsv'),
                              index_col=0)
        with self.assertRaisesRegex(ValueError, 'Duplicated taxa detected'):
            extract_level(table, 'p', delim='|')

    def test_combine_centrifuge(self):
        exp = pd.read_table(get_data_path('centrifuge/combined.tsv'),
                            index_col=0)
        obs = combine_centrifuge(
            [('sampleA', get_data_path('centrifuge/sampleA.txt')),
             ('sampleB', get_data_path('centrifuge/sampleB.txt'))])
        assert_frame_equal(obs[sorted(obs.columns)].sort_index().astype(int),
                           exp[sorted(exp.columns)].sort_index().astype(int))

    def test_combine_bracken(self):
        exp = pd.read_csv(get_data_path('bracken/combined.phylum.tsv'),
                          sep='\t', index_col=0, dtype=int)
        obs = combine_bracken(
            [('sample1', get_data_path('bracken/phylum/sample1.tsv')),
             ('sample2', get_data_path('bracken/phylum/sample2.tsv')),
             ('sample3', get_data_path('bracken/phylum/sample3.tsv'))])
        assert_frame_equal(obs[sorted(obs.columns)].sort_index(),
                           exp[sorted(exp.columns)].sort_index())

        exp = pd.read_csv(get_data_path('bracken/combined.species.tsv'),
                          sep='\t', index_col=0, dtype=int)
        obs = combine_bracken(
            [('sampleA', get_data_path('bracken/species/sampleA.tsv')),
             ('sampleB', get_data_path('bracken/species/sampleB.tsv')),
             ('sampleC', get_data_path('bracken/species/sampleC.tsv'))])
        assert_frame_equal(obs[sorted(obs.columns)].sort_index(),
                           exp[sorted(exp.columns)].sort_index())

    def test_pandas2biom(self):
        fh, filename = mkstemp()
        p = pd.read_csv(get_data_path('float.tsv'), sep='\t', index_col=0)
        with self.assertRaisesRegex(IOError, 'Unable to create file'):
            pandas2biom('/dev/', p)
        pandas2biom(filename, p)
        b = biom.load_table(filename)
        self.assertCountEqual(b.ids(), p.columns)
        self.assertCountEqual(b.ids(axis='observation'), p.index)


if __name__ == '__main__':
    main()
