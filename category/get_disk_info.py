#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# cython:language_level=3

import os
from common.file import FileOperation
from common.command import Command
from common.global_parameter import GlobalParameter

class DiskInfo:
    def __init__(self, t_fileName):
        self.__default_file_name = t_fileName
        self.__bt_devlst = []
        FileOperation.remove_txt_file(self.__default_file_name)
        # 默认时间间隔为1s
        self.__interval  = GlobalParameter().get_disk_interval()
        # 默认执行5次
        self.__times     = GlobalParameter().get_disk_times()
        #默认不采集blktrace
        self.__bt_enable = GlobalParameter().get_disk_bt_enable()
        #blktrace默认采集时长为10s
        self.__bt_intval = GlobalParameter().get_disk_bt_intval()
        #blktrace采集dev块名，多个dev块使用‘，’分隔
        self.__bt_devlst = GlobalParameter().get_disk_bt_devlst()

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
    
    def __get_fstab_info(self):
        '''
            exec cat /etc/fstab
        '''
        fstab_command="cat /etc/fstab"
        cmd_result = Command.cmd_run(fstab_command)
        return Command.cmd_output(fstab_command, cmd_result, self.__default_file_name, '=')
    
    def __get_blkid_info(self):
        '''
            get blkid information
        '''
        blkid_command="blkid"
        cmd_result = Command.cmd_run(blkid_command)
        return Command.cmd_output(blkid_command, cmd_result, self.__default_file_name, '=')
    
    def __get_iostat_info(self, interval, times):
        '''
            get iostat information
        '''
        iostat_command="iostat -xmt {} {}".format(interval, times)
        cmd_result = Command.cmd_run(iostat_command)
        cmd_name = 'iostat'
        return Command.cmd_output(cmd_name, cmd_result, self.__default_file_name, '=')
