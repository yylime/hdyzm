"""
# -*- encoding: utf-8 -*-
@Time    :   2021/12/23 12:45:18
@Author  :   yylime
@Contact :   844202100@qq.com
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
from utils import Slider

# 定义宏变量，浏览器F12后查询对应名字
TEST_URL = "http://dun.163.com/trial/sense"
# 滑动验证码分页
HD_SELECOTR = (
    "body > main > div.g-bd > div > div.g-mn2 > div.m-tcapt > ul > li:nth-child(2)"
)
TC_CLASS_SNAME = "yidun_intelli-tips"  # 点击弹出验证码
BG_CLASS_NAME = "yidun_bg-img"  # 滑块背景
HK_CLASS_NAME = "yidun_jigsaw"  # 滑块
HD_BTN = "yidun_slider"  # 滑动按钮


if __name__ == "__main__":

    # 初始化浏览器
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(
        options=options, executable_path="hdyzm-master/chromedriver/chromedriver"
    )
    wait = WebDriverWait(driver, 5)

    # 点击对应标签
    driver.get(TEST_URL)
    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, HD_SELECOTR)))
    button.click()
    button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, TC_CLASS_SNAME)))
    button.click()

    # 得到背景和滑块的item, 以及滑动按钮
    time.sleep(2)
    bg_item = wait.until(EC.presence_of_element_located((By.CLASS_NAME, BG_CLASS_NAME)))
    hk_item = wait.until(EC.presence_of_element_located((By.CLASS_NAME, HK_CLASS_NAME)))
    hd_btn = wait.until(EC.presence_of_element_located((By.CLASS_NAME, HD_BTN)))

    slider = Slider(driver, bg_item, hk_item, hd_btn)
    slider.run()

    driver.close()
