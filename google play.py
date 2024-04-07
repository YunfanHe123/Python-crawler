# -*- coding:utf-8 -*-

import time
import os
import re
import time
import datetime
#import pymysql
#from scrapy.http import HtmlResponse, request
#from GetComments.items import GetcommentsItem
from scrapy.spiders import Spider
from selenium import webdriver
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import sqlite3
from selenium.webdriver.common.by import By
import pandas as pd
import pyautogui

# #删除文件首行
# def deleteFirstRow(file):
#     size = os.path.getsize('url.txt')
#     if size == 0:
#         print("文件删除成功")
#         return
#     try:
#         file = open('url.txt', 'r+')
#     except:
#         pass
#     l4 = file.readlines()
#     l4[0] = ''
#     file.close()
#     file = open('url.txt', 'w+')
#     l4 = file.writelines(l4)
#     file.close()
#判断阅读更多链接是否存在
# def isElementExist(driver):
#     flag = True
#     browser = driver
#     try:
#         browser.find_element_by_xpath("//span[@class='RveJvd snByac']")
#         return flag
#     except:
#         flag = False
#         return flag
#选择爬取策略 按照时间爬取
# def choosePageRule(driver):
#     try:
#         #展开下拉框
#         driver.find_element_by_xpath("//div[@class='jgvuAb Eic1df']").click()
#         #找到Newest的位置
#         ele = driver.find_element_by_xpath("//div[@class='OA0qNb ncFHed']")
#         ActionChains(driver).move_to_element_with_offset(ele, 0, 49.6).click().perform()
#     except:
#         print("默认评价策略")
#     time.sleep(2)
#     pass
#判断评论长度
# def commentLength(str):
#     str1 = str.strip()
#     index = 0
#     count = 0
#     while index < len(str1):
#         while str1[index] != " ": # 当不是空格是，下标加1
#             index += 1
#             if index == len(str1): # 当下标大小跟字符串长度一样时结束当前循环
#                 break
#         count += 1  # 遇到空格加1
#         if index == len(str1): # 当下标大小跟字符串长度一样时结束当前循环
#             break
#         while str1[index] == " ": # 当有两个空格时，下标加1，防止以一个空格算一个单词
#             index += 1
#     if(count<=5):
#         return True
#     return False
#加载页面
# def loadWebPage(driver):
#     flag = 0
#     count = 0
#     while 1:
#         count = count + 1
#         # 对于评论太多的设置爬取10000条
#         if count >= 250:
#             print("窗口滑动250次")
#             break;
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         try:
#             loadMore = driver.find_element(By.XPATH,"//*[contains(@class,'U26fgb O0WRkf oG5Srb C0oVfc n9lfJ')]").click()
#         except:
#             time.sleep(1)
#             flag = flag + 1
#             if flag >= 10:
#                 print("当前App评论全部获取")
#                 break
#         else:
#             flag = 0
#解析网页
comment_list=[]
a=0
b=0
def fetchWebPage(driver):
    #item = [[]]
    # app名称
    reviews = driver.find_elements(By.CLASS_NAME,'RHo1pe')#RHo1pe
    #pingfen = driver.find_elements(By.CLASS_NAME,'iXRFPc')
    print("There are " + str(len(reviews)) + " reviews avaliable")
    print("数据正在写入数据库")

    for review in reviews:
        #print(review.text)
        #html = driver.page_source
        try:
            xingming = review.find_element(By.CLASS_NAME,'X5PpBb').text
        except:
            xingming = 'unknown'

        try:
            score = review.find_element(By.CLASS_NAME,'iXRFPc').get_attribute('aria-label')
        except:
            score = 'unknown'

        try:
            shijian = review.find_element(By.CLASS_NAME, 'Jx4nYe').text
        except:
            shijian = 'unknown'

        try:
            comment=review.find_element(By.CLASS_NAME,'h3YV2d').text
            if not comment:
                comment = 'unknown'
        except:
            comment = 'unknown'

        c = [shijian,xingming,score,comment]

        if c in comment_list:
            continue
        else:
            comment_list.append(c)

    return comment_list

        #数据入库
        #print(review.text)
        # try:
        #     # 避免插入重复数据
        #     cursor.execute('insert into comment(comment) values(comment)')
        #     db.commit()
        # except:
        #     print("数据库插入出错")
        #     db.rollback()



