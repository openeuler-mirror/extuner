#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# cython:language_level=3

from category.get_net_info import NetInfo
from category.get_cpu_info import CPUInfo
from category.get_disk_info import DiskInfo
from category.get_sysparam_info import SysParamInfo 
from common.config import Config
from common.log import Logger
from common.global_call import GlobalCall


# Access to information for external use
class SummaryInfo:
    @staticmethod
    def init(out_path , work_path , inst_path ):
        '''
            initialization, must be called first
        '''
        Config.init_config(out_path, work_path, inst_path)
        # Specify debug mode
        # Logger().on_debug_type()

    @staticmethod
    def get_info():
        '''
            A function that collects all information, called externally
        '''
                
        if GlobalCall.get_json_value('Getting.Common.enable', 1) == 1:

            if not NetInfo(GlobalCall.output_net_file).get_info():
                Logger().error("Failed to obtain network status due to an error in obtaining network card information !") 
            Logger().info(u"网络数据采集完成")
            
            CPUInfo(GlobalCall.output_cpu_file).get_info()
            Logger().info(u"CPU数据采集完成")

            DiskInfo(GlobalCall.output_disk_file).get_info()
            Logger().info(u"磁盘数据采集完成")

            SysParamInfo(GlobalCall.output_sys_param_file).get_info()
            Logger().info(u"系统参数采集完成")        
            
            return True
        else:
            Logger().warning("配置文件中关闭数据获取功能, Getting.Common.enable = {}".format(GlobalCall.get_json_value('Getting.Common.enable', 1)))
            return False
            
