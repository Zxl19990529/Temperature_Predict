import os
import numpy as np 
from read_xlsx import get_date_num,read_work_book
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score
import argparse

class MyLinear:
    def __init__(self,x_train,y_train,degree=1):
        r'''
        x_train: 1-d ndarray like data
        y_train: 1-d ndarray like data
        degree: 要拟合的曲线阶数，int型变量
        '''
        self.x_train = x_train.reshape(-1,1) #自变量，输入数据。统一维度。
        self.y_train = y_train # 因变量
        self.degree = degree
        self.w = None # 系数 a0+a1x,a2x^2,a3x^3 ...
        self.eq = '' #用于储存等式，如：-2.67+0.136769x^1+0.000475x^2-0.000002x^3
    def fit(self):
        assert not self.w # 如果该对象之前拟合过，则不允许在拟合。
        x_b = np.ones((len(self.x_train),1)) # 对应0次幂的常数项（截距）
        for deg in range(0,self.degree): # 根据要拟合的维度扩增输入数据
            x_b = np.hstack([x_b,self.x_train**(deg+1)])
        self.w = np.linalg.inv(x_b.T.dot(x_b)).dot(x_b.T).dot(self.y_train)# 见最小二乘法理论
        #---将最终拟合的表达式以字符串储存---#
        self.eq = '%.2f'%self.w[0]
        for i in range(1,len(self.w)):
            if self.w[i]>0:
                self.eq +='+%fx^%d'%(self.w[i],i)
            elif self.w[i] == 0:
                continue
            else:
                self.eq+='%fx^%d'%(self.w[i],i)
        return self

    def predict(self,x_predict):
        x_predict = x_predict.reshape(-1,1)# 自变量，输入数据。统一维度。
        x_b = np.ones((len(x_predict),1))
        for deg in range(0,self.degree):
            x_b = np.hstack([x_b,x_predict**(deg+1)])
        return x_b.dot(self.w)

parser = argparse.ArgumentParser()
parser.add_argument('--filename',default='2011_2019.xlsx',type=str,help='输入数据文件')
parser.add_argument('--degree',default=3,type=int,help='要用几次的线性回归来拟合')
parser.add_argument('--mode',default='mean',choices=['max','min','mean'],type=str,help="要可视化的气温，可选最高温、最低温和平均温度")
args = parser.parse_args()

if __name__ == '__main__':
    file_path = args.filename
    degree = args.degree
    year_weather_dict = read_work_book(file_path)
    ###---制作数据集---#

    #---读取数据---#
    weather_2017 = year_weather_dict[2017]
    weather_2017 = np.array(weather_2017)
    date_num = weather_2017[:,0]
    max_temp = weather_2017[:,1]
    min_temp = weather_2017[:,2]
    mean_temp = (max_temp+min_temp)*0.5

    #---划分训练集、测试集---#
    if args.mode == "mean":
        x_train, x_test, y_train, y_test = train_test_split(date_num,mean_temp,test_size=0.1) #划分测试集占0.1
    elif args.mode == 'max':
        x_train, x_test, y_train, y_test = train_test_split(date_num,max_temp,test_size=0.1) #划分测试集占0.1
    else:
        x_train, x_test, y_train, y_test = train_test_split(date_num,min_temp,test_size=0.1) #划分测试集占0.1
    #---构建模型进行拟合---#
    model = MyLinear(x_train,y_train,degree=degree)
    model.fit()
    pred_train = model.predict(x_train)
    pred_test = model.predict(x_test)

    train_mse = mean_squared_error(y_train,pred_train)
    test_mse = mean_squared_error(y_test,pred_test)
    train_r2 = r2_score(y_train,pred_train)
    test_r2 = r2_score(y_test,pred_test)
    print('-----使用了%d次模线性模型-----'%degree)
    print('拟合的曲线为：%s'%model.eq)
    print('训练集均方误差 | r2-score : %.2f | %.2f'%(train_mse,train_r2))
    print('测试集均方误差 | r2-score : %.2f | %.2f'%(test_mse,test_r2))

    #---绘图部分---#
    pred_y_all = model.predict(date_num)
    plt.scatter(date_num,mean_temp,color='b')
    plt.plot(date_num,pred_y_all,color='r')
    plt.xlabel("Day")
    plt.ylabel('Temperature ℃')
    if args.mode == "mean":
        plt.title('Day-Temp(mean) relationship (Qingdao)')
    elif args.mode == 'max':
        plt.title('Day-Temp(max) relationship (Qingdao)')
    else:
        plt.title('Day-Temp(min) relationship (Qingdao)')    
    plt.show()
