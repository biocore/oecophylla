from unittest import TestCase, main
from tempfile import mkstemp

import pandas as pd
from pandas.util.testing import assert_frame_equal
from skbio.util import get_data_path
import biom

from oecophylla.taxonomy.parser import (combine_bracken, pandas2biom)


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
