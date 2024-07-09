#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# cython:language_level=3

from common.file import FileOperation
from common.command import Command

# jvm class
class JVMInfo:
    def __init__(self, t_fileName):
        # output file
        self.__default_file_name = t_fileName
        FileOperation.remove_txt_file(self.__default_file_name)
        
        
    def __get_heap_usage_info(self):
        '''
            Get the java heap usage
        '''
        devices_command="jmap -heap {}".format(self.__pid)
        cmd_result = Command.cmd_run(devices_command)
        return Command.cmd_output("jmap -heap", cmd_result, self.__default_file_name, '=')