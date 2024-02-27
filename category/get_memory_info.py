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
