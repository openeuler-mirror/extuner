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

        vmstat_s_cmd="vmstat -s"
        cmd_result = Command.cmd_run(vmstat_s_cmd)
        res_vmstat_s = FileOperation.wrap_output_format(cmd_name, cmd_result,'-')

        vmstat_command="vmstat {} {}".format(interval, times)
        cmd_result = Command.cmd_run(vmstat_command)
        res_vmstat = FileOperation.wrap_output_format(cmd_name, cmd_result,'=')

        res = res_free + res_vmstat_s + res_vmstat
        return Command.cmd_write_file(res, self.__default_file_name)

    def get_info(self):
        '''
            Get the external interface of memory monitoring information
        '''
        if self.__get_mem_info():
            self.__success_counts += 1
        else:
            self.__failed_counts += 1
            Logger().debug("__get_mem_info failed!!!")

        if self.__get_dmidecode_info():
            self.__success_counts += 1
        else:
            self.__failed_counts += 1
            Logger().debug("__get_dmidecode_info failed!!!")

        if self.__get_free_info(self.__interval, self.__times):
            self.__success_counts += 1
        else:
            self.__failed_counts += 1
            Logger().debug("__get_free_info failed!!!")

        if self.__TOTALNUMS == self.__failed_counts:
            Logger().error("Failed to get memory information")
        Logger().debug("Get memory information end : total [{}] success[{}] failed[{}] waiting threads[{}]".format(self.__TOTALNUMS, self.__success_counts, self.__failed_counts,self.__waiting_counts))
