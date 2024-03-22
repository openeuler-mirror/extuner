#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# cython:language_level=3

from common.file import FileOperation

class SysParamInfo:
    '''
        System parameter class
    '''
    def __init__(self, t_fileName):
        self.__default_file_name = t_fileName
