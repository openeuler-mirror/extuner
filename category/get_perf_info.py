#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# cython:language_level=3

import io
import os
import sys
import base64

from common.config import Config
from common.command import Command
from common.global_call import GlobalCall
from common.log import Logger
from common.file import FileOperation
import re

# Global Variable - start
perf_enable_flag = 0
# Global Variable - end


# Common Functions
def convert_str(value):
    if not sys.version_info[0] >= 3:
        return value.encode('utf-8')
    else:
        return value

# 执行perf命令的时候，出现$?为0，但是其实是有error信息产生
def is_errfile_empty(cmdname, err_filename):
    if os.path.getsize(err_filename):
        # 将异常信息记录到日志中
        with io.open(file = err_filename, mode = 'r', encoding = 'utf-8') as fp:
            tmp_txt = fp.read()
    else:
        if os.path.exists(err_filename):
            os.remo

# hotspot main function
class Hotspot():
	def __init__(self):
		pass


