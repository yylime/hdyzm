
class Config:
    def __init__(self, name) -> None:
        
        # general config
        self.background_path = "imgs/background.png"
        self.slider_path = "imgs/slider.png"
        self.executable_path = "chromedriver/chromedriver"
        
        if name == 'yidun':
            # test url
            self.TEST_URL = "http://dun.163.com/trial/sense"
            # 滑动验证码分页
            self.HD_SELECOTR = (
                "body > main > div.g-bd > div > div.g-mn2 > div.m-tcapt > ul > li:nth-child(2)"
            )
            self.TC_SELECOTR = ".yidun_intelli-tips"  # 点击弹出验证码
            self.BG_SELECOTR = ".yidun_bg-img"  # 滑块背景
            self.HK_SELECOTR = ".yidun_jigsaw"  # 滑块
            self.HD_BTN = ".yidun_slider"  # 滑动按钮

            self.offset = -8

        elif name == 'jiyan':
            self.TEST_URL = "https://www.geetest.com/en/demo"
            self.HD_SELECOTR = '.tab-item-1'
            self.TC_SELECOTR = ".geetest_radar_tip"
            self.BG_SELECOTR = ".geetest_canvas_bg"
            self.HK_SELECOTR = ".geetest_canvas_slice"
            self.HD_BTN = ".geetest_slider_button"
            self.offset = 0
