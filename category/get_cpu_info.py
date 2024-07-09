#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# cython:language_level=3

from time import sleep
from common.customizefunctionthread import CustomizeFunctionThread
from common.file import FileOperation
from common.global_call import GlobalCall
from common.command import Command
from common.global_parameter import GlobalParameter

# CPU class
class CPUInfo:
    def __init__(self, t_fileName):
        self.__default_file_name = t_fileName
        FileOperation.remove_txt_file(self.__default_file_name)
        # 默认时间间隔
        self.__interval = GlobalParameter().get_cpu_interval()
        # 默认执行次数
        self.__times = GlobalParameter().get_cpu_times()

    def __get_cpu_info(self):
        '''
            cat /proc/cpuinfo and lscpu
        '''
        cmd_name = "cat /proc/cpuinfo"
        
        lscpu_cmd = "lscpu"
        cmd_result = Command.cmd_run(lscpu_cmd)
        res_lscpu = FileOperation.wrap_output_format(cmd_name, cmd_result, '-')
        
        dmidecode_cmd = "dmidecode -t processor | grep 'Socket Designation:\|Max Speed:\|Current Speed:'"
        cmd_result = Command.cmd_run(dmidecode_cmd)
        res_dmidecode = FileOperation.wrap_output_format(cmd_name, cmd_result, '-')

        cpuinfo_command="cat /proc/cpuinfo"
        cmd_result = Command.cmd_run(cpuinfo_command)
        res_cpuinfo = FileOperation.wrap_output_format(cmd_name, cmd_result, '=')
        
        res_all = res_lscpu + res_dmidecode + res_cpuinfo
        return Command.cmd_write_file(res_all, self.__default_file_name)

    @GlobalCall.monitor_info_thread_pool.threaded_pool
    def __get_pid_cpustat_info(self):
        '''
            pidstat
        '''
        pidstat_command = "pidstat -w 1 1"
        cmd_name = 'pidstat'
        cmd_result = Command.cmd_run(pidstat_command)
        res_all = FileOperation.wrap_output_format(cmd_name, cmd_result,'-')
        
        pidstat_command="pidstat |sort -ir -k 9"
        for i in range(5):
            cmd_result = Command.cmd_run(pidstat_command)
            if i == 0 : 
                result = cmd_result.split('\n',1)[0] + '\n' + cmd_result.split('\n',1)[1].rsplit('\n',3)[1] + '\n\n'
            result += cmd_result.split('\n',1)[1].rsplit('\n',3)[0] + '\n\n'
            
            sleep(1)
        res_all += FileOperation.wrap_output_format(cmd_name, result,'=')       
        return Command.cmd_write_file(res_all, self.__default_file_name)
   
    @GlobalCall.monitor_info_thread_pool.threaded_pool
    def __get_mpstat_info(self, interval , times):
        '''
            mpstat
        '''
        mpstat_command="mpstat -P ALL {} {}".format(interval, times)
        cmd_result = Command.cmd_run(mpstat_command)
        cmd_name = 'mpstat'
        return Command.cmd_output(cmd_name, cmd_result, self.__default_file_name, '=')

    @GlobalCall.monitor_info_thread_pool.threaded_pool
    def __get_top_info(self, interval , times):
        '''
            top and uptime 
        '''
        top_command = "top -b -n 1"
        cmd_name_top = 'top'
        uptime_command="for i in {1..5}; do uptime; sleep 1; done"
        
        if not Command.cmd_exists('dstat'):
            return False
        
        cmd_result_1 = Command.cmd_run(uptime_command)
        #将uptime_command替换成‘uptime’
        cmd_result = "uptime" + "\n" + cmd_result_1.split('\n',1)[1]
        res_uptime = FileOperation.wrap_output_format(cmd_name_top, cmd_result,'-')
        
        dstat_command="dstat {} {}".format(interval, times)
        cmd_result = Command.cmd_run(dstat_command)
        res_dstat = FileOperation.wrap_output_format(cmd_name_top, cmd_result,'-')
        
        cmd_result = Command.cmd_run(top_command)
        res_top = FileOperation.wrap_output_format(cmd_name_top, cmd_result,'=')
        
        res = res_uptime + res_dstat + res_top 
        return Command.cmd_write_file(res, self.__default_file_name)

    def __get_numastat_info(self):
        '''
            Get numastat information
        '''
        cmd_numactl = "numactl -H"
        cmd_numastat = "numastat -c"
        interval = 10
        
        if not Command.cmd_exists(cmd_numactl):
            return False
        if not Command.cmd_exists(cmd_numastat):
            return False
        
        #为保证两条命令输出到txt的位置必须相邻
        #需要先把两条numa命令的data 包装成可输出txt的格式，使用两次FileOperation.wrap_output_format
        #再统一进行输出到txt，使用Command.cmd_write_file
        
        #1.包装numactl命令
        cmd_result = Command.cmd_run(cmd_numactl)
        res_numactl = FileOperation.wrap_output_format('numactl', cmd_result,'-')
        
        res = Command.cmd_run(cmd_numastat)
        if len(res) == 0:
            return False
        sleep(interval)
        res += "\n\nsleep " + str(interval) + "seconds.....\n\n"
        res += Command.cmd_run(cmd_numastat)
        #2.包装numastat命令
        res_numastat = FileOperation.wrap_output_format('numactl', res,'=')
        
        #3.输出txt
        res_all = res_numactl + res_numastat
        return Command.cmd_write_file(res_all, self.__default_file_name)
    
    def __get_sar_task1(self, interval, times):
        cmd_name = 'sar'
        sar_command ="sar {} {}".format(interval, times)
        sar_result = Command.cmd_run(sar_command)
        #return Command.cmd_output(cmd_name, sar_result, self.__default_file_name, '=')
        res_sar = FileOperation.wrap_output_format(cmd_name, sar_result,'-')
        return res_sar
    
    def __get_sar_task2(self):
        cmd_name = 'sar'
        sar_all_command = "sar -u ALL -P ALL -q -r -B -W -d -p -n DEV -n EDEV 1 3"
        sar_all_result = Command.cmd_run(sar_all_command)
        res_sar_all = FileOperation.wrap_output_format(cmd_name, sar_all_result,'=')
        return res_sar_all

    @GlobalCall.monitor_info_thread_pool.threaded_pool
    def __get_sar_info(self, interval, times):
        '''
            sar
        '''
        task1 = CustomizeFunctionThread(self.__get_sar_task1, (interval, times))
        task2 = CustomizeFunctionThread(self.__get_sar_task2)
        task1.start()
        task2.start()        
        task1.join()           
        task2.join()
        
        res_all = task1.get_result() + task2.get_result() # res_sar + res_sar_all
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
