#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# cython:language_level=3

import argparse
import datetime
import sys
import platform

from common.command import Command

class ToolCmd:
        
    def __get_version(self):
        # line = 'extuner version is 1.0. ' + 'Expires at ' + str(self.__last_day)
        line = 'Extuner version is 1.0. ' 
        return line

    # start add for perf/offcpu command line parser check
    def __check_perf_cmdline(self, args):
        error_msg = []
        if args.perf_enable_type:
            if not args.perf_pid:
                error_msg = "need to specify --pid option"
                return error_msg
        if not args.perf_enable_type:
            if args.perf_pid or args.perf_duration:
                error_msg = "need to specify --perf option"
                return error_msg
        return error_msg

    def args_help(self):
        #共享可选参数wpath ipath opath
        parent_parser = argparse.ArgumentParser(add_help=False)
        parent_parser.add_argument('--work_path', type = str, default = '.', 
                                   help=argparse.SUPPRESS)
                                   #help = 'User can specify the conf path. default is /usr/share/extuner/conf')
        parent_parser.add_argument('--inst_path', type = str, default = '.', 
                                   help = argparse.SUPPRESS)
        parent_parser.add_argument('-o','--out_path', type = str, default = '.', 
                                   help = 'include log and report, default is current directory')
        #共享可选参数version
        vparent_parser = argparse.ArgumentParser(add_help=False)
        vparent_parser.add_argument('-v','--version' , action = 'version', version = self.__get_version(), 
                                    help = 'version')
        
        #共享可选参数cust_col  收集脚本
        cparent_parser = argparse.ArgumentParser(add_help=False)
        cparent_parser.add_argument('--add',   help = 'Extra collection data')
      
        #extuner命令
        parser = argparse.ArgumentParser(
            description='''description:\n  extuner is an expert tuning tool for Kylin system''',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            prog='extuner',
            parents=[vparent_parser],
            usage=''' \n  extuner <COMMAND> [options] ''',
            epilog='''examples:\n    extuner collection --perf --pid -1''')
        
        subparsers = parser.add_subparsers(title = 'commands',prog='extuner',metavar=' ')
        #子命令extuner collection
        desc_c = 'collect the system data,such as CPU/MEM/NET/IO'
        parser_col = subparsers.add_parser('collection',
            parents=[parent_parser], 
            description='''description:\n  {}'''.format(desc_c),
            formatter_class=argparse.RawDescriptionHelpFormatter,
            help='* {}'.format(desc_c))

        parser_col.add_argument('--func', type = str, default = 'col', 
                                   help = argparse.SUPPRESS)      
                
        args = parser.parse_args()
       
        return args
    
    
