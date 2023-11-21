#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# cython:language_level=3


from category.get_cpu_info import CPUInfo
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

            CPUInfo(GlobalCall.output_cpu_file).get_info()
            Logger().info(u"CPU数据采集完成")
        
            return True
        else:
            Logger().warning("配置文件中关闭数据获取功能, Getting.Common.enable = {}".format(GlobalCall.get_json_value('Getting.Common.enable', 1)))
            return False
            
