# -*- coding:utf-8 -*-
#!/usr/bin/env python
# cython:language_level=3

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
        