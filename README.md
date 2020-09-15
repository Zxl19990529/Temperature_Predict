# 青岛天气

张心亮，17020022050，电子信息工程

## 爬虫文件weather.py

该文件是爬虫文件，用来爬取一定年份区间的气温等数据。使用方法为：

```bash
python weather.py --start_year 2011 --end_year 2019
```

最后会得到一个```起始年份_结束年份.csv```的文件。该文件用WPS或者Office打开后需要另存为```xlsx```格式，以便可视化程序和回归模型的读取。

## 可视化文件read_xlsx.py

该文件用于可视化某一年的气温随天数变化曲线。一共有三种模式：最高温，最低温和平均温度。
使用方法样例:

```bash
python read_xlsx.py --filename 2011_2019.xlsx --year 2018 --mode mean
```

## 线性回归模型文件MyLinear.py

该文件中我定义了```MyLinear```的类，实现了类似```sklearn.linear_model```中的```LinearRegression```模块的功能。可以指定要拟合的方程阶数。文件包含线性回归模型，模型评估和模型拟合结果的可视化

使用样例：

```bash
python MyLinear.py --filename 2011_2019.xlsx --degree 3 --mode mean
```
