#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# cython:language_level=3
# Copyright (c) 2023 KylinSoft  Co., Ltd. All Rights Reserved.

import time
from common.config import Config

class KyReport:

    def ky_build(self, work, inst, tm):
        curr_time = time.strftime("%m%d%H%M")
        srcfile   = Config.get_inst_path()   + 'kyreport/extuner_report.html'
        outfile   = Config.get_output_path() + 'extuner_report_' + curr_time + '.html'
        info      = {
                'tm_info'  : { 'start': '', 'stop': '' },
                'base_info': {
                    'hostname'      : '',
                    'system_version': '',
                    'kernel_version': '',
                    'gcc_version'   : '',
                    'glibc_version' : '',
                    'jdk_version'   : '',
                    'net_sum'       : [],
                    'disk_sum'      : [],
                    'cpu_model'     : '',
                    'cpu_arch'      : '',
                    'cpu_cores'     : '',
                    'mem_total'     : '',
                    'mem_free'      : '',
                    'mem_available' : ''
                },
                'cpu_info' : [],
                'mem_info' : [],
                'net_info' : [],
                'io_info'  : [],
                'synthesis_info'  : [],
                'jvm_info' : [],
                'sys_param': [],
                'sys_msg'  : [],
                'hotspot_info': [],
            }

