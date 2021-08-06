# python3
# -*- coding: utf-8 -*-
# @Time : 2021/8/5 14:27 
# @Author : Kate
# @File : test.py 


def debug(func):
    def wrapper(something):  # 指定一毛一样的参数
        print("[DEBUG]: enter {}()".format(func.__name__))
        return func(something)
    return wrapper  # 返回包装过函数

@debug
def say(something):
    print("hello {}!".format(something))