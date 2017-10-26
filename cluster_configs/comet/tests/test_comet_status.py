import os
from unittest import TestCase, main
from click.testing import CliRunner
import shutil
from io import StringIO
from cluster_configs.barnacle.barnacle_status import parse_qstat, get_status


class ProcessingTests(TestCase):

    def setUp(self):
        self.curdir = os.path.abspath(os.path.dirname(__file__))
        self.test_data = os.path.join(self.curdir, 'test_data')

        self.status = ('Job Id: 522083.barnacle.ucsd.edu\n'
                       '    Job_Name = timeout.pbs\n'
                       '    job_state = C\n'
                       '    Variable_List = PBS_O_QUEUE=route,\n'
                       '\tPBS_O_LOGNAME=jgsanders\n'
                       '    exit_status = -11\n')

        self.q_fail = {'Job_Name': 'timeout.pbs',
                       'job_state': 'C',
                       'exit_status': '-11'}

        self.q_succ = {'Job_Name': 'timeout.pbs',
                       'job_state': 'C',
                       'exit_status': '0'}

        self.q_queue = {'Job_Name': 'timeout.pbs',
                        'job_state': 'Q'}

        self.q_run = {'Job_Name': 'timeout.pbs',
                      'job_state': 'R'}

    def test_parse_qstat(self):
        exp_q_dict = {'Job_Name': 'timeout.pbs',
                      'job_state': 'C',
                      'Variable_List': 'PBS_O_QUEUE=route,' + 
                                       'PBS_O_LOGNAME=jgsanders',
                      'exit_status': '-11'}

        obs_q_dict = parse_qstat(StringIO(self.status))

        self.assertEqual(exp_q_dict, obs_q_dict)

    def test_get_status(self):
        status_queue = get_status(self.q_queue)
        self.assertEqual('running', status_queue)

        status_run = get_status(self.q_run)
        self.assertEqual('running', status_run)

        status_succ = get_status(self.q_succ)
        self.assertEqual('success', status_succ)

        status_fail = get_status(self.q_fail)
        self.assertEqual('failed', status_fail)

    def test_both(self):
        # test queued
        with open(os.path.join(self.test_data, 'queued.txt'), 'r') as f:
            q_dict_queue = parse_qstat(f)
            status_queue = get_status(q_dict_queue)
            self.assertEqual('running', status_queue)

        # test running
        with open(os.path.join(self.test_data, 'running.txt'), 'r') as f:
            q_dict_run = parse_qstat(f)
            status_run = get_status(q_dict_run)
            self.assertEqual('running', status_run)

        # test failure
        with open(os.path.join(self.test_data, 'failure.txt'), 'r') as f:
            q_dict_fail = parse_qstat(f)
            status_fail = get_status(q_dict_fail)
            self.assertEqual('failed', status_fail)

        # test success
        with open(os.path.join(self.test_data, 'success.txt'), 'r') as f:
            q_dict_succ = parse_qstat(f)
            status_succ = get_status(q_dict_succ)
            self.assertEqual('success', status_succ)

