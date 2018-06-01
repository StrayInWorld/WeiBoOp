# -*- coding: gbk -*-

import json
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def OpenBaiDu():
    driver = webdriver.Chrome()
    driver.get('http://www.baidu.com')
    driver.find_element_by_id("kw").send_keys("seleniumhq" + Keys.RETURN)
    driver.implicitly_wait(30)
    driver.quit()


class weiBoOpClass(object):
    def __init__(self,driver,url,findStr):
         self.driver=driver
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
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_class_name("iconf_navbar_search").click()  # 搜索按钮
        self.driver.find_element_by_class_name("forSearch").send_keys(findKeyWord + Keys.RETURN)  # 搜索文字

        commendlist = self.driver.find_elements_by_css_selector(".m-ctrl-box.m-box-center-a")
        print(len(commendlist))
        for i in range(len(commendlist)):
            print("commend=", commendlist[i])
            # 下面重新获取"转发，评论，赞" 是因为进行下面一系列操作之后，返回到主页面时，内容已经改变，所以需要重新获取
            newcommendlist = self.driver.find_elements_by_css_selector(".m-ctrl-box.m-box-center-a")
            newcommendlist[i].click()  # 外部评论
            print("已点击外部评论")
            #有1条评论以上的才需要二次点击评论
            if self.is_element_exist('// *[ @ id = "app"] / div[1] / div / div[2] / div / div / footer / div[2]'):
                self.driver.find_element_by_xpath('// *[ @ id = "app"] / div[1] / div / div[2] / div / div / footer / div[2]').click()  # 内部评论
                print("已点击内部评论")
            self.driver.find_element_by_tag_name("textarea").send_keys(r"谔谔21 " + str(i))  # 评论内容
            print("已发表评论")
            self.driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/header/div[3]/a').click()  # 发送评论
            print("已发送评论")
            #弹框处理
            if self.is_element_exist('//*[@id="app"]/div[2]/div[1]/div[2]/footer/div/a'):
                self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[1]/div[2]/footer/div/a').click()
                print("已确定")
                self.driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/header/div[1]').click()
                print("关闭")
                if self.is_element_exist('//*[@id="app"]/div[1]/div/div[1]/div/div[1]/div'):
                    self.driver.find_element_by_css_selector('#app > div:nth-child(1) > div > div.m-top-bar.m-panel.m-container-max.m-topbar-max > div > div.nav-left > div').click()
                    print("已返回")
                continue
            if self.is_element_exist('//*[@id="app"]/div[1]/div/div[1]/div/div[1]/div'):
                self.driver.find_element_by_css_selector('#app > div:nth-child(1) > div > div.m-top-bar.m-panel.m-container-max.m-topbar-max > div > div.nav-left > div').click()
                print("已返回")
        self.driver.quit()

classDriver=weiBoOpClass(webdriver.Chrome(),"https://m.weibo.cn/","范冰冰")





