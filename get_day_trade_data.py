#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @version: 1.0
# @author: moses
# @file: get_day_trade_data
# @time: 11/2/17 9:45 AM

import get_stock_list
import time
import subprocess
import os

class my_global(object):
    moses = 1

class get_day_trade_data(object):
    def __init__(self):
        self.moses = 1
        self.stock_num = []
        self.day = ''
        self.download_link_str = 'http://market.finance.sina.com.cn/downxls.php?date='
        #http://market.finance.sina.com.cn/downxls.php?date=2017-11-01&symbol=sz002041#
        self.download_link_arr = []
        self.get_day()

    def get_stock_num(self):
        get_stock_list.create_list_file()
        rf = open('stock_list_all.log', 'rb')
        for i in rf.readlines():
            if i.split()[0][:2] == '00':
                self.stock_num.append('sz'+i[:6])
            elif i.split()[0][:2] == '60':
                self.stock_num.append('sh'+i[:6])
            else:
                pass

    def get_day(self):
        t = time.localtime()
        y = str(t.tm_year)
        m = str(t.tm_mon)
        d = str(t.tm_mday)
        if len(d) == 1:
            d = '0' + d
        self.day = '%s-%s-%s' % (y, m, d)

    def create_links(self):
        # self.get_day()
        self.get_stock_num()
        for i in self.stock_num:
            self.download_link_arr.append(self.download_link_str + self.day + '&symbol=' + i)
        with open('wait_for_download.log', 'wb') as f:
            for i in self.download_link_arr:
                f.write('%s\n' % i)

    def download_xls(self):
        self.create_links()
        subprocess.call('mkdir %s' % self.day, shell=True)
        for i in self.download_link_arr:
            filename = './%s/%s_%s.log' % (self.day, i[-8:], self.day)
            cmd1 = 'wget -O temp.xls -T 30 \"%s\"' % i
            cmd2 = 'iconv -f GBK -t UTF-8 temp.xls -o %s' % filename
            print '------------%s-------------' % i
            subprocess.call(cmd1, shell=True)
            subprocess.call(cmd2, shell=True)
            time.sleep(2)
        cmd3 = 'rm -f temp.xls'
        subprocess.call(cmd3, shell=True)

    def download_again(self, url):
        rf = open('wait_for_download.log', 'rb')
        arr1 = rf.readlines()
        arr2 = []
        flag = 0
        for i in arr1:
            if i == url:
                flag = 1
            if flag == 1:
                arr2.append(i)
        for i in arr2:
            filename = './%s/%s_%s.log' % (self.day, i[-8:], self.day)
            cmd1 = 'wget -O temp.xls -T 30 \"%s\"' % i
            cmd2 = 'iconv -f GBK -t UTF-8 temp.xls -o %s' % filename
            print '------------%s-------------' % i
            subprocess.call(cmd1, shell=True)
            subprocess.call(cmd2, shell=True)
            time.sleep(2)
        cmd3 = 'rm -f temp.xls'
        subprocess.call(cmd3, shell=True)

    def filter_xls(self):
        files = os.listdir('./%s' % self.day)
        for i in files:
            if '-' in i:
                j = './%s/%s' % (self.day,i)
                with open(j, 'r') as f:
                    if '成交时间' not in f.readline():
                        print 'remove %s' % i
                        os.remove(j)

def download_xls():
    url = input('如果中断后再次下载，请输入中断的URL，首次下载直接回车:')
    if url == '':
        m1 = get_day_trade_data()
        m1.download_xls()
        m1.filter_xls()
        print 'download xls completed!'
    else:
        m1 = get_day_trade_data()
        m1.download_again(url)
        m1.filter_xls()
        print 'download again completed!'

download_xls()
