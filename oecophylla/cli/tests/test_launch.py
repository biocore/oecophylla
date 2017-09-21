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

    def test_config(self):
        _params = ['--input-dir', self.seq_dir,
                   '--params', '%s/data/tool_params.yml' % self.curdir,
                   '--envs', '%s/data/envs.yml' % self.curdir,
                   '--local-scratch', self.local_dir,
                   '--output-dir', self.output_dir,
                   '--just-config',
                   'all'
                   ]

        res = CliRunner().invoke(workflow, _params)

        # test the config file
        with open('%s/config.yaml' % self.output_dir, 'r') as f:
            res_config = yaml.load(f)
        with open('%s/data/exp_config.yaml' % self.curdir, 'r') as f:
            exp_config = yaml.load(f)
        self.assertDictEqual(res_config, exp_config)

    def test_local(self):
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

        # test the config file
        with open('%s/config.yaml' % self.output_dir, 'r') as f:
            res_config = yaml.load(f)
        with open('%s/data/exp_config.yaml' % self.curdir, 'r') as f:
            exp_config = yaml.load(f)
        self.maxDiff = None
        self.assertDictEqual(res_config, exp_config)

    def test_slurm(self):
        # TODO
        pass

    def test_qsub(self):
        # TODO
        pass


if __name__ == '__main__':
    main()
