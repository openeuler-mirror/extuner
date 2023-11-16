#!/usr/bin/env python
# -*- coding: UTF-8 -*- 
# cython:language_level=3

from extuner import main
from common.log import Logger

# main function
if __name__=='__main__': 
    main()
    # try:
    #     main()
    # except Exception as err:
    #     Logger().error("Error: {}".format(err))