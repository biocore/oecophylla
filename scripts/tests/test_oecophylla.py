from unittest import TestCase, main
from click.testing import CliRunner
from shutil import rmtree
from os import remove
from os.path import join, basename
from tempfile import mkdtemp
from skbio.util import get_data_path
from skbio import Sequence
from glob import glob


class ProcessingTests(TestCase):
    def setUp(self):
        # temporary working directory
        self.working_dir = mkdtemp()

        # test data files
        dir = 'test_process_fasta'
        self.input_faa = get_data_path(join(dir, 'input.faa'))
        self.represent = get_data_path(join(dir, 'represent.xml'))
        self.pdb_seqres = get_data_path(join(dir, 'pdb_seqres.txt'))

        self.split_1 = get_data_path(join(dir, '1K5N_B.fasta'))
        self.split_2 = get_data_path(join(dir, '2VB1_A.fasta'))
        self.split_3 = get_data_path(join(dir, '3J4F_A.fasta'))

        # test protein sequences
        self.seqs = []
        x = Sequence('PIVQNLQGQMVHQAISPRTLNAWVKVVEEKAFSPEVIPMFSALSEGATPQDLNTML'
                     'NTVGGHQAAMQMLKETINEEAAEWDRLHPVHAGPIEPGQMREPRGSDIAGTTSTLQ'
                     'EQIGWMTHNPPIPVGEIYKRWIILGLNKIVRMYSPTSILDIRQGPKEPFRDYVDRF'
                     'YKTLRAEQASQEVKNWMTETLLVQNANPDCKTILKALGPAATLEEMMTACQGVGGP'
                     'GHKARVL')
        x.metadata['id'] = '3J4F_A'
        x.metadata['description'] = ('Chain A, Structure Of Hiv-1 Capsid Prote'
                                     'in By Cryo-em')
        self.seqs.append(x)
        x = Sequence('MIQRTPKIQVYSRHPAENGKSNFLNCYVSGFHPSDIEVDLLKNGERIEKVEHSDLS'
                     'FSKDWSFYLLYYTEFTPTEKDEYACRVNHVTLSQPKIVKWDRDM')
        x.metadata['id'] = '1K5N_B'
        x.metadata['description'] = ('Chain B, Hla-B2709 Bound To Nona-Peptide'
                                     ' M9')
        self.seqs.append(x)
        x = Sequence('KVFGRCELAAAMKRHGLDNYRGYSLGNWVCAAKFESNFNTQATNRNTDGSTDYGIL'
                     'QINSRWWCNDGRTPGSRNLCNIPCSALLSSDITASVNCAKKIVSDGNGMNAWVAWR'
                     'NRCKGTDVQAWIRGCRL')
        x.metadata['id'] = '2VB1_A'
        x.metadata['description'] = ('Chain A, Hewl At 0.65 Angstrom Resolutio'
                                     'n')
        self.seqs.append(x)

    def test_local(self):
        pass

    def test_slurm(self):
        pass

    def test_qsub(self):
        pass

    def test_workflow(self):
        # get representative proteins
        params = ['--infile', self.input_faa,
                  '--outfile', join(self.working_dir, 'output.faa'),
                  '--identifiers', None,
                  '--represent', self.represent]
        res = CliRunner().invoke(_process_fasta, params)
        self.assertEqual(res.exit_code, 0)
        exp = ('Number of representative proteins: 3\n'
               'Number of extracted proteins: 0\n'
               'Task completed.\n')
        self.assertEqual(res.output, exp)

        # extract proteins
        params = ['--infile', self.input_faa,
                  '--outfile', join(self.working_dir, 'output.faa'),
                  '--identifiers', '1,3',
                  '--represent', None]
        res = CliRunner().invoke(_process_fasta, params)
        self.assertEqual(res.exit_code, 0)
        exp = ('Number of extracted proteins: 2\n'
               'Task completed.\n')
        self.assertEqual(res.output, exp)

    def tearDown(self):
        rmtree(self.working_dir)


if __name__ == '__main__':
    main()
