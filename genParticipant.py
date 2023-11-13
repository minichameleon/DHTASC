# -*- coding: utf-8 -*-
import json
import pathlib
import random
import time
import numpy as np
import sys

import config

"""
生成参与者概貌
感知任务包含以下选项：
    temp1：经度、纬度、当前所在时间(初始化为该时段（小时）的开头时间)
    temp2：具有的传感器
        temp21：参与者愿意贡献的传感器
        temp22：参与者存在顾虑的传感器
        temp23：参与者不存在传感器（此类型的传感器限制在一到两种内选择，参与者以0.5的概率拥有该传感器。若参与者拥有该传感器则将其并入temp21或temp22）
            
            参与者具有的传感器每个传感器的工作负载
"""

# 共计12种传感器类型，前10钟是常见的传感器，第11和第12是不常见的传感器
def genParticipant(filename,unix_stamp_moment,flag=0):

    # 参与者的经纬度从文件读取
    # 使用出租车一次行驶的起点经纬度（即上客点）作为参与者的其实位置，参与者的时间初始化为该时段的起始时间
    if flag==0:
        try:
            with open(filename,encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            print( "文件不存在" )
        panticipant = {}
        i = 0
        for line in lines:
            temp1 = line.strip().split(',')[0:2]
            #将起始时间转化为时间戳
            work_time = "2008-" + unix_stamp_moment[0] + "-" + unix_stamp_moment[1] + " " + str(int( unix_stamp_moment[2:4] ) - 1 ) + ":00:00"
            timeArray = time.strptime( work_time, "%Y-%m-%d %H:%M:%S" )
            work_start_time = int( time.mktime( timeArray ) )
            temp1.append(work_start_time)

            # 以正态分布设置参与者愿意共享的传感器类型的数目
            while True:
                willing_sensor_num = int(random.gauss((config.sensor_num)//2,1))
                if willing_sensor_num<=config.sensor_num-2:
                    print(willing_sensor_num)
                    break
            willing_sensor = random.sample(list(range(1,config.sensor_num-1)),willing_sensor_num)
            no_willing_sensor = []
            for no in range(1,config.sensor_num-1):
                if no not in willing_sensor:
                    no_willing_sensor.append(no)
            no_exist_sensor = []
            # 参与者以0.5的概率拥有11号和12号传感器
            suiji1 = np.random.uniform(0,1,2)
            for no in range(2):
                if suiji1[no] >0.5:
                    suiji2 = np.random.uniform(0,1,1)
                    if suiji2 >=0.5:
                        willing_sensor.append(config.sensor_num-1+no)
                    else:
                        no_willing_sensor.append(config.sensor_num-1+no)
                else:
                    no_exist_sensor.append(config.sensor_num-1+no)
            # 为每个传感器生成期望报酬和负载，其中愿意共享的传感器期望报酬为0
            temp21 = []
            for w in willing_sensor:
                workload = random.randint(config.left_workload,config.right_workload)
                temp21.append([w,0,workload])
            temp22 = []
            for nw in no_willing_sensor:
                pay = random.randint(config.left_pay,config.right_pay)
                workload = random.randint(config.left_workload,config.right_workload)
                temp22.append([nw,pay,workload])
            temp23 = []
            for ne in no_exist_sensor:
                pay = sys.maxsize
                workload = 0
                temp23.append([ne,pay,workload])
            temp2 = temp21+temp22+temp23
            panticipant[str(i)] = [temp1,temp2]
            i = i + 1
    elif flag == 1:

        try:
            with open(filename,encoding='utf-8') as f:
                lines = json.load(f)
        except FileNotFoundError:
            print( "文件不存在" )
        panticipant = {}
        i = 0
        for line in lines:
            temp1 = lines[str(line)]

            while True:
                willing_sensor_num = int( random.gauss( (config.sensor_num) // 2, 1 ) )
                if willing_sensor_num <= config.sensor_num - 2:
                    print( willing_sensor_num )
                    break
            willing_sensor = random.sample( list( range( 1, config.sensor_num - 1 ) ), willing_sensor_num )
            no_willing_sensor = []
            for no in range( 1, config.sensor_num - 1 ):
                if no not in willing_sensor:
                    no_willing_sensor.append( no )
            no_exist_sensor = []
            # 参与者以0.5的概率拥有11号和12号传感器
            suiji1 = np.random.uniform( 0, 1, 2 )
            for no in range( 2 ):
                if suiji1[no] > 0.5:
                    suiji2 = np.random.uniform( 0, 1, 1 )
                    if suiji2 >= 0.5:
                        willing_sensor.append( config.sensor_num - 1 + no )
                    else:
                        no_willing_sensor.append( config.sensor_num - 1 + no )
                else:
                    no_exist_sensor.append( config.sensor_num - 1 + no )
            # 为每个传感器生成期望报酬和负载，其中愿意共享的传感器期望报酬为0
            temp21 = []
            for w in willing_sensor:
                workload = random.randint( config.left_workload, config.right_workload )
                temp21.append( [w, 0, workload] )
            temp22 = []
            for nw in no_willing_sensor:
                pay = random.randint( config.left_pay, config.right_pay )
                workload = random.randint( config.left_workload, config.right_workload )
                temp22.append( [nw, pay, workload] )
            temp23 = []
            for ne in no_exist_sensor:
                pay = sys.maxsize
                workload = 0
                temp23.append( [ne, pay, workload] )
            temp2 = temp21 + temp22 + temp23
            panticipant[str( i )] = [temp1, temp2]
            i = i + 1
    return panticipant


if __name__ == '__main__':

    # 存储某小时任务位置的文件地址
    for bai in range( 65, 70 ):
        for ge in range( 1, 25 ):
            if ge <= 9:
                addr = 'd100data_start\\' + str( bai ) + '0' + str( ge ) + '.txt'
                writename1 = 'ddd_d100data_start_with_sensor\\' + str( bai ) + '0' + str( ge ) + '.json'
                timestamp = str( bai ) + '0' + str( ge )
            else:
                addr = 'd100data_start\\' + str( bai ) + str( ge ) + '.txt'
                writename1 = 'ddd_d100data_start_with_sensor\\' + str( bai ) + str( ge ) + '.json'
                timestamp = str( bai ) + str( ge )

            # 如果构造的文件路径不存在，在继续下一个
            filepathx = pathlib.Path( addr )
            if not filepathx.exists( ):
                continue
            # addr = 'd100data_start/6501.txt'
            panticipant = genParticipant(addr,timestamp)
            print(type(panticipant))
            print( timestamp + ":" )
            for i in range(len(panticipant)):
                print(panticipant[str(i)])
            with open(writename1,'w',encoding='utf-8') as f:
                json.dump(panticipant,f)












