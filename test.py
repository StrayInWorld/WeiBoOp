# coding=utf-8
from selenium import webdriver
import time

# 访问百度
driver = webdriver.Chrome()
driver.get("http://www.baidu.com")

# 搜索
driver.find_element_by_id("kw").send_keys("selenium")
driver.find_element_by_id("su").click()
time.sleep(3)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
print("执行了")
time.sleep(3)

driver.quit()