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
            print("cookies存在，执行正常流程")
            self.doOp(findStr)
        else:
            print("cookies不存在")
            try:
                WebDriverWait(self.driver, 60, 0.5).until(EC.presence_of_element_located((By.LINK_TEXT, '发现')))
                dictCookies = self.driver.get_cookies()
                jsonCookies = json.dumps(dictCookies)
                # 登录完成后，将cookie保存到本地文件
                with open('cookies.json', 'w') as f:
                    f.write(jsonCookies)
                self.doOp(findStr)
            finally:
                self.driver.close()

    # 判断节点是否存在
    def is_element_exist(self,css):
        s = self.driver.find_elements_by_xpath(css)
        if len(s) == 0:
            print("元素未找到:%s" % css)
            return False
        elif len(s) == 1:
            print("找到了")
            return True
        else:
            print("找到%s个元素：%s" % (len(s), css))
            return False

    #处理弹框
    def handlerAlert(self):
        self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[1]/div[2]/footer/div/a').click()
        print("已确定")
        try:
            self.driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/header/div[1]').click()
            print("关闭")
        except WebDriverException:
            self.movePage(1)
            self.driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/header/div[1]').click()
            print("关闭")

        if self.is_element_exist('//*[@id="app"]/div[1]/div/div[1]/div/div[1]/div'):
            self.driver.find_element_by_css_selector(
                '#app > div:nth-child(1) > div > div.m-top-bar.m-panel.m-container-max.m-topbar-max > div > div.nav-left > div').click()
            print("已返回")

    #移动鼠标
    def movePage(self,height):
        time.sleep(2)
        if height is None:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        else:
            self.driver.execute_script("window.scrollTo(0, 50);")
        print("执行了移动鼠标")

    #发表评论
    def writeComment(self,word,num):
        self.driver.find_element_by_tag_name("textarea").send_keys(word + str(num))  # 评论内容
        print("已发表评论")
        self.driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/header/div[3]/a').click()  # 发送评论
        print("已发送评论")


    def doOp(self,findKeyWord):
        self.driver.get('https://m.weibo.cn/')

        # 删除第一次建立连接时的cookie
        self.driver.delete_all_cookies()
        # 读取登录时存储到本地的cookie
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
        # 再次访问页面，便可实现免登陆访问
        self.driver.get('https://m.weibo.cn/')
        self.driver.implicitly_wait(6)
        self.driver.find_element_by_class_name("iconf_navbar_search").click()  # 搜索按钮
        self.driver.find_element_by_class_name("forSearch").send_keys(findKeyWord + Keys.RETURN)  # 搜索文字

        commendlist = self.driver.find_elements_by_css_selector(".m-ctrl-box.m-box-center-a")
        print(len(commendlist))
        if len(commendlist)==0:
            self.movePage()
        for i in range(len(commendlist)):
            print("-----------------"+str(i)+"-----------------")
            # 下面重新获取"转发，评论，赞" 是因为进行下面一系列操作之后，返回到主页面时，内容已经改变，所以需要重新获取
            newcommendlist = self.driver.find_elements_by_css_selector(".m-ctrl-box.m-box-center-a")
            btnClick=newcommendlist[i].find_elements_by_css_selector(".m-diy-btn.m-box-col.m-box-center.m-box-center-a")[1]
            try:
               btnClick.click()  # 外部评论
            except WebDriverException:
               self.movePage(1)
               btnClick.click()

            print("已点击外部评论")
            #有1条评论以上的才需要二次点击评论
            if not self.is_element_exist('// *[ @ id = "app"] / div[1] / div / div[2] / div / div / footer / div[2]'):
                self.writeComment("嗯嗯",i)
                # 弹框处理
                if self.is_element_exist('//*[@id="app"]/div[2]/div[1]/div[2]/footer/div/a'):
                    self.handlerAlert()
                    continue
                continue
            self.driver.find_element_by_xpath('// *[ @ id = "app"] / div[1] / div / div[2] / div / div / footer / div[2]').click()  # 内部评论
            print("已点击内部评论")
            self.writeComment("嗯嗯", i)
            #弹框处理
            if self.is_element_exist('//*[@id="app"]/div[2]/div[1]/div[2]/footer/div/a'):
                self.handlerAlert()
                continue
            self.driver.find_element_by_css_selector('#app > div:nth-child(1) > div > div.m-top-bar.m-panel.m-container-max.m-topbar-max > div > div.nav-left > div').click()
            print("已返回")
        self.driver.quit()

keyWord="鹿晗"
getUrl="https://m.weibo.cn/"

while True:
    classDriver = weiBoOpClass(webdriver.Chrome())
    try:
        classDriver.startOp(getUrl, keyWord)
    except WebDriverException:
        print("没有找到位置")
    finally:
        print("出错了，重新运行了")
        classDriver.driver.quit()
        weiBoOpClass(webdriver.Chrome()).startOp(getUrl, keyWord)
