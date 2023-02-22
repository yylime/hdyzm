"""
# -*- encoding: utf-8 -*-
@Time    :   2021/12/23 14:37:06
@Author  :   yylime
@Contact :   844202100@qq.com
"""

import random
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from PIL import Image
import numpy as np
from scipy import signal
import requests
import time
import matplotlib.pylab as plt
import base64


def valid_test_img_show(img, distance):
    plt.figure
    plt.imshow(img)
    plt.axvline(distance, color="r")
    plt.savefig("imgs/valid.png")
    # plt.show()


def get_boundary(array):
    grad = np.array(array > 0)
    h, w = grad.shape
    # img_show(grad)
    rows_sum = np.sum(grad, axis=1)
    cols_sum = np.sum(grad, axis=0)
    left, top, bottom = 0, 0, h
    # get the top index
    p = np.max(rows_sum) * 0.5
    for i in range(h):
        if rows_sum[i] > p:
            top = i
            break
    for i in range(h - 1, -1, -1):
        if rows_sum[i] > p:
            bottom = i
            break
    p = np.max(cols_sum) * 0.5
    for i in range(w):
        if cols_sum[i] > p:
            left = i
            break
    return top, bottom + 1, left


def get_tracks(distance):
    v = random.randint(0, 2)
    t = 0.1
    tracks = []
    cur = 0
    mid = distance * 0.8
    while cur < distance:
        if cur < mid:
            a = random.randint(2, 4)
        else:
            a = -random.randint(3, 5)
        s = v * t + 0.5 * a * t ** 2
        cur += s
        v = v + a * t
        tracks.append(round(s))
    tracks.append(distance - sum(tracks))
    return tracks


class Slider:
    def __init__(self, cfg) -> None:

        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)

        self.driver = webdriver.Chrome(
            options=options, executable_path=cfg.executable_path
        )
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
        })
        # prepare to do
        self._prepare(cfg)


    def _prepare(self, cfg):
        # 初始化浏览器
        wait = WebDriverWait(self.driver, 5)
        # 点击对应标签
        self.driver.get(cfg.TEST_URL)
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cfg.HD_SELECOTR)))
        button.click()
        self.tc_item = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cfg.TC_SELECOTR)))
        self.tc_item.click()

        # 得到背景和滑块的item, 以及滑动按钮
        time.sleep(2)
        self.background_item = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, cfg.BG_SELECOTR))
        )
        self.slider_item = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, cfg.HK_SELECOTR))
        )
        self.slider_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, cfg.HD_BTN)))

        self.offset = cfg.offset
        self.background_path = cfg.background_path
        self.slider_path = cfg.slider_path



    def _download_img(self, selenium_item, path, size):
        url = selenium_item.get_attribute("src")
        if url is not None:
            response = requests.get(url)
            with open(path, "wb") as f:
                f.write(response.content)
            img = Image.open(path).resize(size)
            img.save(path)
        # use js to download picture
        else:
            class_name = selenium_item.get_attribute("class")
            # 下面的js代码根据canvas文档说明而来
            js_cmd = (
                'return document.getElementsByClassName("%s")[0].toDataURL("image/png");'
                % class_name
            )
            # 执行 JS 代码并拿到图片 base64 数据
            im_info = self.driver.execute_script(js_cmd)  # 执行js文件得到带图片信息的图片数据
            im_base64 = im_info.split(",")[1]  # 拿到base64编码的图片信息
            im_bytes = base64.b64decode(im_base64)  # 转为bytes类型
            with open(path, "wb") as f:  # 保存图片到本地
                f.write(im_bytes)
            img = Image.open(path).resize(size)
            img.save(path)

    def _download_images(self):
        # mark the size of background picture
        backgroud_size = (
            self.background_item.size["width"],
            self.background_item.size["height"],
        )
        slider_size = self.slider_item.size["width"], self.slider_item.size["height"]
        # download img
        self._download_img(self.background_item, self.background_path, backgroud_size)
        self._download_img(self.slider_item, self.slider_path, slider_size)

    def get_distance_by_default(self):
        # download pictures
        self._download_images()
        # load the picture
        backgroud_img = Image.open(self.background_path).convert("L")
        slider_img = Image.open(self.slider_path).convert("L")
        backgroud_img = np.array(backgroud_img)
        slider_img = np.array(slider_img)
        # covld
        top, bottom, left = get_boundary(slider_img)
        scharr = np.array([[-3, 0, +3], [-3, 0, +3], [-3, 0, +3]])
        grad = signal.correlate2d(
            backgroud_img[top:bottom, :], scharr, boundary="symm", mode="same"
        )
        # 得到距离
        cols_sum = np.sum(grad, axis=0)
        # desc
        sorted_sum = np.argsort(-np.abs(cols_sum))
        distance = np.min(sorted_sum[:4])
        # show the distance on background
        # valid_test_img_show(backgroud_img, distance)
        return distance + self.offset - left

    def run(self):
        fore = random.randint(0, 15)
        distance = self.get_distance_by_default()
        tracks = get_tracks(distance + fore)

        # 开始滑动
        ActionChains(self.driver).click_and_hold(self.slider_btn).perform()
        time.sleep(random.randint(0, 10) * 0.1)
        for t in tracks:
            ActionChains(self.driver, duration=5).move_by_offset(t, 0).perform()
        time.sleep(random.randint(0, 10) * 0.1)

        # 反拉
        tracks = get_tracks(fore)
        for t in tracks:
            ActionChains(self.driver).move_by_offset(-t, 0).perform()

        time.sleep(random.randint(0, 10) * 0.1)
        ActionChains(self.driver).release().perform()

        time.sleep(2)
        self.driver.close()
