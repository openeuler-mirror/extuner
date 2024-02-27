#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# cython:language_level=3
#!coding=utf-8

import sys

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

from common.decorator_wrap import DecoratorWrap

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
