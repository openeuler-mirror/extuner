# -*- coding:utf-8 -*-
#!/usr/bin/env python
# cython:language_level=3

import subprocess
import os
import sys
from common.log import Logger

class Command:
    
    @staticmethod
    def call(cmd, caller = ''):
        '''
            Encapsulated CALL function to return abnormal location information
        '''
        if(subprocess.call(cmd, shell = True)):
            raise Exception("{} : [{}] Failed to execute!".format(caller, cmd))

    @staticmethod
    def check_ethtool_cg(cmd_stde):
        if cmd_stde == b"Cannot get device coalesce settings: Operation not supported\n":
            return True
        elif cmd_stde == b"Cannot get device ring settings: Operation not supported\n":
            return True
        else:
            return False

    @staticmethod
    def cmd_check(cmd_stdo, cmd_stde, cmd_returncode, cmd):
        if cmd_returncode and Command.check_ethtool_cg(cmd_stde):
            Logger().warning("{} : {}".format(cmd, cmd_stde.decode('utf8')))
            return False
        elif cmd_returncode:
            if len(cmd_stde) != 0:
                Logger().warning("{}".format(cmd_stde.decode('utf8')))
            # else:
            #     Logger().error("exec command {} failed! ".format(cmd))
            return False
        else:
            return True

    @staticmethod
    def cmd_run(cmd,  caller = ''):
        '''
            Encapsulate the general RUN function, get the result 
        '''
        command_result = ''
        try:
            env_c = os.environ
            env_c['LANG'] = 'en_US.UTF-8'
            
            check_cmd = cmd.split()
            if check_cmd[0] == 'cat' or check_cmd[0] == 'ls':
                if not os.path.exists(check_cmd[1]):
                    Logger().error("{} 不存在, cmd_run 命令 {} 无法执行".format(check_cmd[1], cmd))
                    return command_result
            
            ret = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE , stderr = subprocess.PIPE, env = env_c)
            stdout,stderr = ret.communicate()
            if not sys.version_info[0] >= 3:
                stdout = stdout.replace('\x1b[7l', '')
            if Command.cmd_check(stdout, stderr, ret.returncode, cmd):
                command_result = cmd + '\n'+ stdout.decode('utf8')
                
            return command_result
                       
        except Exception as err:
            Logger().error("An exception occurred when executing [{}]: {}".format(cmd, err))
            return command_result

    @staticmethod
    def cmd_exec(cmd,  caller = ''):
        '''
            Encapsulate the general RUN function, get the result 
        '''
        command_result = ''
        try:
            env_c = os.environ
            env_c['LANG'] = 'en_US.UTF-8'
            # 添加文件是否存在判断
            check_cmd = cmd.split()
            if check_cmd[0] == 'cat' or check_cmd[0] == 'ls':
                if "scaling_governor" in check_cmd[1] :
                    if len(os.listdir("/sys/devices/system/cpu/cpufreq/")) == 0:
                        Logger().debug("命令 {} 无法执行, 已经处于性能模式".format(cmd))
                        return command_result
                elif not os.path.exists(check_cmd[1]):
                    Logger().error("{} 不存在，命令 {} 无法执行".format(check_cmd[1], cmd))
                    return command_result
            # ret = subprocess.run(cmd, shell = True, stdout = subprocess.PIPE , stderr = subprocess.PIPE, env = env_c)
            ret = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE , stderr = subprocess.PIPE, env = env_c)
            stdout,stderr = ret.communicate()
            if Command.cmd_check(stdout, stderr, ret.returncode, cmd):
                command_result = stdout.decode('utf8')
            return command_result.strip()
                       
        except Exception as err:
            Logger().error("An exception occurred when executing [{}]: {}".format(cmd, err))
            return command_result


    @staticmethod
    def cmd_exec_err(cmd,  caller = ''):
        '''
            Encapsulate the general RUN function, get the result 
        '''
        command_result = ''
        try:
            env_c = os.environ
            env_c['LANG'] = 'en_US.UTF-8'
            # ret = subprocess.run(cmd, shell = True, stdout = subprocess.PIPE , stderr = subprocess.PIPE, env = env_c)
            ret = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE , stderr = subprocess.PIPE, env = env_c)
            stdout,stderr = ret.communicate()
            if Command.cmd_check(stdout, stderr, ret.returncode, cmd):
                command_result = stderr.decode('utf8')
            return command_result
                       
        except Exception as err:
            Logger().error("An exception occurred when executing [{}]: {}".format(cmd, err))
            return command_result

     