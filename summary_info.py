#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# cython:language_level=3


from common.config import Config


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
