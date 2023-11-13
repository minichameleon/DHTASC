# -*- coding: utf-8 -*-
import random
import json
import pathlib
import config
import numpy as np
"""
生成感知任务
感知任务包含以下选项：
    temp1：经度、纬度、任务截止时间、所属类别（经过聚类预处理得到）
    temp2：所需的传感器
    temp3：任务的预算
    temp4：任务所需的最少参与人数、任务所需的最多参与人数
"""
# 共计12种传感器类型，前10钟是常见的传感器，第11和第12是不常见的传感器
sensorID = list(range(1,config.sensor_num+1))

# 以一个小时作为一个任务分配周期
def genTask(file_name,flag=0):
    # flag 0：txt  1:json
    # 任务的经纬度从文件读取
    # 使用出租车一次行驶的终点经纬度（即下客点）作为感知任务所在的位置，到达终点的时间作为感知任务的截止时间
    Task = {}

    if flag==0:
        try:
            with open( file_name, encoding='utf-8' ) as f:
                lines = f.readlines( )
        except FileNotFoundError:
            print("文件不存在")
        i=0
        for line in lines:
            temp1 = line.strip().split(',')

            # 设置该任务需要的传感器数量
            sensorNum = int(random.gauss(config.mu_sensor_num_of_task,config.sigma_sensor_num_of_task))
            # 从传感器列表中随机选择sensorNum个类型的传感器
            x=0
            # 每个任务以0.2的概率拥有不通用的传感器11、12
            spec_sensor = [11,12]
            temp2 = []
            if sensorNum>=2:
                suiji1 = np.random.uniform( 0, 1, 2 )
                for no in range(2):
                    if suiji1[no]<=0.2:
                        temp2.append(spec_sensor[no])
                        x = x+1
            temp2 = temp2 + random.sample(sensorID[0:config.sensor_num-x],sensorNum-x)

            # 完成任务所需的参与者人数，low and high
            low = random.randint(config.left_need_people_low,config.right_need_people_low)
            high = random.randint(config.left_need_people_high,config.right_need_people_high)
            temp4 = [low,high]


            # 任务的预算与完成任务所需的传感器数量成正比,但是设置了任务最低预算
            price_per = random.randint(config.left_per_budget_range,config.right_per_budget_range)    #不同的任务发布者对任务的预算估计不同

            # 该任务的预算为
            temp3 = price_per * sensorNum * low
            # if temp3 < 10: temp3 = 10

            task = [temp1,temp2,temp3,temp4]
            Task[str(i)] = task
            i = i + 1
    elif flag==1:
        try:
            with open( file_name, encoding='utf-8' ) as f:
                lines = json.load(f)
        except FileNotFoundError:
            print("文件不存在")
        i=0
        for line in lines:
            temp1 = lines[str(line)]

            # 设置该任务需要的传感器数量
            sensorNum = int( random.gauss( config.mu_sensor_num_of_task, config.sigma_sensor_num_of_task ) )
            # 从传感器列表中随机选择sensorNum个类型的传感器
            x = 0
            # 每个任务以0.2的概率拥有不通用的传感器11、12
            spec_sensor = [11, 12]
            temp2 = []
            if sensorNum >= 2:
                suiji1 = np.random.uniform( 0, 1, 2 )
                for no in range( 2 ):
                    if suiji1[no] <= 0.2:
                        temp2.append( spec_sensor[no] )
                        x = x + 1
            temp2 = temp2 + random.sample( sensorID[0:config.sensor_num - x], sensorNum - x )

            # 完成任务所需的参与者人数，low and high
            low = random.randint( config.left_need_people_low, config.right_need_people_low )
            high = random.randint( config.left_need_people_high, config.right_need_people_high )
            temp4 = [low, high]

            # 任务的预算与完成任务所需的传感器数量成正比,但是设置了任务最低预算
            price_per = random.randint( config.left_per_budget_range,
                                        config.right_per_budget_range )  # 不同的任务发布者对任务的预算估计不同

            # 该任务的预算为
            temp3 = price_per * sensorNum * low
            # if temp3 < 10: temp3 = 10

            task = [temp1, temp2, temp3, temp4]
            Task[str( i )] = task
            i = i + 1

    return Task



if __name__ == '__main__':
    """ 生成某个小时内的任务"""

    # 存储某小时任务位置的文件地址
    for bai in range(65, 70):
        for ge in range(1, 25):
            if ge <= 9:
                addr = 'd100data_end\\' + str(bai) + '0' + str(ge) + '.txt'
                writename1 = 'ddd\\' + str(bai) + '0' + str(ge) + '.json'
            else:
                addr = 'd100data_end\\' + str(bai) + str(ge) + '.txt'
                writename1 = 'ddd\\' + str(bai) + str(ge) + '.json'
            # 如果构造的文件路径不存在，在继续下一个
            filepathx = pathlib.Path(addr)
            if not filepathx.exists():
                continue

            # addr = 'd100data_end\\6501.txt'
            TASK = genTask(addr)
            nums = len(TASK)
            for i in range(nums):
                print(TASK[str(i)])
            # sim = [[0 for i in range(nums)] for j in range(nums)]
            # for i in range(nums):
            #     ttemp = set(TASK[str(i)][1])
            #     for j in range(nums):
            #         if i==j:
            #             sim[i][j] = 0
            #         else:
            #             ttemp2 = set(TASK[str(j)][1])
            #             a = ttemp & ttemp2
            #             b = ttemp | ttemp2
            #             sim[i][j] = len(a) / len(b)
            # print(sim)
            with open( writename1, 'w', encoding='utf-8' ) as wf2:
                json.dump( TASK, wf2 )






