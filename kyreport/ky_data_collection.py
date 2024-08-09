#!/usr/bin/env python
# -*- coding: UTF-8 -*- 
# cython:language_level=3
# Copyright (c) 2023 KylinSoft  Co., Ltd. All Rights Reserved.

import io
import os
from common.config import Config
from common.decorator_wrap import DecoratorWrap
from common.log import Logger
from common.global_parameter import GlobalParameter

@DecoratorWrap.singleton
class DATACOLLECTION:
    def __init__(self):
        self.__arr_synthesis_info = []
        
        self.collection_cpu_txt_data(Config.get_output_path() + 'CPUInfo.txt')
        
    def collection_cpu_txt_data(self, fname  = ''):
        try:
            flg_cmd = '=========================kylin========================='
            flg_sub = '-------------------------kylin-------------------------'

            if not os.path.exists(fname):
                Logger().warning("Report file not found: {}".format(fname))

            else:
                with io.open(file = fname, mode = 'r', encoding = 'utf-8') as fp:
                    txt = fp.read()
                    cmd_grp = txt.strip()[:-len(flg_cmd)].split(flg_cmd)
                    for grp in cmd_grp:
                        grp_obj = { 'group': '' , 'sub': [] }
                        cmd_sub = grp.strip().split(flg_sub)
                        for sub in cmd_sub:
                            sub_obj = { 'cmd': '', 'res': '' }
                            sub_arr = sub.strip().split('\n', 2)
                            if 3 == len(sub_arr):
                                sub_g = sub_arr[0].split('Command: ')[1]
                                sub_s = sub_arr[1].split('SubCommand: ')[1]
                                sub_c = sub_arr[2]
                                
                                sub_obj['cmd']   = sub_s
                                sub_obj['res']   = sub_c

                                if sub_s == GlobalParameter().sub_sarall:
                                    dict_synthesis = {'group': '' , 'sub': []}
                                    dict_synthesis["group"] = sub_g
                                    dict_synthesis["sub"].append(sub_obj)
                                    self.__arr_synthesis_info.append(dict_synthesis)
                                    continue
                                
                                grp_obj['group'] = sub_g
                                grp_obj['sub'].append(sub_obj)                            
        
        except Exception as err:
            Logger().error('Failed parse file "{}": {}'.format(fname, err))
            
