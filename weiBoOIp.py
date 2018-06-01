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


# ��¼cookie
def recordCookie():
    driver = webdriver.Chrome()
    driver.get('https://m.weibo.cn/')
    # ��ȡcookie��ͨ��jsonģ�齫dictת����str
    driver.implicitly_wait(30)
    dictCookies = driver.get_cookies()
    jsonCookies = json.dumps(dictCookies)
    # ��¼��ɺ󣬽�cookie���浽�����ļ�
    with open('cookies.json', 'w') as f:
        f.write(jsonCookies)

    driver.quit()

# recordCookie()
#Login1("������ʦ��")

class weiBoOpClass(object):
    def __init__(self,driver,url):
         self.driver=driver
         self.driver.get(url)
         self.driver.implicitly_wait(10)
         self.isHaveCookiesFile()

    def isHaveCookiesFile(self):
        if os.path.isfile("cookies.json"):
            print("cookies���ڣ�ִ����������")
            self.doOp("������ʦ��")
        else:
            print("cookies������")
            try:
                WebDriverWait(self.driver, 20, 0.5).until(EC.presence_of_element_located((By.LINK_TEXT, '����')))
                dictCookies = self.driver.get_cookies()
                jsonCookies = json.dumps(dictCookies)
                # ��¼��ɺ󣬽�cookie���浽�����ļ�
                with open('cookies.json', 'w') as f:
                    f.write(jsonCookies)
                self.doOp("������ʦ��")
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
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_class_name("iconf_navbar_search").click()  # ������ť
        self.driver.find_element_by_class_name("forSearch").send_keys(findKeyWord + Keys.RETURN)  # ��������

        commendlist = self.driver.find_elements_by_css_selector(".m-ctrl-box.m-box-center-a")
        print(len(commendlist))
        for i in range(len(commendlist)):
            print("commend=", commendlist[i])
            # �������»�ȡ"ת�������ۣ���" ����Ϊ��������һϵ�в���֮�󣬷��ص���ҳ��ʱ�������Ѿ��ı䣬������Ҫ���»�ȡ
            newcommendlist = self.driver.find_elements_by_css_selector(".m-ctrl-box.m-box-center-a")
            newcommendlist[i].click()  # �ⲿ����
            print("�ѵ���ⲿ����")
            self.driver.find_element_by_xpath(
                '// *[ @ id = "app"] / div[1] / div / div[2] / div / div / footer / div[2]').click()  # �ڲ�����
            print("�ѵ���ڲ�����")
            self.driver.find_element_by_tag_name("textarea").send_keys(r"���� " + str(i))  # ��������
            print("�ѷ�������")
            self.driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/header/div[3]/a').click()  # ��������
            print("�ѷ�������")
            # btnAlert = driver.find_element_by_css_selector(css_selector=".m-btn.m-btn-white.m-btn-text-orange")
            # if len(btnAlert) == 1:
            #     driver.find_element_by_css_selector(".m-btn.m-btn-white.m-btn-text-orange").click()
            #     print("�е���")
            #     driver.find_element_by_css_selector(".m-box.m-flex-grow1.m-alnf-sth.m-aln-center.m-flex-base0").click()
            #     print("�ѹر�")
            #     break
            self.driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/div[1]/div/div[1]/div').click()
            print("�ѷ���")
        self.driver.quit()

classDriver=weiBoOpClass(webdriver.Chrome(),"https://m.weibo.cn/")





