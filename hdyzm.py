# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 16:11:21 2019

@author: lin
"""
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from PIL import Image
import matplotlib.pylab as plt
from scipy import signal
import numpy as np
import time
import random
import os

#定义宏变量
#TEST_URL = 'https://www.geetest.com/type/'
TEST_URL = 'http://dun.163.com/trial/sense'
HD_TAG = "body > main > div.g-bd > div > div.g-mn2 > div.m-tcapt > ul > li:nth-child(2)"
TC_CLASS_SNAME = "yidun_intelli-tips"
PIC_CLASS_NAME = "yidun_bg-img"
HD_BTN = "yidun_slider"


options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
driver = webdriver.Chrome(options=options,executable_path="./chromedriver")
wait = WebDriverWait(driver,5)

driver.get(TEST_URL)
time.sleep(2)
button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,HD_TAG)))
button.click()
time.sleep(2)
button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,TC_CLASS_SNAME)))
button.click()

#得到图片
time.sleep(2)
img = wait.until(EC.presence_of_element_located((By.CLASS_NAME,PIC_CLASS_NAME)))
location = img.location
size = img.size
driver.save_screenshot('snap.png')
#得到验证码的位置
left = location['x']
top = location['y']
right = left+size['width']
bottom = top+size['height']
img_obg = Image.open('snap.png')
crop_img = img_obg.crop((left,top,right,bottom))
crop_img.save('crop.png')
#卷积操作
im = np.array(crop_img.convert('L'))
#先进行平滑处理
# 生成高斯算子的函数
def func(x,y,sigma=1):
    return 100*(1/(2*np.pi*sigma))*np.exp(-((x-2)**2+(y-2)**2)/(2.0*sigma**2))
# 生成标准差为5的5*5高斯算子
g = np.fromfunction(func,(3,3),sigma=1)

grad = signal.convolve2d(im, g, mode="same")
plt.figure()
plt.imshow(grad)
plt.show()

f = np.array([[-1,0,1],
              [-2,0,2],
              [-1,0,1],
              ])

grad = signal.convolve2d(grad,f,boundary='symm',mode='same')
plt.figure()
plt.imshow(grad)
plt.show()

#得到距离
grad = np.sum(grad[:,:],axis=0)
max_to_min = np.argsort(grad)


positive = []
i = 0
j = 0
while(j<6):
    if max_to_min[i]>55:
        positive.append(max_to_min[i])
        j = j+1
    i = i+1

x_left_index = 0 
diffs = [x-positive[i] for i,x in enumerate(positive[1:])]
for i,d in enumerate(diffs):
    if d==1 or d==-1:
        x_left_index=i
        break
x_left = positive[x_left_index]
x_left -= 0

#模拟人为滑动
v0 = random.randint(0,2)
t = 0.1
tracks = []
cur = 0
mid = x_left*0.8
while cur < x_left:
    if cur<mid:
        a = random.randint(2,4)
    else:
        a = -random.randint(3,5)
    v = v0
    s = v*t+0.5*a*t**2
    cur += s
    v0 = v+a*t
    tracks.append(round(s))

tracks.append(x_left-sum(tracks))
n_stop = [0]*random.randint(10,30)
stop = random.randint(round(len(tracks)*0.85),round(len(tracks)*0.95))
tracks = tracks[:stop]+n_stop+tracks[stop:]
#开始滑动
button = wait.until(EC.presence_of_element_located((By.CLASS_NAME,HD_BTN)))
ActionChains(driver).click_and_hold(button).perform()
for t in tracks:
    ActionChains(driver).move_by_offset(t,0).perform()

fore = random.randint(0,7)
ActionChains(driver).move_by_offset(fore,0).perform()
time.sleep(0.6)
ActionChains(driver).move_by_offset(-fore,0).perform()

time.sleep(0.5)
ActionChains(driver).release().perform()
time.sleep(3)
driver.close()




