# 验证码识别
1. selenium实现滑动验证码识别
   - 测试[网易易盾](!http://dun.163.com/trial/sense)通过（2021年12月27日）

### 实际效果

1. 运行录制

![screen_record](imgs/screen_record.gif)



2. 距离计算可视化

![距离结果可视化](imgs/valid.png)

### 环境

```python
# env
ubuntu-18.04 + vscode + python-3.7(miniconda)+ chrome(96.0.4664.110)
```
### 使用前

1. 配置python环境（建议[miniconda](https://docs.conda.io/en/latest/miniconda.html)），然后安装如下依赖

```python
# requirements
selenium==4.0.0
pillow
numpy
scipy
matplotlib
```

2. 下载对应版本的chromedriver到chromedriver目录下（如果使用windows注意修改 *yi_dun.test* 中对应的路径）[官方地址](https://chromedriver.chromium.org/downloads)     [镜像地址](https://npm.taobao.org/mirrors/chromedriver/)

### 运行

1. 滑动验证码测试

   - 网易易盾

   ```python
   python yidun_test.py
   ```



### 常见问题

1. 滑动验证码如果出现滑动不流畅，请参考 https://blog.csdn.net/qq_36250766/article/details/100541705