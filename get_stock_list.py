#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @version: 1.0
# @author: moses
# @file: get_stock_list
# @time: 11/8/17 9:19 AM

import subprocess
import sys

def download_list():
    try:
        subprocess.call('wget -O temp1.html \"http://quote.eastmoney.com/stocklist.html\"', shell=True)
        subprocess.call('iconv -f GBK -t UTF-8 temp1.html -o temp2.html', shell=True)
    except:
        print 'check your network!'
        sys.exit(0)

def create_list_file():
    download_list()
    arr1 = []
    with open('temp2.html','rb') as f:
        for i in f:
            if '<li><a target="_blank" href="http://quote.eastmoney.com/' in i:
                j = i.split(')')[0].split('>')[-1]
                k = j.split('(')
                arr1.append('%s\t%s' % (k[1], k[0]))
    with open('stock_list_all.log', 'wb') as f:
        for i in arr1:
            # print i
            f.write('%s\n' % i)
    subprocess.call('rm -f temp1.html',shell=True)
    subprocess.call('rm -f temp2.html',shell=True)

# create_list_file()