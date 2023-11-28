#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# cython:language_level=3

import os
from common.config import Config

# file operation class
class FileOperation:

    @staticmethod
    def remove_txt_file(file_name):
        '''
            empty file
        '''
        if os.path.exists(Config.get_output_path() + file_name):
            os.remove(Config.get_output_path() + file_name)
        else:
            # os.mkdir(Config.get_output_path() + file_name)
            file = open(Config.get_output_path() + file_name,'w')
            file.close()
