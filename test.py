from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random

def OpenBaiDu():
    driver = webdriver.Chrome()
    driver.get('http://www.baidu.com')
    driver.find_element_by_id("kw").send_keys("seleniumhq" + Keys.RETURN)
    driver.implicitly_wait(30)
    driver.quit()

def testRandom():
    print("randrange(1,100, 2) : ", random.randrange(1, 100, 2))

for i in range(101):
    print(random.choice((1,23,3)))