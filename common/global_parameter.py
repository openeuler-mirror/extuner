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
        
    
    # -------------------cpu parameters----------------------- 
    @property
    def get_cpu_interval(self):
        return self.g_cpu_interval
    
    @property
    def get_cpu_times(self):
        return self.g_cpu_times
    
    
    