# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 13:28:59 2019

@author: anjali.dharmik
"""
from selenium import webdriver

import selenium
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re,json
import pandas as pd
import os
from pandas.io.json import json_normalize
import time,sys
import re


#url = "https://twitter.com/hashtag/ccchealth?vertical=default"#"https://twitter.com/narendramodi"
#url = "https://twitter.com/twitteruk?lang=en"

def twitter_wrapper(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("user-agent=ua.chrome()")
    browser = webdriver.Chrome(chrome_options=chrome_options,\
    executable_path="E:/Projects_04Feb2019/Twitter_PoC/Pocs/driver/chromedriver_win32/chromedriver")
    browser.get(url)
    
    
    #scrolling down...
    pause = 3
    
    lastHeight = browser.execute_script("return document.body.scrollHeight")
    #print(lastHeight)
    
    count = 1
    sub_url_lst =[]
    div_data_lst =[]#set()
    i = 0
    source =""
    
    
    
    browser.get_screenshot_as_file("test03_1_"+str(i)+".jpg")
    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause)
        newHeight = browser.execute_script("return document.body.scrollHeight")
        #print(newHeight)
        if newHeight == lastHeight:
            break
        lastHeight = newHeight
        i += 1
    
        #extract JSON from web pages...
        source = BeautifulSoup(browser.page_source)
        
        for st in source.findAll('div'):
            try:
                
                if "content" in st["class"]:
                    sub_url_lst.append(st)
            except:
                pass
        
        for d in sub_url_lst:
            name,post,_datetime =[],'',''
            for d1 in d.findAll('strong'):
                name.append(d1.get_text())
                
            for d2 in d.findAll('p'):
                post = d2.get_text()
            for d3 in d.findAll('small'):
                for d4 in d3.findAll('a'):
                    _datetime = d4["title"]
            
            _name =name[0]
            if _datetime !='' and post !="":
                div_data_lst.append([_name,_datetime,post])
    
    browser.quit()
    df = pd.DataFrame(div_data_lst,columns=['name','datetime','post'])
    df.drop_duplicates(['post'],keep='first')
    df.to_csv("twitter_post.csv",index=False)
    return df