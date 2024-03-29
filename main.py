"""
# -*- encoding: utf-8 -*-
@Time    :   2021/12/23 12:45:18
@Author  :   yylime
@Contact :   844202100@qq.com
"""

from utils import Slider
from setting import Config
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--name",
    default="jiyan",
    type=str,
    help="find useful name in setting.py",
)
args = parser.parse_args()

if __name__ == "__main__":

    cfg = Config(args.name)
    slider = Slider(cfg)
    slider.run()
