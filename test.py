from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get(r'G:\weiboOp\test.html')

# # 1.串联寻找
# print(driver.find_element_by_id('B').find_element_by_tag_name('div').text)
#
# # 2.xpath父子关系寻找
# print(driver.find_element_by_xpath("//div[@id='B']/div").text)
#
# # 3.css selector父子关系寻找
# print(driver.find_element_by_css_selector('div#B>div').text)
#
# # 4.css selector nth-child
#print(driver.find_element_by_css_selector('div#B div:nth-child(1)').text)
#
# # 5.css selector nth-of-type
# print(driver.find_element_by_css_selector('div#B div:nth-of-type(1)').text)
#
# # 6.xpath轴 child
# print(driver.find_element_by_xpath("//div[@id='B']/child::div").text)

# test
#print(driver.find_element_by_css_selector('div#B:nth-child(2)').text)
print(driver.find_element_by_css_selector('div#B div').text)
print(driver.find_element_by_css_selector('div#B>div:nth-child(2)').text)
driver.quit()

