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
offcpu_enable_flag = 0
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
            Logger().debug("{} : {} ".format(cmdname, tmp_txt))

        # 对无法生成报告的错误进行处理
        perf_report_error_type1 = 'file has no samples'
        if cmdname == 'perf report':
            if perf_report_error_type1 in tmp_txt:
                # perf report -i perf.data的时候，提示The perf.data file has no samples!
                Logger().debug("{}异常, 文件路径: {}".format(cmdname, err_filename))
                return False
            else:
                # 例如：perf report -i perf.data的时候，
                #       若提示Failed to open /tmp/perf-xxxx.map, continuing without symbols
                #       这时候，其实是可以得到输出的，因此需要返回True
                return True
        else:
            # 暂不处理
            return False
    else:
        if os.path.exists(err_filename):
            os.remove(err_filename)
        return True

def replace_invisible_chars(input_file, output_file, flag):
    if not flag:
        # 制表符和换行符不进行替换
        invisible_chars_pattern = re.compile(r'[\x00-\x08\x0B-\x1F\x7F]')
    else:
        invisible_chars_pattern = re.compile(r'[\x00-\x1F\x7F]')

    with io.open(file = input_file, mode = 'r', encoding = 'utf-8') as fp:
        origin_content = fp.read()

    new_content = invisible_chars_pattern.sub('', origin_content)

    with io.open(file = output_file, mode = 'w', encoding = 'utf-8') as fp:
        fp.write(new_content)

    return True

# hotspot main function
class Hotspot():
	def __init__(self):
		pass

	def get_hotspot_report_flag(self):
		if perf_enable_flag != 0 or offcpu_enable_flag != 0:
			return True
		else:
			return False

