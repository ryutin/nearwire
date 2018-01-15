#!/usr/local/bin/python

import sys
import json
import re


json_file = open('chicago-il.json','r')

title_re = re.compile(r'"title": ')
start_space_re = re.compile('^\s+')

#title_re = re.compile('title')

with open('chicago-il.json') as my_file:
    for line in my_file:
        #print(line)
        if title_re.search(line):
            xline=re.sub(r'^\s+"',r'"',line)
            xline=re.sub(r' - [^"]+"',r'',xline)
            print(xline.rstrip())
