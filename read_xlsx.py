from openpyxl import load_workbook
from matplotlib import pyplot as plt
import numpy as np 
from sklearn.linear_model import LinearRegression
import argparse

leap_year = {# 闰年
    1:31,
    2:29,
    3:31,
    4:30,
    5:31,
    6:30,
    7:31,
    8:31,
    9:30,
    10:31,
    11:30,
    12:31
}

normal_year = { # 非闰年
    1:31,
    2:28,
    3:31,
    4:30,
    5:31,
    6:30,
    7:31,
    8:31,
    9:30,
    10:31,
    11:30,
    12:31
}

color_dict = {
    2011:'#BC8F8F',
    2012:'r',
    2013:'#D2691E',
    2014:'#FF8C00',
    2015:'#FFD700',
    2016:'#556B2F',
    2017:'#00FFFF',
    2018:'b',
    2019:'#9400D3'
}
def get_date_num(year,month,day):
    date_num = 0
    year_dict = None

    if year%4 == 0:
        year_dict = leap_year
    else:
        year_dict = normal_year
    for month_i in range(0,month):
        if not year_dict.get(month_i):
            continue
        else:
            date_num += year_dict[month_i]
    date_num += day
    return date_num

def read_work_book(file_path):
    work_book = load_workbook(file_path)
    sheets = work_book.worksheets # 获取所有的表单
    year_weather = {}
    sheet = sheets[0]
    rows = sheet.rows
    for row in rows:
        row_context = [cell.value for cell in row]
        if '日期' in row_context:
            continue
        date,week_day,weather,max_temp,min_temp,wind_direction,wind_strength = row_context
        # print(date) # '2011-01-01
        pure_date = date[1:]
        # print(pure_date) # 2011-01-01
        year,month,day = pure_date.split('-') # 2011 01 01
        year = int(year)
        month = int(month)
        day = int(day)
        date_num = get_date_num(year,month,day)
        if not year_weather.get(year):
            # year_weather[year] = [[date_num,weather,int(max_temp),int(min_temp),wind_direction,wind_strength]]
            year_weather[year] = [[date_num,int(max_temp),int(min_temp)]]
        else:
            # year_weather[year].append([date_num,weather,int(max_temp),int(min_temp),wind_direction,wind_strength])
            year_weather[year].append([date_num,int(max_temp),int(min_temp)])

    return year_weather # year:[ [date_num,max_temp,min_temp] ]

parser = argparse.ArgumentParser()
parser.add_argument('--filename',default='2011_2019.xlsx',type=str,help='输入数据文件')
parser.add_argument('--year',default=2018,type=int,help='要可视化的的年份')
parser.add_argument('--mode',default='max',choices=['max','min','mean'],type=str,help="要可视化的气温，可选最高温、最低温和平均温度")
args = parser.parse_args()

if __name__ == '__main__':
    file_path = args.filename
    year_weather_dict = read_work_book(file_path)
    # date_num = np.array(range(1,367))
    for year_num in year_weather_dict:

        if not year_num == args.year:
            continue
        ###---数据提取---###
        year_weather = year_weather_dict[year_num]
        year_weather = np.array(year_weather)
        date_num = year_weather[:,0]
        max_temp = year_weather[:,1]
        min_temp = year_weather[:,2]
        mean_temp = (max_temp+min_temp)*0.5
        if args.mode == "mean":
            plt.title('Mean temperature')
            plt.scatter(date_num,mean_temp,marker='.',color=color_dict[year_num],label=year_num) # 绘制平均气温和时间的散点关系
        elif args.mode == 'max':
            plt.title('Max temperature')
            plt.scatter(date_num,max_temp,marker='.',color=color_dict[year_num],label=year_num) # 绘制最高气温和时间的散点关系
        else:
            plt.title('Min temperature')
            plt.scatter(date_num,min_temp,marker='.',color=color_dict[year_num],label=year_num) # 绘制最低气温和时间
    plt.xlabel("Day")
    plt.ylabel('Temperature ℃')
    plt.show()
    print('fins')