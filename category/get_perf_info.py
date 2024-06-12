#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# cython:language_level=3

import io
import os
import sys
import base64

# Global Variable - start
perf_enable_flag = 0
# Global Variable - end


# Common Functions
def convert_str(value):
    if not sys.version_info[0] >= 3:
        return value.encode('utf-8')
    else:
        return value

# hotspot main function
class Hotspot():
	def __init__(self):
		pass


