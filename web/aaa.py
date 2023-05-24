#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : intyou
# @Time     : 2023/5/23 10:36
# @File     : aaa.py
# @Email    : intyou@outlook.com
# @GitHub   : https://github.com/intyouss
import random
def get_random_code():
    return ''.join(random.sample('0123456789', 6))

print(get_random_code())