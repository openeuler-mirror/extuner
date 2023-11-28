#!/usr/bin/env python
# -*- coding: UTF-8 -*- 
# cython:language_level=3

class DecoratorWrap:
    @staticmethod
    def singleton(cls):
        '''
            singleton decorator
        '''
        instances = {}
        def _singleton(*args, **kwargs):
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)
            return instances[cls]

        return _singleton
