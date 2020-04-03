from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest
from selenium.webdriver.common.action_chains import ActionChains


class ShopPlan:
    def __init__(self,url):
        options = webdriver.ChromeOptions()
        options.add_argument('lang=zh_CN.UTF-8')
        options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
        self.driver=webdriver.Chrome(chrome_options=options)
        self.url=url
    def login(self):

        driver=self.driver
        driver.get(self.url)
        # size
        span_background =driver.find_element_by_xpath('//*[@id="wrap"]/div[2]/div[1]/div[2]/div[1]/form/div[5]')
        hua_size=span_background.size
        print(hua_size)
        huadong=driver.find_element_by_xpath('//*[@id="nc_3_n1z"]')
        huadong_local=huadong.location
        print(huadong_local)
        
        # 拖動操作
        x_local=huadong_local['x']+hua_size['width']
        y_local=huadong_local['y']
        ActionChains(driver).click_and_hold(huadong)
        print("hold")
        time.sleep(1)
        print("huadong")
        ActionChains(driver).drag_and_drop_by_offset(
            huadong, x_local, y_local).perform()
        
        print("success")
      
        time.sleep(50)

if __name__ == "__main__":
    ShopPlan("https://login.zhipin.com/?ka=header-login").login()