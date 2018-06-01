# # coding:utf-8
# from selenium import webdriver
#
# driver = webdriver.Chrome()
# driver.implicitly_wait(10)
# driver.get("http://www.baidu.com")
# def is_element_exist(css):
#     s = driver.find_elements_by_css_selector(css_selector=css)
#     if len(s) == 0:
#         print("元素未找到:%s"%css)
#         return False
#     elif len(s) == 1:
#         return True
#     else:
#         print("找到%s个元素：%s"%(len(s),css))
#         return False
#
# # 判断页面上有无id为kw的元素
# if is_element_exist(".m-btn.m-btn-white.m-btn-text-orange"):
#     driver.find_element_by_id("kw").send_keys("yoyoketang")
# # 判断页面有无标签为input元素
# if is_element_exist("input"):
#     driver.find_element_by_tag_name("input").send_keys("yoyoketang")
# # 判断页面有无id为xxx的元素
# if is_element_exist("xxx"):
#     driver.find_element_by_id("xxx").send_keys("yoyoketang")
#
# def isElementExist(css):
#     try:
#         driver.find_element_by_css_selector(css)
#         return True
#     except:
#         return False
#
# print(isElementExist("#xxx"))



