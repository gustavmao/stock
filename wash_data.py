#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @version: 1.0
# @author: moses
# @file: wash_data
# @time: 11/2/17 3:00 PM

import os
import time
import pickle
# import subprocess

class my_global(object):
    moses = 1

class data_parse(object):
    def __init__(self):
        self.moses = 1
        self.paths = []
        self.day = ''
        self.stock_dict = {}

    def get_day(self):
        t = time.localtime()
        y = str(t.tm_year)
        m = str(t.tm_mon)
        d = str(t.tm_mday)
        if len(d) == 1:
            d = '0' + d
        self.day = '%s-%s-%s' % (y, m, d)

    def list_files(self):
        files = os.listdir('./%s' % self.day)
        for i in files:
            if '-' in i and 'log' in i:
                self.paths.append('./%s/%s' % (self.day, i))

    def shijian_transform(self, t): # 15:00:03
        a1 = t.strip().split(':')
        p1 = int(a1[0])
        p2 = int(a1[1])
        p3 = int(a1[2])
        before930 = 34200
        before1300 = 39600
        s = 0
        if p1 in [9,10,11]:
            s += (p1 * 3600 + p2 * 60 + p3 - before930)
        if p1 in [13,14,15]:
            s += (p1 * 3600 + p2 * 60 + p3 - before1300)
        return float(s)

    def jiage_transform(self, p):
        return float(p.strip())

    def chengjiaoliang_transform(self, v):
        return float(v.strip())

    def chengjiaoe_transform(self, v):
        return float(v.strip())

    def maimaipan_transform(self, s):
        i = 0
        if s.strip() == '卖盘':
            i -= 1
        elif s.strip() == '买盘':
            i += 1
        else:
            pass
        return float(i)

    def wash_single_file_data(self, filename):
        rf = open(filename, 'r')
        arr_line = []
        arr_file = []
        for i in rf.readlines()[1:]:
            if len(i) > 10:
                j = i.strip().split()
                print j
                arr_line.append(self.shijian_transform(j[0]))
                arr_line.append(self.jiage_transform(j[1]))
                arr_line.append(self.chengjiaoliang_transform(j[3]))
                arr_line.append(self.chengjiaoe_transform(j[4]))
                arr_line.append(self.maimaipan_transform(j[5]))
                arr_file.append(arr_line)
                arr_line = []
        return arr_file

    def wash_all_file_data(self):
        self.day = '2017-11-06' ######################################## self.get_day()
        self.list_files()
        count = 0
        for i in self.paths:
            j = i.strip()[:-4] + '.pkl'
            k = self.wash_single_file_data(i)
            with open(j, 'wb') as f:
                pickle.dump(k, f)
            count += 1
            print '%s  %s' %(i, count)

def wash_data():
    m1 = data_parse()
    m1.wash_all_file_data()
    # subprocess.call('cd ./%s && rm *.log -f' % m1.day, shell=True)

wash_data()