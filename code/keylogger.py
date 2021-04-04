#!bin/env python3
import sys
from datetime import datetime

def timestamp_ms():
    dt = datetime.now()
    return int(dt.microsecond + (dt.second + dt.day * 86400) * 10**6) // 10**3

if __name__ == '__main__':
    
    start = timestamp_ms()
    line = sys.stdin.readline()
    while line != '':
        print(line)
        line = sys.stdin.readline()
    
