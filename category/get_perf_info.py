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

# Perf Class
class Perf():
    def __init__(self):
        pass

    def __set_perf_parameter(self):
        if len(perf_args) == 0:
            self.__enable = GlobalCall.get_json_value("Getting.Application.Perf.enable", 0, Config.get_json_dict())
            self.__pid = GlobalCall.get_json_value("Getting.Application.Perf.pid", convert_str('-1'), Config.get_json_dict())
            self.perf_duration = GlobalCall.get_json_value("Getting.Application.Perf.duration", 15, Config.get_json_dict())
        else:
            self.__enable = int(perf_args['perf_enable_type'])
            self.__pid = convert_str(perf_args['perf_pid'])
            self.perf_duration = int(perf_args['perf_duration'])

        self.freq = 99
        self.perf_data_path = Config.get_output_path()
        self.perf_data_file = '{}{}'.format(self.perf_data_path,'perf.data')
        self.perf_svg_file_0 = '{}{}'.format(self.perf_data_path,'perf_0.svg')
        self.perf_svg_file = '{}{}'.format(self.perf_data_path,'perf.svg')
        self.perf_svg_errfile = '{}{}'.format(self.perf_data_path,'perf_svg_err.tmp')
        self.flamegraph_tool_path = '{}{}/{}/'.format(Config.get_inst_path(), 'third_party', 'FlameGraph')

        # perf report filter by default
        self.perf_report_errfile_default = '{}{}'.format(self.perf_data_path,'perf_report_err.tmp')
        self.perf_report_file_default = '{}{}'.format(self.perf_data_path, 'perf.txt')

        # perf report filter use a same err file to log
        self.perf_report_errfile_filter = '{}{}'.format(self.perf_data_path,'perf_report_err.filter')
        # perf report filter by --no-children --sort comm,dso,symbol
        self.perf_report_file_filter1 = '{}{}'.format(self.perf_data_path, 'perf_1.txt')
        # perf report filter by -sort comm,dso,symbol
        self.perf_report_file_filter2 = '{}{}'.format(self.perf_data_path, 'perf_2.txt')

    def __check_perf_command(self):
        if not Command.cmd_exists('perf'):
            return False
        else:
            return True

    # start add for extuner.conf parser, should consistent with command line parsing
    def __check_perf_enable_value(self):
        #if self.__enable == 0:
        #    Logger().debug("Application.Perf.enable = 0, 不进行Perf数据采集")
        #    return False

        if self.__enable != 0 and self.__enable not in perf_enable_list:
            Logger().error("Application.Perf.enable 参数值不可用")
            return False
        else:
            return True

# OffCPU Class
class OffCPU():
	def __init__(self):
		self.__get_kernel_version()

	def __get_kernel_version(self):
		try:
			self.kernel_version = Command.cmd_exec('cat /proc/version').split()[2]
		except Exception as err:
			Logger().error("Error: {}".format(err))

    def __diff_kernel_version(self, dest):
        res = True
        # only compare major and minor part
        iteration_len = 2
        k = self.kernel_version.split(".")
        d = dest.split(".")
        if len(k) < iteration_len or len(d) < iteration_len:
            Logger().error("kernel version used to compare must contain major and minor part.")
            return None
        for i in range(iteration_len):
            if int(k[i]) == int(d[i]):
                res = True
            elif int(k[i]) < int(d[i]):
                res = False
                break
            else:
                res = True
                break
        return res

    def __check_offcpu_command(self):
        if not Command.cmd_exists(self.offcputime_tool):
            return False
        else:
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

