#!/usr/bin/env python
# -*- coding: UTF-8 -*- 
# cython:language_level=3

from common.log import Logger
from common.tool_cmd import ToolCmd
from summary_info import SummaryInfo

# main function
# if __name__=='__main__': 
def main():

    Timer = { "start": "", "stop": "" }
    ret = False
    args = ToolCmd().args_help()
    func = args.func


    if args.work_path == '':
        work_path = '/usr/share/extuner/'
    else:
        work_path = args.work_path
        
    if args.inst_path == '':
        inst_path = '/usr/share/extuner/'
    else:
        inst_path = args.inst_path
    
    out_path = args.out_path

    SummaryInfo.init(out_path,work_path, inst_path)
    Logger().info("Extuner 开始执行")