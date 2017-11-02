#!/usr/bin/env python

import subprocess
import sys
import time
import re
from io import StringIO

def parse_scontrol(lines):
    s_dict = {}

    p = re.compile('^(.+?)=(.+)$')
    for line in lines:
        entries = line.strip().split(' ')
        for entry in entries:
            m = p.match(entry)
            if m:
                s_dict[m.groups()[0]] = m.groups()[1]

    return(s_dict)

def get_status(s_dict):
    try:
        if s_dict['JobState'] == 'RUNNING':
            status = "running"
        elif s_dict['JobState'] == 'PENDING':
            status = "running"
        elif s_dict['JobState'] == 'COMPLETED' and s_dict['ExitCode'] == '0:0':
            status = "success"
        elif s_dict['JobState'] == 'FAILED':
            status = "failed"
        elif s_dict['JobState'] == 'TIMEOUT':
            status = "failed"
        else:
            status = "failed"
    except KeyError:
        status = "failed"

    return(status)

def main():
    jobid = sys.argv[1]

    TRY_TIMES = 3

    for i in range(TRY_TIMES):
        cmd = "scontrol show job  {}".format(jobid)
        p1 = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, shell=True)
        out, err = p1.communicate()

        if err.decode().startswith('slurm_load_jobs error: Invalid job id specified'):
            time.sleep(1)
            continue

    s_dict = parse_scontrol(StringIO(out.decode()))

    status = get_status(s_dict)

    print(status)

if __name__ == '__main__':
    main()
