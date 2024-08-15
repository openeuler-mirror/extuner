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

