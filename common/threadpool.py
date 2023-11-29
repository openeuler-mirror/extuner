# -*- coding:utf-8 -*-
#!/usr/bin/env python
# cython:language_level=3

import functools
from concurrent.futures import ThreadPoolExecutor
from common.decorator_wrap import DecoratorWrap

@DecoratorWrap.singleton
class ThreadPool():
    def __init__(self, max_threads = 10):
        # Maximum concurrent threads
        self.__max_threads = max_threads
        self.__thread_obj = ThreadPoolExecutor(self.__max_threads)
        # Store the created thread
        self.__generate_list = []
    
    def threaded_pool(self, func):
        '''
            Externally callable thread pool decorator
        '''
        @functools.wraps(func)
        def inner(*args, **kwargs):
            obj = self.__thread_obj.submit(func, *args)
            self.__generate_list.append(obj)
        return inner
    