# -*- coding: utf-8 -*-

import random
import copy
import math
import json
import sys

import config
from calculateDis import getDistance
"""
通过随机安排的方式，为任务寻找参与者
"""
# 对于每一个任务，随机为其选择最大参与者人数

# 按照截止时间对任务排序
def sort_task_by_deadline(TASK,Tid):
    temp = [int(TASK[str(t)][0][2]) for t in Tid]
    x_temp  = sorted(enumerate(temp),key=lambda x:x[1])
    x_id = [dd[0] for dd in x_temp ]
    shunxu = [Tid[q] for q in x_id]
    return shunxu

# 验证参与者能否完成任务
def verify(ttask,wworker):
    the_now_time = int(wworker[0][2]) # 参与者当前的时间
    move_dis = getDistance(ttask[0][0],ttask[0][1],wworker[0][0],wworker[0][1]) # 计算参与者与任务之间的距离
    move_time = move_dis*100/config.v # 计算移动时间
    timeflag = True
    if the_now_time + move_time > int(ttask[0][2]) : # 判断执行某任务时间能都满足要求
        timeflag = False
        return False
    ttask_nedd_sensor = set(ttask[1])
    wworker_have_sensor = [s[0] for s in wworker[1] if s[1]!= sys.maxsize]
    t_budget = int(ttask[2]) - move_dis*2
    if t_budget<0:
        return False
    numflag = False
    if ttask_nedd_sensor.issubset(set(wworker_have_sensor)):
        # 如果参与者满足任务要求，则判断数量是否满足
        numflag = True
        for ttask_nedd_sensor_id in ttask_nedd_sensor:
            index = wworker_have_sensor.index(ttask_nedd_sensor_id)
            if wworker[1][index][1]==0: # 如果需要的传感器是愿意共享的传感器，则预算减1
                temp_budget = t_budget - 1
            else: # 否则减去参与者的期望报酬
                temp_budget= t_budget - wworker[1][index][1]
            if wworker[1][index][2] - 1 < 0 and temp_budget < 0: # 如果预算不足则表示任务无法完成
                numflag = False
                break
            else: # 否则更新参与者的传感器工作负载
                wworker[1][index][2] = wworker[1][index][2] - 1
                t_budget = temp_budget

    if timeflag and numflag: # 如果时间和数量都满足
        return True
    else:
        return False

def randomMatch(filename,filename2):
    # -- 参与者数据
    with open( filename, 'r', encoding='utf-8' ) as f:
        participant = json.load( f )

    # -- 感知任务数据
    with open( filename2, 'r', encoding='utf-8' ) as f:
        Task = json.load( f )

    taskLen = len(Task)
    participantLen = len(participant)
    pid = list(range(participantLen))
    assign_participant = [] # 分配
    for tid in range(taskLen):
        task = Task[str(tid)]
        budget = int(task[2])
        need_people_min = int(task[3][0])
        need_people_max = int(task[3][1])
        need_sensor = task[1]
        assign_id = random.sample(pid,need_people_max)
        assign_participant.append(assign_id)
    # 统计每个参与者完成哪些任务
    assign_task = [[] for i in range(participantLen)]
    for tid in range(taskLen):
        for pp in assign_participant[tid]:
            assign_task[pp].append(tid)

    task_finish_rate = [0 for i in range(taskLen)]
    total_dis = [0 for i in range(participantLen)]
    for pid in range(participantLen):
        if assign_task[pid]!=[]:
            assign_task[pid]=sort_task_by_deadline(Task,assign_task[pid])
            # 计算任务能否被完成和任务完成率、移动距离等
            worker = copy.copy(participant[str(pid)])
            the_now_time = int(worker[0][2])
            for j in assign_task[pid]:
                wworker = copy.copy(worker)
                if verify(Task[str(j)],wworker):
                    # 如果任务的到达时间和传感器匹配以及数量能够满足，则分配，并更新参与者状态
                    task_finish_rate[j] = task_finish_rate[j]  + 1
                    dis = getDistance(Task[str(j)][0][0],Task[str(j)][0][1],worker[0][0],worker[0][1])
                    total_dis[pid] = total_dis[pid] + dis
                    worker[0][0] = Task[str(j)][0][0]
                    worker[0][1] = Task[str(j)][0][1]
                    worker[0][2] = the_now_time + dis*100/config.v
                    # 更新 传感器负载
                    temp_budget = 0
                    psensor = [s[0] for s in worker[1]]
                    for sid in Task[str(j)][1]:
                        sindex = psensor.index(sid)
                        worker[1][sindex][2] = worker[1][sindex][2] - 1
                        temp_budget = temp_budget + int(worker[1][sindex][1])
                    Task[str( j )][2] = Task[str(j)][2] - temp_budget - 2 * dis
    global_finish = 0
    finish = []
    distance = []
    juli = 0
    task_num = 0
    for i in range(taskLen):
        if task_finish_rate[i] < Task[str(i)][3][0]:  # 小于最小参与者人数
            f_i = 0
            finish.append(0)
        elif task_finish_rate[i] >= int(Task[str(i)][3][0]) and task_finish_rate[i] < int(Task[str(i)][3][1]): #在范围内
            f_i = task_finish_rate[i]
            if int(Task[str(i)][3][0]) == int(Task[str(i)][3][1]):
                temp_finish = (f_i/int(Task[str(i)][3][0]))*2
                global_finish = global_finish + temp_finish
                finish.append(temp_finish)
            else:
                temp_finish = 1 + (f_i-int(Task[str(i)][3][0]))/(int(Task[str(i)][3][1])-int(Task[str(i)][3][0]))
                global_finish = global_finish + temp_finish
                finish.append(temp_finish)
            task_num = task_num + 1
        else:  # 大于等于最大值
            f_i = Task[str(i)][3][1]
            if int( Task[str( i )][3][0] ) == int( Task[str( i )][3][1] ): # 最大值等于最小值
                temp_finish = (f_i / int( Task[str( i )][3][0] )) * 2
                global_finish = global_finish + temp_finish
                finish.append(temp_finish)
            else: # 其他
                temp_finish = 1 + (f_i - int( Task[str(i)][3][0] )) / (
                            int( Task[str(i)][3][1] ) - int( Task[str(i)][3][0] ))
                global_finish = global_finish + temp_finish
                finish.append(temp_finish)
            task_num = task_num + 1
    for i in range(participantLen):
        juli = juli + total_dis[i]

    return global_finish,juli,task_num



if __name__ == '__main__':
    filename = 'newdata_d100data_start_with_sensor/6501.json'
    filename2 = 'newdata_d100data_end_with_task/6501.txt'
    GF,JL,TN = randomMatch(filename,filename2)
    print("-"*20)
    print(GF,JL,TN)
