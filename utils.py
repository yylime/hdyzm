"""
# -*- encoding: utf-8 -*-
@Time    :   2021/12/23 14:37:06
@Author  :   yylime
@Contact :   844202100@qq.com
"""

import random
from selenium.webdriver import ActionChains
from PIL import Image
import numpy as np
from scipy import signal
import requests
import time
import matplotlib.pylab as plt


def download_form_url(url, path, size):
    response = requests.get(url)
    with open(path, "wb") as f:
        f.write(response.content)
    img = Image.open(path).resize(size)
    img.save(path)
    return path


def valid_test_img_show(img, distance):
    plt.figure
    plt.imshow(img)
    plt.axvline(distance)
    plt.savefig('hdyzm-master/imgs/valid.png')
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
    def __init__(
        self, driver, background_item, slider_item, slider_btn, method="defaulat"
    ) -> None:
        self.driver = driver
        self.background_item = background_item
        self.slider_item = slider_item
        self.slider_btn = slider_btn
        self.method = method
        self.offset = 8  # offset

    def _download_images(self):
        backgroud_url = self.background_item.get_attribute("src")
        slider_url = self.slider_item.get_attribute("src")
        print(backgroud_url, slider_url)
        # mark the size of background picture
        backgroud_size = (
            self.background_item.size["width"],
            self.background_item.size["height"],
        )
        slider_size = self.slider_item.size["width"], self.slider_item.size["height"]
        # download img
        download_form_url(
            backgroud_url, "hdyzm-master/imgs/background.png", backgroud_size
        )
        download_form_url(slider_url, "hdyzm-master/imgs/slider.png", slider_size)

    def get_distance_by_default(self):
        # download pictures
        self._download_images()
        # load the picture
        backgroud_img = Image.open("hdyzm-master/imgs/background.png").convert("L")
        slider_img = Image.open("hdyzm-master/imgs/slider.png").convert("L")
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
        sorted_sum = np.argsort(-cols_sum)
        distance = sorted_sum[0]
        # show the distance on background
        valid_test_img_show(backgroud_img, distance)
        return distance + self.offset  - left

    def run(self):
        distance = self.get_distance_by_default()
        tracks = get_tracks(distance)

        # 开始滑动
        ActionChains(self.driver).click_and_hold(self.slider_btn).perform()
        for t in tracks:
            ActionChains(self.driver, duration=5).move_by_offset(t, 0).perform()
        # time.sleep(0.7)
        # fore = random.randint(0, 7)
        # ActionChains(self.driver, duration=5).move_by_offset(fore, 0).perform()
        # time.sleep(0.6)
        # ActionChains(self.driver, duration=5).move_by_offset(-fore, 0).perform()
        time.sleep(0.2)
        ActionChains(self.driver, duration=5).release().perform()
        time.sleep(2)
