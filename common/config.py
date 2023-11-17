#!/usr/bin/env python
# -*- coding: UTF-8 -*- 
# cython:language_level=3

import io
import json5
import os
import sys
import time

# Initialize classes, load working directory and output directory, etc.
class Config:
    @staticmethod
    def init_config(opath, wpath , ipath ):
        '''
            Initialize working directory information, must be called
        '''
        Config.set_work_path(wpath)
        Config.set_inst_path(ipath)
        Config.set_out_path(opath)
        
        try:
            with io.open(Config.conf_fn, 'r', encoding='utf-8') as file:
                Config.dict_json = json5.load(file)
        except Exception as err:
            print("程序初始化失败: 配置文件内容设置异常 {}，请修改后重新启动程序。".format(err))
            sys.exit()

        if not os.path.exists('{}/output-{}/'.format(Config.out_path, Config.dt)):
            os.makedirs('{}/output-{}/'.format(Config.out_path, Config.dt))

        if not os.path.exists(Config.out_path + '/log/'):
            os.makedirs(Config.out_path + '/log/')

        # if not os.path.exists(Config.out_path+'/temp/'):
        #     os.makedirs(Config.out_path + '/temp/') 

    