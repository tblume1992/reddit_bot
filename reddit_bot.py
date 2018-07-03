#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 18:40:52 2018

@author: tyler
"""
import random 
import string
import pandas as pd
import time 
from selenium import webdriver
from lxml.html import fromstring
import requests
class account_creation():
    def __init__(self, number_of_accounts = 1, password_length = 8):
        self.number_of_accounts = number_of_accounts
        self.password_length = password_length
        
    def create_usernames(self):
        user_name_list = []
        for i in range(self.number_of_accounts):
            user_name_list.append(random.randint(100000,999999))
        return user_name_list
    def create_passwords(self):
        password_list = []
        for i in range(self.number_of_accounts):
            password_list.append(''.join(random.SystemRandom().choice(string.ascii_uppercase 
                                         + string.ascii_lowercase 
                                         + string.digits) 
                                         for _ in range(self.password_length)))
        return password_list
    def account_details(self):
        details = pd.DataFrame()
        details['Usernames'] = self.create_usernames()
        details['Passwords'] = self.create_passwords()
        return details
    
    


class reddit_operations():
    def __init__(self, usernames, passwords, base_email):
        from selenium import webdriver
        self.usernames = usernames
        self.passwords = passwords
        self.base_email = base_email
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        self.options = webdriver.ChromeOptions()
        # specify headless mode
        '''
        self.options.add_argument('headless')
        '''
        # specify the desired user agent
        self.options.add_argument(f'user-agent={self.user_agent}')
        self.driver = webdriver.Chrome(chrome_options=self.options)

    def beat_captcha(self):
        import pyautogui
        time.sleep(random.randint(1,3))
        pyautogui.moveTo(120,430)  
        pyautogui.click()  
        time.sleep(2)
        '''
        self.driver.close()
        '''
    def open_reddit_register(self):
        self.driver.get('http://reddit.com/register')
        self.driver.maximize_window()
    def enter_email(self):
        time.sleep(random.randint(1,5))
        inputElement = self.driver.find_element_by_id("regEmail")
        inputElement.send_keys(str(self.usernames) + '.'  + str(self.base_email))
        time.sleep(2)
        next_button = self.driver.find_elements_by_xpath("/html/body/div/div/div[2]/div/form/div[1]/fieldset[2]/button")[0]
        next_button.click()
    def enter_username(self):
        inputElement = self.driver.find_element_by_id("regUsername")
        inputElement.send_keys(str(self.usernames))
        print(self.usernames)
    def enter_password(self):
        inputElement = self.driver.find_element_by_id("regPassword")
        inputElement.send_keys(str(self.passwords))
        print(self.passwords)           
class proxy_handling():
    def __init__(self):
       self.i = 1
    def get_proxies(self):       
        url = 'https://free-proxy-list.net/'
        response = requests.get(url)
        parser = fromstring(response.text)
        proxies = set()
        print(parser)
        for i in parser.xpath('//tbody/tr')[:1000]:
            if i.xpath('.//td[7][contains(text(),"yes")]'):
                proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                proxies.add(proxy)
        return list(proxies)
    def proxy_switching(self, proxy_list):  
        PROXY = random.choice(proxy_list)
        print(PROXY)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=%s' % PROXY)
        
 
class accountCreation():
    def __init__(self, base_email, n = 5, password_length = 8):
        self.n = n
        self.base_email = base_email
        self.password_length = password_length
        self.ac = account_creation(self.n, self.password_length)
        self.details = self.ac.account_details()
        self.proxy_lists = proxy_handling()
        self.proxy = self.proxy_lists.get_proxies()
    def createAccounts(self):
        for i in range(self.n):
            self.proxy_lists.proxy_switching(self.proxy)
            ro = reddit_operations(usernames = self.details.iloc[i,0], passwords = self.details.iloc[i,1], base_email = self.base_email)
            ro.open_reddit_register()
            time.sleep(2)
            ro.enter_email()
            ro.enter_username()
            time.sleep(2)
            ro.enter_password()
            ro.beat_captcha()
            
           


