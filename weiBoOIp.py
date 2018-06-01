# -*- coding: gbk -*-

import json
import os
import time

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def OpenBaiDu():
    driver = webdriver.Chrome()
    driver.get('http://www.baidu.com')
    driver.find_element_by_id("kw").send_keys("seleniumhq" + Keys.RETURN)
    driver.implicitly_wait(30)
    driver.quit()


class weiBoOpClass(object):
    def __init__(self,driver):
         self.driver=driver

    def startOp(self,url,findStr):
        self.driver.get(url)
        self.driver.implicitly_wait(6)
        self.isHaveCookiesFile(findStr)

    def isHaveCookiesFile(self,findStr):
        if os.path.isfile("cookies.json"):
            print("cookies���ڣ�ִ����������")
            self.doOp(findStr)
        else:
            print("cookies������")
            try:
                WebDriverWait(self.driver, 60, 0.5).until(EC.presence_of_element_located((By.LINK_TEXT, '����')))
                dictCookies = self.driver.get_cookies()
                jsonCookies = json.dumps(dictCookies)
                # ��¼��ɺ󣬽�cookie���浽�����ļ�
                with open('cookies.json', 'w') as f:
                    f.write(jsonCookies)
                self.doOp(findStr)
            finally:
                self.driver.close()

    # �жϽڵ��Ƿ����
    def is_element_exist(self,css):
        s = self.driver.find_elements_by_xpath(css)
        if len(s) == 0:
            print("Ԫ��δ�ҵ�:%s" % css)
            return False
        elif len(s) == 1:
            print("�ҵ���")
            return True
        else:
            print("�ҵ�%s��Ԫ�أ�%s" % (len(s), css))
            return False

    #������
    def handlerAlert(self):
        self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[1]/div[2]/footer/div/a').click()
        print("��ȷ��")
        try:
            self.driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/header/div[1]').click()
            print("�ر�")
        except WebDriverException:
            self.movePage(1)
            self.driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/header/div[1]').click()
            print("�ر�")

        if self.is_element_exist('//*[@id="app"]/div[1]/div/div[1]/div/div[1]/div'):
            self.driver.find_element_by_css_selector(
                '#app > div:nth-child(1) > div > div.m-top-bar.m-panel.m-container-max.m-topbar-max > div > div.nav-left > div').click()
            print("�ѷ���")

    #�ƶ����
    def movePage(self,height):
        time.sleep(2)
        if height is None:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        else:
            self.driver.execute_script("window.scrollTo(0, 50);")
        print("ִ�����ƶ����")

    #��������
    def writeComment(self,word,num):
        self.driver.find_element_by_tag_name("textarea").send_keys(word + str(num))  # ��������
        print("�ѷ�������")
        self.driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/header/div[3]/a').click()  # ��������
        print("�ѷ�������")


    def doOp(self,findKeyWord):
        self.driver.get('https://m.weibo.cn/')

        # ɾ����һ�ν�������ʱ��cookie
        self.driver.delete_all_cookies()
        # ��ȡ��¼ʱ�洢�����ص�cookie
        with open('cookies.json', 'r', encoding='utf-8') as f:
            listCookies = json.loads(f.read())
        for cookie in listCookies:
            self.driver.add_cookie({
                'domain': '.weibo.cn',
                'name': cookie['name'],
                'value': cookie['value'],
                'path': '/',
                'expiry': None
            })
        # �ٴη���ҳ�棬���ʵ�����½����
        self.driver.get('https://m.weibo.cn/')
        self.driver.implicitly_wait(6)
        self.driver.find_element_by_class_name("iconf_navbar_search").click()  # ������ť
        self.driver.find_element_by_class_name("forSearch").send_keys(findKeyWord + Keys.RETURN)  # ��������

        commendlist = self.driver.find_elements_by_css_selector(".m-ctrl-box.m-box-center-a")
        print(len(commendlist))
        if len(commendlist)==0:
            self.movePage()
        for i in range(len(commendlist)):
            print("-----------------"+str(i)+"-----------------")
            # �������»�ȡ"ת�������ۣ���" ����Ϊ��������һϵ�в���֮�󣬷��ص���ҳ��ʱ�������Ѿ��ı䣬������Ҫ���»�ȡ
            newcommendlist = self.driver.find_elements_by_css_selector(".m-ctrl-box.m-box-center-a")
            btnClick=newcommendlist[i].find_elements_by_css_selector(".m-diy-btn.m-box-col.m-box-center.m-box-center-a")[1]
            try:
               btnClick.click()  # �ⲿ����
            except WebDriverException:
               self.movePage(1)
               btnClick.click()

            print("�ѵ���ⲿ����")
            #��1���������ϵĲ���Ҫ���ε������
            if not self.is_element_exist('// *[ @ id = "app"] / div[1] / div / div[2] / div / div / footer / div[2]'):
                self.writeComment("����",i)
                # ������
                if self.is_element_exist('//*[@id="app"]/div[2]/div[1]/div[2]/footer/div/a'):
                    self.handlerAlert()
                    continue
                continue
            self.driver.find_element_by_xpath('// *[ @ id = "app"] / div[1] / div / div[2] / div / div / footer / div[2]').click()  # �ڲ�����
            print("�ѵ���ڲ�����")
            self.writeComment("����", i)
            #������
            if self.is_element_exist('//*[@id="app"]/div[2]/div[1]/div[2]/footer/div/a'):
                self.handlerAlert()
                continue
            self.driver.find_element_by_css_selector('#app > div:nth-child(1) > div > div.m-top-bar.m-panel.m-container-max.m-topbar-max > div > div.nav-left > div').click()
            print("�ѷ���")
        self.driver.quit()

keyWord="¹��"
getUrl="https://m.weibo.cn/"

while True:
    classDriver = weiBoOpClass(webdriver.Chrome())
    try:
        classDriver.startOp(getUrl, keyWord)
    except WebDriverException:
        print("û���ҵ�λ��")
    finally:
        print("�����ˣ�����������")
        classDriver.driver.quit()
        weiBoOpClass(webdriver.Chrome()).startOp(getUrl, keyWord)
