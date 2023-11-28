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

    @staticmethod
    def wrap_output_format(cmd_name, data, split):
        '''
            wrap file format to data , use --- or === split and return 
            do not write file
        '''
        out = 'Command: ' + cmd_name + '\nSubCommand: ' + data
        if split == '=':
            out = out + "=========================kylin=========================\n"
        else:
            out = out + "-------------------------kylin-------------------------\n"
        
        return out
    