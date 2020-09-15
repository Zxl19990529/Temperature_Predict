# 引入必要库
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from tqdm import tqdm
import argparse

class Day_weather:
    def __init__(self):
        self.date = None  # 日期，比如 '2020-07-01
        self.weekday = None  # 星期， 比如 星期四
        self.weather = None  # 天气，比如 多云
        self.max_temp = None  # 最高温， 纯数字
        self.min_temp = None  # 最低温， 纯数字
        self.wind_direction = None  # 风向, 西南风 2级
        self.wind_strength = None  # 风力， '2级


def make_url(city='qingdao', start_month=202007, end_month=202008):
    url_list = []
    base_url = 'http://lishi.tianqi.com/%s/%d.html'  # 基础url
    for month in range(start_month, end_month+1):  # 循环得到各个年月历史天气的url
        url = base_url % (city, month)
        url_list.append(url)
    return url_list


def get_data(city='qingdao', start_month=202001, end_month=202008):
    all_data = []
    url_list = make_url(city, start_month, end_month)
    header = {# 伪装成浏览器
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
         AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 \
        Safari/537.36'}
    print('scratching from %d to %d' % (start_month, end_month))
    pbar = tqdm(url_list) # 设置进度条
    for url in url_list:
        pbar.update(1) # 更新进度条
        html = requests.get(url=url, headers=header)
        soup = BeautifulSoup(html.text, 'html.parser') # 解析html文本
        ul = soup.find_all("ul", class_='thrui')[0]
        tmp = ul.find_all("li")
        lis = tmp[:]
        for li in lis:
            day_wea = Day_weather()# 创建天气对象
            div = li.find_all('div')
            day_wea.date = '\'' + div[0].text.split(' ')[0]# 日期数据
            day_wea.weekday = div[0].text.split(' ')[1]# 星期
            day_wea.max_temp = div[1].text.split('℃')[0]# 最高温
            day_wea.min_temp = div[2].text.split('℃')[0]# 最低温
            day_wea.weather = div[3].text# 天气状况 
            day_wea.wind_direction = div[4].text.split(' ')[0]# 风向
            day_wea.wind_strength = '\'' + \
                div[4].text.split(' ')[1].split('级')[0]# 风力
            all_data.append(day_wea)
    return all_data

parser = argparse.ArgumentParser()
parser.add_argument('--start_year',default=2011,type=int,help='输入要爬取的起始年份')
parser.add_argument('--end_year',default=2019,type=int,help='输入要爬取的结束年份')
args = parser.parse_args()

if __name__ == '__main__':
    start_year = args.start_year
    end_year = args.end_year
    all_data = []
    for year in range(start_year, end_year+1):# 爬取从2011年到2019年的所有数据
        year_data = get_data('qingdao', start_month=int(
            str(year)+'01'), end_month=int(str(year)+'12'))
        all_data += year_data
    output_name = '%d_%d.csv' % (start_year, end_year)
    f = open(output_name, 'w')
    f.writelines('日期,星期,天气,最高温(℃),最低温(℃),风向,风力（级别）\n')
    for day_weather in all_data:
        context = ','.join([day_weather.date, day_weather.weekday, day_weather.weather, day_weather.max_temp,
                            day_weather.min_temp, day_weather.wind_direction, day_weather.wind_strength])+'\n'
        f.writelines(context)
    f.close()
