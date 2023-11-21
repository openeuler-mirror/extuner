#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# cython:language_level=3

from common.file import FileOperation
from common.command import Command
from common.global_parameter import GlobalParameter

# CPU class
class CPUInfo:
    def __init__(self, t_fileName):
        self.__default_file_name = t_fileName
        FileOperation.remove_txt_file(self.__default_file_name)
        # 默认时间间隔
        self.__interval = GlobalParameter().get_cpu_interval
        # 默认执行次数
        self.__times = GlobalParameter().get_cpu_times

    def __get_cpu_info(self):
        '''
            cat /proc/cpuinfo and lscpu
        '''
        cmd_name = "cat /proc/cpuinfo"
        
        lscpu_cmd = "lscpu"
        cmd_result = Command.cmd_run(lscpu_cmd)
        res_lscpu = FileOperation.wrap_output_format(cmd_name, cmd_result, '-')
        
        cpuinfo_command="cat /proc/cpuinfo"
        cmd_result = Command.cmd_run(cpuinfo_command)
        res_cpuinfo = FileOperation.wrap_output_format(cmd_name, cmd_result, '=')
        
        
        res_all = res_lscpu + res_cpuinfo 
        return Command.cmd_write_file(res_all, self.__default_file_name)

    # getInfo
    def get_info(self):
        self.__get_cpu_info()
        self.__get_top_info(self.__interval, self.__times)
        
        #多线程执行命令，间隔self.__interval秒，运行self.__times次
        #必须放在一起，保证命令启动时间一致
        self.__get_pid_cpustat_info()
        self.__get_mpstat_info(self.__interval, self.__times)
        self.__get_sar_info(self.__interval, self.__times)
        self.__get_numastat_info()