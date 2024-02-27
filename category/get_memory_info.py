#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# cython:language_level=3

from common.global_parameter import GlobalParameter
from common.log import Logger
from common.file import FileOperation
from common.global_call import GlobalCall
from common.command import Command

# memory class
class MemInfo():
    def __init__(self, t_fileName):
        self.__TOTALNUMS = 2
        self.__success_counts, self.__failed_counts, self.__waiting_counts = 0, 0, 0
        self.__default_file_name = t_fileName
        FileOperation.remove_txt_file(self.__default_file_name)
        # 默认时间间隔为1s
        self.__interval = GlobalParameter().get_mem_interval()
        # 默认执行5次
        self.__times    = GlobalParameter().get_mem_times()

    def __get_mem_info(self):
        '''
            Mem information
        '''
        mem_command="cat /proc/meminfo"
        cmd_name_m = mem_command
        cmd_result = Command.cmd_run(mem_command)
        res_m = FileOperation.wrap_output_format(cmd_name_m, cmd_result, '-')
        return Command.cmd_write_file(res_m, self.__default_file_name)

    def __get_dmidecode_info(self):
        '''
            Memory slots info
        '''
        dmidecode_command="dmidecode -t memory"
        cmd_name = dmidecode_command
        cmd_result = Command.cmd_run(dmidecode_command)
        return Command.cmd_output(cmd_name, cmd_result, self.__default_file_name, '=')

    def __get_free_info(self,interval, times):
        '''
            Get memory information
        '''
        free_command="free -m"
        cmd_name = "free -m"
        cmd_result = Command.cmd_run(free_command)
        res_free = FileOperation.wrap_output_format(cmd_name, cmd_result,'-')
        return Command.cmd_write_file(res_free, self.__default_file_name)
