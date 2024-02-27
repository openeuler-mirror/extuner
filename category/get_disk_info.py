#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# cython:language_level=3

import os
from common.file import FileOperation
from common.command import Command

class DiskInfo:
    def __init__(self, t_fileName):
        self.__default_file_name = t_fileName
        self.__bt_devlst = []
        FileOperation.remove_txt_file(self.__default_file_name)

    def __get_fdisk_info(self):
        '''
            fdisk -l and blkid
        '''
        fdisk_command="fdisk -l"
        cmd_name = fdisk_command 
        cmd_result = Command.cmd_run(fdisk_command)
        res_fdisk = FileOperation.wrap_output_format(cmd_name, cmd_result, '-')
        blkid_command="blkid"
        cmd_result = Command.cmd_run(blkid_command)
        res_blkid = FileOperation.wrap_output_format(cmd_name, cmd_result, '=')
        
        res_all = res_fdisk + res_blkid
        return Command.cmd_write_file(res_all, self.__default_file_name)
    
    def __get_df_h_info(self):
        '''
            exec df -h
        '''
        df_h_command="df -h"
        cmd_result = Command.cmd_run(df_h_command)
        cmd_name = df_h_command
        return Command.cmd_output(cmd_name, cmd_result, self.__default_file_name, '=')