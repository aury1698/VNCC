# Copyright (c) Alex Ellis 2017. All rights reserved.
# Copyright (c) OpenFaaS Author(s) 2018. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import sys
#from function import handler
from handler import handle

def get_stdin():
    buf = ""
    while(True):
        line = sys.stdin.readline()
        buf += line
        if line == "" or line == "\n":
            break
    return buf

if __name__ == "__main__":
    st = get_stdin()
    #ret = handler.handle(st)
    ret = handle(st)
    if ret != None:
        print(ret)
