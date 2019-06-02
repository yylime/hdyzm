'''
21/3/2019
@lin
reference : https://blog.csdn.net/lmw1239225096/article/details/79099238
'''
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

def get_image():
    '''
    从网页的网站截图中，截取验证码图片
    :return: 验证码图片
    '''
    #因为图片的位置是绝对值，所以滑动一下窗口
    driver.execute_script("window.scrollTo(0,0)")
    img = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.geetest_canvas_bg.geetest_absolute')))
    time.sleep(2)  # 保证图片刷新出来
    localtion = img.location
    size = img.size
    print(localtion,size)
    left = localtion['x']+1
    top = localtion['y']
    right = localtion['x'] + size['width']
    bottom = localtion['y'] + size['height']-1
    #截图得到图片
    driver.save_screenshot('snap.png')
    page_snap_obj = Image.open('snap.png')
    #切割图片得到验证码
    crop_imag_obj = page_snap_obj.crop((left, top, right, bottom))
    # crop_imag_obj.save('crop.png')
    return crop_imag_obj

def get_dist(img,N = 10):
    '''
    :param img:
    :param N:找到N个最小的点，求x质心
    :return:
    '''
    #用来检测边缘
    scharr=np.array([[-1,0,1],
                     [-1,0,1],
                     [-1,0,1]])
    im = np.array(img.convert('RGB'))
    im = np.sum(im,axis=2)
    #得到滤波器之后的图片
    grad=signal.convolve2d(im,scharr,boundary='symm',mode='same')
    #把文字的作用去掉，所以从５０开始加
    grad = np.sum(grad[20:,:],axis = 0)
    min_to_max_indx = np.argsort(-abs(grad))
    positive = []
    for i in range(N):
        if grad[min_to_max_indx[i]]>0 and min_to_max_indx[i]>55:
            positive.append(min_to_max_indx[i])
    positive.sort()
    print(positive)

    #得到左边界
    x_left = 0
    try:
        x_left_index = [x-positive[i] for i,x in enumerate(positive[1:])].index(1)
        x_left = positive[x_left_index]
        print(x_left)
    except:
        x_left = max(positive)
        print('failed!')
    return x_left-7

def get_tracks(distance):
    '''
    拿到移动轨迹，模仿人的滑动行为，先匀加速后匀减速
    匀变速运动基本公式：
    ①v=v0+at
    ②s=v0t+½at²
    ③v²-v0²=2as
    :param distance: 需要移动的距离
    :return: 存放每0.3秒移动的距离
    '''
    # 初速度
    v = 0
    # 单位时间为0.2s来统计轨迹，轨迹即0.2内的位移
    t = 0.3
    # 位移/轨迹列表，列表内的一个元素代表0.2s的位移
    tracks = []
    # 当前的位移
    current = 0
    # 到达mid值开始减速
    mid = distance * 3 / 4
    while current < distance:
        if current < mid:
            # 加速度越小，单位时间的位移越小,模拟的轨迹就越多越详细
            a = random.randint(2,4)
        else:
            a = -random.randint(3,5)
        # 初速度
        v0 = v
        # 0.2秒时间内的位移
        s = v0 * t + 0.5 * a * (t ** 2)
        # 当前的位置
        current += s
        # 添加到轨迹列表
        tracks.append(round(s))
        # 速度已经达到v,该速度作为下次的初速度
        v = v0 + a * t
    return tracks
def huadong():
    image1 = get_image()
    # 步骤二：对比两张图片的所有RBG像素点，得到不一样像素点的x值，即要移动的距离
    distance = get_dist(image1)
    # 步骤三：模拟人的行为习惯（先匀加速拖动后匀减速拖动），把需要拖动的总距离分成一段一段小的轨迹
    tracks = get_tracks(distance)
    print(tracks)
    # print(image1.size)
    print(distance, sum(tracks))
    # 步骤四：按照轨迹拖动，完全验证
    button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_slider_button')))
    ActionChains(driver).click_and_hold(button).perform()
    for track in tracks:
        ActionChains(driver).move_by_offset(xoffset=track, yoffset=0).perform()
    else:
        ActionChains(driver).move_by_offset(xoffset=3, yoffset=0).perform()  # 先移过一点
        ActionChains(driver).move_by_offset(xoffset=-3, yoffset=0).perform()  # 再退回来，是不是更像人了
    time.sleep(0.5)  # 0.5秒后释放鼠标
    ActionChains(driver).release().perform()
    time.sleep(3)
def refresh():
    '''
    检测是否需要刷新，因为成功率太低
    :return:
    '''
    try:
        get_image()
        flag = True
        refresh = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_refresh_1')))
        refresh.click()
    except:
        flag =False
    return flag

def main():
    try:
        driver.get('https://www.geetest.com/type/')
        #　步骤零点击滑动验证
        time.sleep(1)
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#app>section>div>ul>li:nth-child(2)')))
        button.click()
        # 步骤一：先点击按钮，弹出图片
        time.sleep(2)
        button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_radar_tip')))
        button.click()
        # 滑动验证
        huadong()
    except:
        main()
    finally:
        time.sleep(2)
        #检测一下是否成功如果失败重新来一次
        flag = refresh()
        while(flag):
            huadong()
            flag = refresh()
            print('刷新一下，重新验证，不要慌')
        print('验证成功！休息5s')
        #删除保存的照片
        if os.path.exists('snap.png'):
            os.remove('snap.png')
if __name__ == '__main__':
    #定义抓取浏览器
    driver = webdriver.Chrome()
    options = webdriver.ChromeOptions()
    options.add_argument('start-maximized')
    # driver.maximize_window()
    wait = WebDriverWait(driver, 5)
    for i in range(20):
        try:
            main()
            time.sleep(5)
        # 为了做ppt的视频效果
        except:
            print('再尝试!')