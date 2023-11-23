# -*- coding:utf-8 -*-
#!/usr/bin/env python
# cython:language_level=3


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

    