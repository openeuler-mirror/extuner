#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# cython:language_level=3

from common.file import FileOperation

# jvm class
class JVMInfo:
    def __init__(self, t_fileName):
        # output file
        self.__default_file_name = t_fileName
        FileOperation.remove_txt_file(self.__default_file_name)