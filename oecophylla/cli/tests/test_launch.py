import os
from unittest import TestCase, main
from click.testing import CliRunner
import shutil
from oecophylla.cli.launch import workflow
import yaml
import subprocess


class ProcessingTests(TestCase):

    def setUp(self):
        self.seq_dir = "%s/../../../test_data/test_reads" % os.path.abspath(
            os.path.dirname(__file__))
        self.curdir = os.path.abspath(os.path.dirname(__file__))
        self.output_dir = '%s/test_output' % self.curdir
        self.local_dir = '%s/test_scratch' % self.curdir
        os.mkdir(self.local_dir)

    def tearDown(self):
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        if os.path.exists(self.local_dir):
            shutil.rmtree(self.local_dir)

    def test_local(self):
        self.maxDiff = None
        _params = ['--input-dir', self.seq_dir,
                   '--params', '%s/data/tool_params.yml' % self.curdir,
                   '--envs', '%s/data/envs.yml' % self.curdir,
                   '--local-scratch', self.local_dir,
                   '--output-dir', self.output_dir,
                   '--snakemake-args', '-n',
                   'all'
                   ]

        #res = CliRunner().invoke(workflow, _params)
        cmd = ' oecophylla workflow ' + ' '.join(_params)

        proc = subprocess.Popen(cmd, shell=True)
        proc.wait()

        # make sure that the tests complete
        self.assertEqual(proc.returncode, 0)

    def test_slurm(self):
        # TODO
        pass

    def test_qsub(self):
        # TODO
        pass


if __name__ == '__main__':
    main()
