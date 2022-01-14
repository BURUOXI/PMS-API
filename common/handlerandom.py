#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/12/14 20:22
# @File : test_shop.py
# @Project : PMS-API

import random
from faker import Factory
from faker import Faker
import radar
import datetime
import uuid
import time
import time

fake = Factory().create()
fake_cn = Faker("zh_CN")
fa = Faker(locale='zh_CN')

def credit_card_number():
    """生成银行卡账户 """

    return fa.credit_card_number()

def chinese_name():
    """生成中文名字"""
    return fake_cn.name()



def generate_uuid():
    """生成uuie"""
    return uuid.uuid1()


def date_now():
    """生成当前时间"""
    return datetime.datetime.now()
# .strftime('%Y-%m-%d %H:%M:%S')  格式化放在调用出

def start_data():
    now_data = datetime.datetime.now().strftime('%Y-%m-%d')
    five_data = (datetime.datetime.now() + datetime.timedelta(days=5)).strftime('%Y-%m-%d')
    # print(now_data,five_data )
    return now_data, five_data

start_data()


def date_now_sleep_stamp():
    # print(str(datetime_stamp2[1:10]))
    time.sleep(0.1)
    t = time.time()
    millis = int(round(t * 1000))
    print(millis)
    return millis


def date_now_stamp():
    # print(str(datetime_stamp2[1:10]))
    t = time.time()
    millis = int(round(t * 1000))
    print(millis)
    return millis


def date_pasttime_one_hour():
    return (datetime.datetime.now() - datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')


def random_datetime_2019():
    return str(radar.random_datetime(start='2019-01-01T00:00:00', stop='2019-08-01T23:59:59', parse=radar.utils.parse))


def random_datetime_2018():
    return str(radar.random_datetime(start='2018-01-01T00:00:00', stop='2018-12-30T23:59:59', parse=radar.utils.parse))


def ramdom_cn_name():
    return fake_cn.name()


def random_cn_phone_number():
    return fake_cn.phone_number()


def random_phone_number():
    # 随机手机号"""
    return fake_cn.phone_number()


def random_name():
    # 随机英文姓名#
    return fake.name()


def random_address():
    # 随机地址"""
    return fake.address()


def random_country():
    # 随机国家"""
    return fake.country()


def random_city():
    # 随机城市
    return fake.city()


def random_country_code():
    # 随机国家邮编
    return fake.country_code()


def random_email():
    # 随机email
    return fake.email()


def random_state():
    # 随机省份
    return fake.state()


def random_date():
    # 随机日期
    return fake.date()


def random_text():
    # 随机生成文章(用于生成sku描述）
    return fake.text()


def random_words():
    # 随机生成单个词语（用于标题）
    return fake.word()


def random_date():
    # 随机生成日期(年、月、日）
    return fake.date()


def random_paragraph():
    # 随机生成段落
    return fake.paragraph()


def random_color_name():
    # 随机颜色名
    return fake.color_name()


def random_uri():
    # 随机生成URL
    return fake.uri()


def random_company():
    # 随机生成公司名
    return fake_cn.company()


def random_str(min_chars=0, max_chars=8):
    # 长度在最大值与最小值之间的随机字符串"""
    return fake.pystr(min_chars=min_chars, max_chars=max_chars)  # 新增的


def random_pyint():
    # 随机整数
    return fake.pyint()


def set_random_pyint(min, max):
    # 随机整数
    return fake.pyint(min, max)


def set_random_uppercase_letter():
    return fake.random_uppercase_letter()


def random_pyfloat(left_digits=2, right_digits=2, positive=True):
    # 生成正的小数（left_digits整数位数，right_digits小数位数）
    return fake.pyfloat(left_digits=2, right_digits=2, positive=True)


def random_iso8601(tzinfo=None, end_datetime=None):
    # 生成年月日时分秒
    return fake.iso8601(tzinfo=None, end_datetime=None)


def randon_str(min_chars=0, max_char=20):
    # 随机自定义长度字符串（随便定义长度）
    return fake.pystr(min_chars=None, max_chars=20)  # NEW


def factory_generate_ids(starting_id=1, increment=1):
    # 返回一个生成器函数，调用这个函数产生生成器，从starting_id开始，步长为increment。
    def generate_started_ids():
        val = starting_id
        local_increment = increment
        while True:
            yield val
            val += local_increment

    return generate_started_ids


def factory_choice_generator(values):
    """ 返回一个生成器函数，调用这个函数产生生成器，从给定的list中随机取一项。 """

    def choice_generator():
        my_list = list(values)
        rand = random.Random()
        while True:
            yield random.choice(my_list)

    return choice_generator


# if __name__ == '__main__':
#     print(credit_card_number())
#     print(chinese_name())
    # print(random_phone_number())
    # print(random_name())
    # print(random_address())
    # print(random_country())
    # print(random_city())
    # print(random_country_code())
    # print(random_email())
    # print(random_state())
    # print(random_date())
    # print(random_text())
    # print(random_words())
    # print(random_date())
    # print(random_paragraph())
    # print(random_uri())
    # print(random_company())
    # print(random_str(min_chars=6, max_chars=8))
    # print(random_pyint())
    # print(random_pyfloat(left_digits=2, right_digits=2, positive=True))
    # print(random_iso8601(tzinfo=None, end_datetime=None))
    # print(random_str(min_chars=0, max_chars=20))
    # id_gen = factory_generate_ids(starting_id=0, increment=2)()
    # for i in range(5):
    #     print(next(id_gen))
    #
    # choices = ['John', 'Sam', 'Lily', 'Rose']
    # choice_gen = factory_choice_generator(choices)()
    # for i in range(5):
    #     print(next(choice_gen))