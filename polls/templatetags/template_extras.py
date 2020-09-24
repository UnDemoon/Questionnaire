# -*- coding: utf-8 -*-
from django import template
#时间模块
import time
#正则模块
import re  
register = template.Library()  

#时间戳转日期过滤器
@register.filter
def timestamp_filter(value):
    timeStamp = int(value)
    return time.strftime('%Y-%m-%d %X', time.localtime(timeStamp))

#减法过滤器
@register.filter
def subtract_filter(value, num):
    value = int(value)
    num = int(num)
    return value-num

# 访问页字典取值
@register.filter
def viist_dictget_filter(ary, key):
    key = "text_name_" + str(key)
    return ary.get(key, None)

# manage页字典取值
@register.filter
def dictget_filter(ary, key):
    return ary.get(key, None) 

# manage页字典取值
@register.filter
def keys_make_filter(key_1, key_2):
    key = "radio_"+str(key_1)+"_"+str(key_2)
    return key