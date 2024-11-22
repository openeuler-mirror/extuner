#!/usr/bin/env python
# -*- coding: UTF-8 -*- 
# cython:language_level=3

from common.log import Logger
from common.tool_cmd import ToolCmd
from summary_info import SummaryInfo
from common.threadpool import ThreadPool
from kyreport.ky_report import KyReport
import time

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
    Timer["start"] = time.strftime("%Y-%m-%d %H:%M:%S")
    
    if 'col' == func:
        #get 功能
        ret = SummaryInfo.get_info()
    
    if ThreadPool().is_thread_working:
        ThreadPool().thread_finish()

    
    Timer["stop"] = time.strftime("%Y-%m-%d %H:%M:%S")

    KyReport().ky_build(Timer)

    Logger().info("Extuner 执行成功")
    # Logger().info("结果输出目录为 : {}".format(Config.path_format(os.path.abspath(Config.get_output_path()))))