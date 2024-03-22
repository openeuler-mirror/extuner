#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# cython:language_level=3
#!coding=utf-8

import os
import sys

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

from common.decorator_wrap import DecoratorWrap
from common.file import FileOperation
from common.log import Logger
from common.command import Command

# net class
@DecoratorWrap.singleton
class NetInfo:
    def __init__(self, t_fileName):
        # network output file
        self.__default_file_name = t_fileName
        # network devices
        #获得所有网卡设备，包括虚拟网卡和物理网卡，格式为：NAME.TYPE
        self.__netdevice = {} 
        #获得已连接网卡设备，格式为：NAME.TYPE
        self.__netdev_act = {} 
        #获得支持ring buffer 的已连接网卡设备
        self.__netdev_ring = [] #
        #网卡连接状态信息
        self.__link_status = {}

    def __get_devices(self):
        '''
            Get all network card names
        '''

        ifc_all_dir  = '/sys/class/net/'
        ifc_virt_dir = '/sys/devices/virtual/net/'
        ifc_all  = list()
        ifc_virt = list()
        self.__netdevice  = dict()
        self.__netdev_act = dict()

        if not os.path.exists(ifc_all_dir):
            Logger().error("Unable to get all interface info, directory {} not exists: ".format(ifc_all_dir))
            return False
        elif not os.path.exists(ifc_virt_dir):
            Logger().error("Unable to get virtial interface info, directory {} not exists: ".format(ifc_virt_dir))
            return False
        
        
        ifc_all = os.listdir(ifc_all_dir)
        ifc_virt = os.listdir(ifc_virt_dir)

        for ifc in ifc_all:
            # 跳过虚拟网口
            if ifc in ifc_virt:
                continue

            self.__netdevice[ifc]  = 'ethernet'
            
            cmd = "ethtool {} | grep 'Link detected:' | cut -d ' ' -f 3".format(ifc)
            res = Command.cmd_run(cmd)
            if 'yes' in res.strip().lower():
                self.__netdev_act[ifc] = 'ethernet'
        
        return True
    
    def __get_devices_info(self):
        '''
            nmcli con show and ethtool
        '''
        cmd_name = "nmcli con show"
        res_list  = []
        res_e  = []
        res = ''
        
        devices_command="nmcli con show"
        cmd_result = Command.cmd_run(devices_command)
        res_list.append(cmd_result)
        
        for i, device in enumerate(self.__netdevice):
            type = self.__netdevice[device] 
            if type in ['bridge', 'ethernet']:
                cmd_result = Command.cmd_run('ethtool -i ' + device)
                res_list.append(cmd_result)

                cmd_result = Command.cmd_run('ethtool ' + device)
                for sent in reversed(cmd_result.split('\n')):
                    if 'Link detected' in sent:
                        status = sent.split(':',1)[1].strip()
                        self.__link_status[device] = status
                        break
                res_e.append(cmd_result)

        #wrap result 
        res_list += res_e
        for i,cmd_result in enumerate(res_list):
            split = '=' if i == len(res_list)-1 else '-'
            res += FileOperation.wrap_output_format(cmd_name, cmd_result, split)
        return Command.cmd_write_file(res, self.__default_file_name)
    
    def __get_eth_off_info(self):
        '''
            get net offload information
        '''
        cmd_name = "ethtool"
        res = ''
        res_list  = []
        
        for i, device in enumerate(self.__netdevice):
            type = self.__netdevice[device] 
            if type == 'ethernet' and self.__link_status[device] == 'yes':
                cmd_result = Command.cmd_run("ethtool -k " + device)
                res_list.append(cmd_result)
                cmd_result = Command.cmd_run("ethtool -c " + device) 
                res_list.append(cmd_result)
                cmd_result = Command.cmd_run("ethtool -g " + device) 
                if len(cmd_result) != 0 :
                    if device in self.__netdev_act.keys():
                        self.__netdev_ring.append(device)
                    res_list.append(cmd_result)
                        
        #wrap result 
        for i,cmd_result in enumerate(res_list):
            split = '=' if i == len(res_list)-1 else '-'
            res += FileOperation.wrap_output_format(cmd_name, cmd_result, split)

        return Command.cmd_write_file(res, self.__default_file_name)
    
    def __get_sar_DEV_task1(self, interval, times):
        # print("Sar_dev task 1 started")
        # get "sar -n DEV" command info
        sar_command ="sar -n DEV {} {}".format(interval, times)
        cmd_name = 'sar -n DEV'
        sar_result = Command.cmd_run(sar_command)
        res_d = FileOperation.wrap_output_format(cmd_name, sar_result, '-')
        # print("Sar_dev task 1 completed")
        return res_d
    
    def __get_sar_DEV_task2(self, interval, times):
        # print("Sar_dev task 2 started")
        # get "sar -n EDEV" command info
        sar_command ="sar -n EDEV {} {}".format(interval, times)
        cmd_name = 'sar -n DEV'
        sar_result_e = Command.cmd_run(sar_command)
        res_e = FileOperation.wrap_output_format(cmd_name, sar_result_e, '=')
        # print("Sar_dev task 2 completed")
        return res_e

    def get_info(self):
        '''
            Get network monitoring information external interface
        '''
        if not self.__get_devices():
            return False
        self.__get_devices_info()
        self.__get_eth_off_info()
        