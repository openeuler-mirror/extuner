# -*- coding:utf-8 -*-
#!/usr/bin/env python
# cython:language_level=3
from common.command import Command
import subprocess,shlex

class ConfCheck:
    def pid(process):
        '''
            check pid exist or not, return pid or null
        '''
        get_pid_cmd = "ps -ef | grep {} | grep -v grep | awk '{{print $2}}'".format(process)
        pid_list = Command.cmd_run(get_pid_cmd).split("\n")
        pid_list.pop(0)
        pid_list.pop(-1)
        if len(pid_list) != 0:
            return pid_list[0]
        else:
            return ''

    def pid_list(process):
        '''
            check process exist or not, return pid_list or null
        '''
        get_pid_cmd = "ps -ef | grep {} | grep -v grep | awk '{{print $2}}'".format(process)
        p_list = Command.cmd_run(get_pid_cmd).split("\n")
        p_list.pop(0)
        p_list.pop(-1)
        return p_list

    @staticmethod
    def f_exists(file  = ''):
        if file == '':
            return False
        devnull = open("/dev/null", "w")
        ret = subprocess.Popen(shlex('test -e ' + file), stdout = devnull, stderr = devnull)
        ret.communicate()
        if 0 == ret.returncode:
            return True
        else:
            return False