class GetComment(Spider):
    #name = "comment"
    # 打开数据库
    try:
        # db = pymysql.connect(host="localhost", user="root", password=" ", db="scrapy", port=3306)
        # cursor = db.cursor()
        zufang = sqlite3.connect('评论爬虫.sqlite')
        cursor = zufang.cursor()
        print("数据库打开成功")
    except:
        print("数据库打开失败")
        print("正在退出程序")
        exit(0)
    #driver = webdriver.Chrome()
    print("正在爬取网页信息")
    # f  = open('url.txt', 'r+')
    # line = f.readline()
    # num = 1
    # while line:
    #     size = os.path.getsize('url.txt')
    #     if size == 0:
    #          break;
    #     print("爬取app数目：" + str(num))
    #     try:
    #         f = open('url.txt', 'r+')
    #     except:
    #         pass
    #     u = line
    #     deleteFirstRow(f)
    #     driver.get(u)
        #评价策略默认
        #choosePageRule(driver)
    time.sleep(2)
    driver = webdriver.Chrome()
    driver.get('https://play.google.com/store/apps/details?id=com.nixonappsstudio.bloodpressurechecker.reports&hl=en&gl=US')#&hl=en
    driver.set_page_load_timeout(30)
    driver.find_element(By.XPATH, '//span[@class="VfPpkd-vQzf8d" and text()="See all reviews"]').click()
    pyautogui.moveTo(960, 540, duration=1)
    while True:
        a=len(driver.find_elements(By.CLASS_NAME, 'RHo1pe'))
        pyautogui.scroll(-4000)
        time.sleep(4)
        pyautogui.scroll(-4000)
        time.sleep(4)
        pyautogui.scroll(-4000)
        time.sleep(4)
        pyautogui.scroll(-4000)
        time.sleep(4)
        pyautogui.scroll(-4000)
        time.sleep(4)
        pyautogui.scroll(-4000)
        time.sleep(4)
        pyautogui.scroll(-4000)
        time.sleep(4)
        pyautogui.scroll(-4000)
        time.sleep(4)
        pyautogui.scroll(-4000)
        time.sleep(4)
        pyautogui.scroll(-4000)
        time.sleep(4)
        b=len(driver.find_elements(By.CLASS_NAME, 'RHo1pe'))
        if a==b:
            break

    '''while True:
        # 滑动之前的页面高度
        document = driver.execute_script('return document.body.scrollHeight;')
        time.sleep(2)
        # 滑动页面
        driver.execute_script(f'window.scrollTo(0,{document})')
        time.sleep(2)
        # 滑动之后的页面高度
        document2 = driver.execute_script('return document.body.scrollHeight;')
        # 比较滑动前与滑动后的高度
        if document == document2:
            break'''


        # html = driver.page_source
        # driver.get_cookies()
        #driver.quit()
        #loadWebPage(driver)
        #driver.find_element(By.XPATH, "//*[contains(@class,'U26fgb O0WRkf oG5Srb C0oVfc n9lfJ')]").click()
        #js = "var q=document.body.scrollTop=10000"
        #driver.execute_script(js)
        #driver.find_element(By.XPATH, "//*[@class='U26fgb O0WRkf oG5Srb C0oVfc n9lfJ M9Bg4d']").click()

        #driver.execute_script("window.scrollTo(0, 1500);")
    fetchWebPage(driver)
    df = pd.DataFrame(comment_list,columns=['shijian','xingming','score','comment'])
    a=df.to_csv('D:/医学信息学/研究生论文撰写/高血压app/app终极数据（最新版）/用户评论数据/google play美国用户评论数据/Blood Pressure Checker Reports_Nixon Apps Studio.csv',encoding='utf_8_sig')
    #line = f.readline()
        #num = num+1
    print("程序任务结束")
    driver.close()

# zufang = sqlite3.connect('评论爬虫.sqlite')
# create_table = 'create table app (title varchar(512), money varchar(128))'
# zufang.execute(create_table)
