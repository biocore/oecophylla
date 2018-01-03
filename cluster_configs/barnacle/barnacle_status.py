#!/usr/bin/env python

import subprocess
import sys
import time
import re
from io import StringIO

def parse_qstat(lines):
    q_dict = {}

    p = re.compile('^ +(.+?) = (.+)')
    for line in lines:
        if line.startswith(' '):
            entry = line.rstrip()
            m = p.match(entry.rstrip())
            q_dict[m.groups()[0]] = m.groups()[1]
        elif line.startswith('\t'):
            entry += line.strip()
            m = p.match(entry.rstrip())
            q_dict[m.groups()[0]] = m.groups()[1]

    return(q_dict)

def get_status(q_dict):
    try:
        if q_dict['job_state'] == 'R':
            status = "running"
        elif q_dict['job_state'] == 'Q':
            status = "running"
        elif q_dict['job_state'] == 'C' and q_dict['exit_status'] == '0':
            status = "success"
        elif q_dict['job_state'] == 'C' and q_dict['exit_status'] != '0':
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
        cmd = "qstat -f {}".format(jobid)
        p1 = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, shell=True)
        out, err = p1.communicate()

        if err.decode().startswith('qstat: Unknown Job Id Error'):
            time.sleep(5)
            continue

    q_dict = parse_qstat(StringIO(out.decode()))

    status = get_status(q_dict)

    print(status)

if __name__ == '__main__':
    main()
