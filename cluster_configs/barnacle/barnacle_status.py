#!/usr/bin/env python

import subprocess
import sys
import time
import re
from io import StringIO

def parse_qstat(lines):
    status = {}

    for line in lines:
        if line.startswith(' '):
            entry = line.rstrip()
            p = re.compile('^ +(.+?) = (.+)')
            m = p.match(entry.rstrip())
            status[m.groups()[0]] = m.groups()[1]
        elif line.startswith('\t'):
            entry += line.strip()
            p = re.compile('^ +(.+?) = (.+)')
            m = p.match(entry.rstrip())
            status[m.groups()[0]] = m.groups()[1]

    return(status)

def print_status(status):
    try:
        if status['job_state'] == 'R':
            print("running")
        elif status['job_state'] == 'Q':
            print("running")
        elif status['job_state'] == 'C' and status['exit_status'] == '0':
            print("success")
        elif status['job_state'] == 'C' and status['exit_status'] != '0':
            print("failed")
        else:
            print("failed")
    except KeyError:
        print("failed")

def main():
    jobid = sys.argv[1]

    cmd = "qstat -f {}".format(jobid)
    p1 = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    lines = p1.communicate()[0].decode()
    status = parse_qstat(StringIO(lines))

    print_status(status)

if __name__ == '__main__':
    main()
