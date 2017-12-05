#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @version: 1.0
# @author: moses
# @file: selenium_handle
# @time: 11/3/17 9:50 AM
# 此脚本暂时不用
# 在交易时间自动刷新会导致selenium报错，暂时无法解决这个问题
# 改变这种逐页访问得到股票代号的方式，直接根据在新浪下载的文件内容筛选

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time

def get_stock_list():
    driver = webdriver.Firefox()
    driver.get("http://quote.eastmoney.com/center/list.html#33")
    time.sleep(10)
    wf = open('stock_list_range.log', 'wb')

    while True:
        elem4 = driver.find_elements_by_xpath('//*[@id="fixed"]/tbody/tr')
        num = len(elem4) - 1

        for j in range(2, 2 + num):
            elem1 = driver.find_element_by_xpath('//*[@id="fixed"]/tbody/tr[%s]/td[2]/a' % j)
            elem2 = driver.find_element_by_xpath('//*[@id="fixed"]/tbody/tr[%s]/td[3]/a' % j)
            wf.write('%s\t%s' % (elem1.text.encode('utf-8'), elem2.text.encode('utf-8')))
            # print (j - 1), elem1.text, type(elem2.text.encode('utf-8'))

        elem3 = driver.find_element_by_xpath('//*[@id="pagenav"]/a[last()]')
        if elem3.text == u"下一页":
            driver.execute_script("arguments[0].scrollIntoView();", elem3)
            # ActionChains(driver).move_to_element(elem3).perform()
            ActionChains(driver).click(elem3).perform()
            time.sleep(2)
        else:
            break
    wf.close()
    driver.close()

# get_stock_list()