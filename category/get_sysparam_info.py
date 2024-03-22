#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# cython:language_level=3

from common.file import FileOperation

class SysParamInfo:
    '''
        System parameter class
    '''
    def __init__(self, t_fileName):
        self.__default_file_name = t_fileName

    def __get_sys_param_info(self):
        '''
            get current system parameters
        '''
        sysparam_command = "sysctl -a"
        cmd_name = sysparam_command
        cmd_result = Command.cmd_run(sysparam_command)
        return Command.cmd_output(cmd_name, cmd_result, self.__default_file_name, '=')
