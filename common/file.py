#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# cython:language_level=3

import io
import json5
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
    
    @staticmethod
    def write(data, file_name):
        '''
            write to the file
        '''
        full_file_name = Config.get_output_path() + file_name
        with io.open(full_file_name, mode='a', encoding='utf-8') as file_obj:
            file_obj.write(data)
            
    @staticmethod
    def write_json_file(data_dict, file_name):
        '''
            Write dict type content to json file
        '''
        full_file_name = file_name
        js_obj = json5.dumps(data_dict, indent=4)
        full_file_name = Config.get_output_path() + file_name
        with io.open(full_file_name, mode='a', encoding='utf-8') as file_obj:
            file_obj.write(js_obj)
