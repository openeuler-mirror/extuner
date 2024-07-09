#!/usr/bin/env python
# -*- coding: UTF-8 -*- 
# cython:language_level=3

import sys
from common.config import Config
from common.decorator_wrap import DecoratorWrap
from common.global_call import GlobalCall

@DecoratorWrap.singleton
class GlobalParameter:
    def __init__(self):
        if not sys.version_info[0] >= 3:
            default_disk_dev = ''.encode('utf-8')
        else:
            default_disk_dev = ''
            
        # *-----------------------get cpu info-------------------
        # 默认时间间隔为1s
        self.g_cpu_interval = GlobalCall.get_json_value("Getting.Common.CPU.interval", 1, Config.get_json_dict())
        # 默认执行5次
        self.g_cpu_times = GlobalCall.get_json_value("Getting.Common.CPU.times", 5, Config.get_json_dict())
        # 默认执行15秒,perf stat专用参数
        self.g_perf_stat_duration = GlobalCall.get_json_value("Getting.Common.CPU.duration", 15, Config.get_json_dict())

        # *-----------------------get memory info-------------------
        # 默认时间间隔为1s
        self.g_mem_interval = GlobalCall.get_json_value("Getting.Common.Memory.interval", 1, Config.get_json_dict())
        # 默认执行5次
        self.g_mem_times    = GlobalCall.get_json_value("Getting.Common.Memory.times"   , 5, Config.get_json_dict())

        # *-----------------------get disk info-------------------
        # 默认时间间隔为1s
        self.g_disk_interval = GlobalCall.get_json_value("Getting.Common.Disk.interval", 1, Config.get_json_dict())
        
        # 默认执行5次
        self.g_disk_times = GlobalCall.get_json_value("Getting.Common.Disk.times"          , 5, Config.get_json_dict())

        #默认不采集blktrace
        self.g_disk_bt_enable = GlobalCall.get_json_value("Getting.Common.Disk.enable_blktrace", 0)
        
        #blktrace默认采集时长为10s
        self.g_disk_bt_intval = GlobalCall.get_json_value("Getting.Common.Disk.seconds"        , 10)

        #blktrace采集dev块名，多个dev块使用‘，’分隔
        self.g_disk_bt_devlst = GlobalCall.get_json_value("Getting.Common.Disk.dev"            , default_disk_dev, Config.get_json_dict())

        # *-----------------------get net info-------------------
        # 默认时间间隔为1s
        self.g_net_interval = GlobalCall.get_json_value("Getting.Common.Net.interval", 1, Config.get_json_dict())
        # 默认执行5次
        self.g_net_times    = GlobalCall.get_json_value("Getting.Common.Net.times", 5, Config.get_json_dict())

        # *-----------------------get jvm info-------------------
        # 默认pid为1
        self.g_jvm_pid      = GlobalCall.get_json_value("Getting.Application.JVM.pid"     , 1, Config.get_json_dict())

    # -------------------cpu parameters----------------------- 
    @property
    def get_cpu_interval(self):
        return self.g_cpu_interval
    
    @property
    def get_cpu_times(self):
        return self.g_cpu_times
    
    @property
    def get_perf_stat_duration(self):
        return self.g_perf_stat_duration

       # -------------------memory parameters-----------------------
    @property
    def get_mem_interval(self):
        return self.g_mem_interval

    @property
    def get_mem_times(self):
        return self.g_mem_times

    # -------------------disk parameters----------------------- 
    @property
    def get_disk_interval(self):
        return self.g_disk_interval    
    
    @property   
    def get_disk_times(self):
        return self.g_disk_times
   
    @property  
    def get_disk_bt_enable(self):
        return self.g_disk_bt_enable

    @property  
    def get_disk_bt_intval(self):
        return self.g_disk_bt_intval
    
    @property  
    def get_disk_bt_devlst(self):
        return self.g_disk_bt_devlst

    # -------------------net parameters----------------------- 
    def get_net_interval(self):
        return self.g_net_interval
    
    def get_net_times(self):
        return self.g_net_times

    # -------------------jvm parameters-----------------------
    def get_jvm_pid(self):
        return self.g_jvm_pid
