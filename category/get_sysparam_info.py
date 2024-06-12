#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# cython:language_level=3

from common.file import FileOperation
from common.command import Command

class SysParamInfo:
    '''
        System parameter class
    '''
    def __init__(self, t_fileName):
        self.__default_file_name = t_fileName
        FileOperation.remove_txt_file(self.__default_file_name)

    def __get_sys_param_info(self):
        '''
            get current system parameters
        '''
        sysparam_command = "sysctl -a"
        cmd_name = sysparam_command
        cmd_result = Command.cmd_run(sysparam_command)
        return Command.cmd_output(cmd_name, cmd_result, self.__default_file_name, '=')

    def __get_boot_param_info(self):
        '''
            Get startup parameters
        '''
        bootparam_command = "cat /proc/cmdline"
        cmd_name = "cmdline"
        cmd_result = Command.cmd_run(bootparam_command)
        res_cmd = FileOperation.wrap_output_format(cmd_name, cmd_result, '-')

        kernel_command = "grubby --info=ALL | grep ^kernel"
        ker_result = Command.cmd_run(kernel_command)
        res_gk = FileOperation.wrap_output_format(cmd_name, ker_result, '-')
