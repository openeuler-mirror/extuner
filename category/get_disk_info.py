#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# cython:language_level=3

import os
from common.file import FileOperation

class DiskInfo:
    def __init__(self, t_fileName):
        self.__default_file_name = t_fileName
        self.__bt_devlst = []
        FileOperation.remove_txt_file(self.__default_file_name)
