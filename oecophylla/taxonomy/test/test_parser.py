from unittest import TestCase, main

import pandas as pd
from pandas.util.testing import assert_frame_equal
from skbio.util import get_data_path

from oecophylla.taxonomy.parser import trim_lineage, combine_bracken


class ParserTest(TestCase):
    def test_trim_lineage(self):
        # trim nothing
        exp = ('k__Bacteria;p__Proteobacteria;c__Gammaproteobacteria;o__Entero'
               'bacterales;f__Enterobacteriaceae;g__Escherichia;s__Escherichia'
               '_coli;t__Escherichia_coli_O104:H4')
        obs = trim_lineage(
            ('k__Bacteria;p__Proteobacteria;c__Gammaproteobacteria;o__Enteroba'
             'cterales;f__Enterobacteriaceae;g__Escherichia;s__Escherichia_col'
             'i;t__Escherichia_coli_O104:H4'),
            ['45;45', '45;45', '45;45', '45;45', '45;45', '14;14', '14;14',
             '8;10'])
        self.assertEqual(exp, obs)

        # trim last 1
        exp = ('k__Bacteria;p__Bacteroidetes;c__Bacteroidia;o__Bacteroidales;f'
               '__Bacteroidaceae;g__Bacteroides;s__Bacteroides_uniformis;t__')
        obs = trim_lineage(
            ('k__Bacteria;p__Bacteroidetes;c__Bacteroidia;o__Bacteroidales;f__'
             'Bacteroidaceae;g__Bacteroides;s__Bacteroides_uniformis;t__Bacter'
             'oides_uniformis_ATCC_8492'),
            ['16;16', '16;16', '16;16', '16;16', '16;16', '16;16', '12;16',
             '0;0'])
        self.assertEqual(exp, obs)

        # trim last 2
        exp = ('k__Bacteria;p__Proteobacteria;c__Gammaproteobacteria;o__Entero'
               'bacterales;f__Enterobacteriaceae;g__Escherichia;s__;t__')
        obs = trim_lineage(
            ('k__Bacteria;p__Proteobacteria;c__Gammaproteobacteria;o__Enteroba'
             'cterales;f__Enterobacteriaceae;g__Escherichia;s__Escherichia_col'
             'i;t__'),
            ['18;18', '18;18', '18;18', '18;18', '18;18', '8;8', '0;0', '0;0'])
        self.assertEqual(exp, obs)

        # trim last 3
        exp = ('k__Bacteria;p__Bacteroidetes;c__Bacteroidia;o__Bacteroidales;f'
               '__Bacteroidaceae;g__;s__;t__')
        obs = trim_lineage(
            ('k__Bacteria;p__Bacteroidetes;c__Bacteroidia;o__Bac'
             'teroidales;f__Bacteroidaceae;g__Bacteroides;s__;t__'),
            ['70;70', '70;70', '70;70', '70;70', '26;26', '0;0', '0;0', '0;0'])
        self.assertEqual(exp, obs)

        # trim in the middle, i.e. after Kingdom
        exp = 'k__Bacteria;p__;c__;o__;f__;g__;s__;t__'
        obs = trim_lineage(
            ('k__Bacteria;p__Bacteroidetes;c__Bacteroidia;o__Bac'
             'teroidales;f__Bacteroidaceae;g__Bacteroides;s__;t__'),
            ['70;70', '1;70', '70;70', '70;70', '26;26', '0;0', '0;0', '0;0'])
        self.assertEqual(exp, obs)

    def test_combine_bracken(self):
        exp = pd.read_csv(get_data_path('bracken/combined.phylum.tsv'),
                          sep='\t', index_col=0, dtype=int)
        obs = combine_bracken(get_data_path('bracken/phylum'))
        assert_frame_equal(obs[sorted(obs.columns)].sort_index(),
                           exp[sorted(exp.columns)].sort_index())

        exp = pd.read_csv(get_data_path('bracken/combined.species.tsv'),
                          sep='\t', index_col=0, dtype=int)
        obs = combine_bracken(get_data_path('bracken/species'))
        assert_frame_equal(obs[sorted(obs.columns)].sort_index(),
                           exp[sorted(exp.columns)].sort_index())


if __name__ == '__main__':
    main()
