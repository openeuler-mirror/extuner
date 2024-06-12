#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# cython:language_level=3
# Copyright (c) 2023 KylinSoft  Co., Ltd. All Rights Reserved.

from common.command import Command

# System log class
class SysMessage():
    def __init__(self, t_fileName):
        self.__default_file_name = t_fileName

    def __get_system_message(self):
        '''
            get system log
        '''
        mem_command="dmesg -T"
        cmd_result = Command.cmd_run(mem_command)
        return Command.cmd_output(mem_command, cmd_result, self.__default_file_name, '=')

    def get_info(self):
        self.__get_system_message()
