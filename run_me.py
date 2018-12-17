#!/usr/bin/env python3

import subprocess as sp
import os
import signal
import logging

## log definitions:
log_file_name = 'my.log'
for i in range(19):
    print(i)
## if there is a log of a previous run, delete it
if os.path.exists(log_file_name):
    os.remove(log_file_name)

handler = logging.FileHandler(log_file_name)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s (from %(funcName)s)')
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.info('3')

logger.info('----- Starting run_me.py ------')
#print("A")

tcp_proc = sp.Popen(["./Camera/camera_tcp_session.py"], shell=True, stdout=sp.PIPE, bufsize=10 ** 8, preexec_fn=os.setsid)
main_proc = sp.Popen(["./main.py"],  shell=True, stdin=tcp_proc.stdout, preexec_fn=os.setsid)
main_proc.wait()
os.killpg(os.getpgid(tcp_proc.pid), signal.SIGTERM)
