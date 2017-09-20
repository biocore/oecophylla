from unittest import TestCase, main

import pandas as pd
from pandas.util.testing import assert_frame_equal
from skbio.util import get_data_path

from oecophylla.taxonomy.parser import combine_bracken


class ParserTest(TestCase):
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


if __name__ == '__main__':
    main()
