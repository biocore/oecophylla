import os
from unittest import TestCase, main
from click.testing import CliRunner
import shutil
from io import StringIO
from cluster_configs.comet.comet_status import parse_scontrol, get_status


class ProcessingTests(TestCase):

    def setUp(self):
        self.curdir = os.path.abspath(os.path.dirname(__file__))
        self.test_data = os.path.join(self.curdir, 'test_data')

        self.status = ('JobId=12166539 JobName=fail.sbatch\n'
                       '   JobState=FAILED Reason=NonZeroExitCode\n'
                       '   ExitCode=1:0\n')

        self.s_fail = {'JobName': 'timeout.pbs',
                       'JobState': 'FAILED',
                       'ExitCode': '1:0'}

        self.s_time = {'JobName': 'timeout.pbs',
                       'JobState': 'TIMEOUT',
                       'ExitCode': '0:1'}

        self.s_succ = {'JobName': 'timeout.pbs',
                       'JobState': 'COMPLETED',
                       'ExitCode': '0:0'}

        self.s_queue = {'JobName': 'timeout.pbs',
                        'JobState': 'PENDING'}

        self.s_run = {'JobName': 'timeout.pbs',
                      'JobState': 'RUNNING'}

    def test_parse_scontrol(self):
        exp_s_dict = {'JobId': '12166539',
                      'JobName': 'fail.sbatch',
                      'JobState': 'FAILED',
                      'Reason': 'NonZeroExitCode',
                      'ExitCode': '1:0'}

        obs_s_dict = parse_scontrol(StringIO(self.status))

        self.assertEqual(exp_s_dict, obs_s_dict)

    def test_get_status(self):
        status_queue = get_status(self.s_queue)
        self.assertEqual('running', status_queue)

        status_run = get_status(self.s_run)
        self.assertEqual('running', status_run)

        status_succ = get_status(self.s_succ)
        self.assertEqual('success', status_succ)

        status_fail = get_status(self.s_fail)
        self.assertEqual('failed', status_fail)

        status_time = get_status(self.s_time)
        self.assertEqual('failed', status_time)

    def test_both(self):
        # test queued
        with open(os.path.join(self.test_data, 'queued.txt'), 'r') as f:
            s_dict_queue = parse_scontrol(f)
            status_queue = get_status(s_dict_queue)
            self.assertEqual('running', status_queue)

        # test running
        with open(os.path.join(self.test_data, 'running.txt'), 'r') as f:
            s_dict_run = parse_scontrol(f)
            status_run = get_status(s_dict_run)
            self.assertEqual('running', status_run)

        # test failure
        with open(os.path.join(self.test_data, 'failure.txt'), 'r') as f:
            s_dict_fail = parse_scontrol(f)
            status_fail = get_status(s_dict_fail)
            self.assertEqual('failed', status_fail)

        # test timeout
        with open(os.path.join(self.test_data, 'timeout.txt'), 'r') as f:
            s_dict_fail = parse_scontrol(f)
            status_fail = get_status(s_dict_fail)
            self.assertEqual('failed', status_fail)

        # test success
        with open(os.path.join(self.test_data, 'success.txt'), 'r') as f:
            s_dict_succ = parse_scontrol(f)
            status_succ = get_status(s_dict_succ)
            self.assertEqual('success', status_succ)

