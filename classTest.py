import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("http://www.python.org")
        self.assertIn("Python", driver.title)
        elem = driver.find_element_by_name("q")
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()

#���������Ǽ̳��� unittest.TestCase �࣬�̳�������������һ�������ࡣ
# setUp�����ǳ�ʼ���ķ����������������ÿ�����������Զ����á�
# ÿһ�����Է����������й淶�������� test ��ͷ�����Զ�ִ�С�
# ���� tearDown ��������ÿһ�����Է�������֮����á����൱����������������
# �����������д���� close �������㻹����д quit ���������� close �����൱�ڹر������ TAB ѡ���Ȼ�� quit ���˳��������������
# ����ֻ������һ�� TAB ѡ���ʱ�򣬹رյ�ʱ��Ҳ�Ὣ����������رա�


