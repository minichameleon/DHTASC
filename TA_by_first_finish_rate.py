# -*- coding: utf-8 -*-

"""
#以任务完成率优先的任务分配方法
"""

import copy
import sys
import json

from calculateDis import getDistance
import config

def verify(ttask,tworker):
    """验证参与者tworker能否完成任务ttask"""

    # 验证到达时间
    dis = getDistance(ttask[0][0],ttask[0][1],tworker[0][0],tworker[0][1])  # 计算参与者与任务之间的距离
    the_now_time = int(tworker[0][2]) #将参与者的时间作为当前时间
    move_time = dis*100/config.v   # 参与者移动到任务点需要花费的时间
    arrive_time = the_now_time  + move_time #参与者到达任务点的时间
    if arrive_time > int(ttask[0][2]): # 如果达到时间已经超过了任务截止时间，则认为该参与者不能完成该任务
        return False

    # 验证传感器能否满足
    psensor = [s[0] for s in tworker[1]]  # 获取参与者的全部传感器id
    tsensor = ttask[1] # 任务所需要的传感器类型
    psensorset = set(psensor)  # 以集合的形式组织
    tsensorset = set(tsensor)  # 以集合的形式组织
    if not tsensorset.issubset(psensorset):  # 如果任务所需要的传感器不是参与者所具有的传感器的子集，则参与者指定不能完成该任务
        return False
    flag = True
    # 验证参与者的传感器负载是否满足要求
    for tsid in tsensor: # 对于任务需要的每一个传感器
        for psid in range(len(psensor)): #遍历参与者具有的所有传感器
            if tsid == psensor[psid]:  # 任务所需的传感器与参与者者具有的传感器匹配上
                if tworker[1][psid][2]<1: # 进一步判断 参者具有的该传感器是否还能被使用至少一次
                # 传感器匹配上，且负载数量不能满足要求，即便一个不满足也意味着任务不能被完成
                    flag = False
                    return flag
                # 匹配上且满足，则进行到下一个任务所需的传感器
                break
    return flag


def change_profile(replaceid,raw_profile,refer_profile):
    """
    # 更新参与者概貌信息
    :param replaceid: 被分配了任务的参与者id
    :param raw_profile: 原参与者概貌
    :param refer_profile: 在尝试新的任务分配过程中参与者概貌发生的变化
    :return: 替换后的参与者概貌
    """
    copy_raw_profile= copy.deepcopy( raw_profile )
    replace_len = len(replaceid)
    for i in range(replace_len):
        copy_raw_profile[str(replaceid[i])] = refer_profile[replaceid[i]]
    return copy_raw_profile


def allocate_by_first_finish_rate(filename,filename2):
    # -- 参与者数据
    with open( filename, 'r', encoding='utf-8' ) as f:
        participant = json.load( f )

    # -- 感知任务数据
    with open( filename2, 'r', encoding='utf-8' ) as f:
        Task = json.load( f )

    taskLen = len( Task )  # 任务的数量
    participantLen = len( participant )  # 参与者的数量
    resTask = list(range(taskLen)) # 将任务id序列化
    participant_profile_temp = copy.deepcopy(participant)  # 用来描述参与者与任务的匹配后的参与者的概貌变化
    finish_rate = 0 # 累加，计算每一轮选择后 任务的完成率
    distance = 0  # 累加，计算每一轮选择后，总得移动距离的变化
    haved_accomplish = 0  # 统计已经完成的任务数量
    while(len(resTask)>0):
        global_finish = []
        global_dis = []
        participant_profile_change_refer = [] # 用来表示参与者在执行各个任务时的参与者情况变化
        for tid in resTask:
            task = copy.deepcopy(Task[str(tid)])
            participant_profile_temp_2 = copy.deepcopy( participant_profile_temp ) #对每个任务进行分配时，将参与者信息恢复
            budget = int(task[2]) # 当前任务的预算
            tsensor = task[1]  # 当前任务需要的传感器
            paypal = [] # 用来记录每个参与者完成该任务所需要的支付报酬
            juli = [] # 用来记录每个参与者完成该任务时移动的距离
            need_people_min = task[3][0] # 当前任务需要的参与者最少人数
            need_people_max = task[3][1] # 当前任务需要的参与者最多人数
            participant_profile_temp_refer = [] # 用来记录参与者完成某个任务后，每个参与者状态的变化
            for pid in range(participantLen):
                worker = copy.deepcopy( participant_profile_temp_2[str( pid )] )
                if verify(task,worker):
                    dis = getDistance(task[0][0],task[0][1],worker[0][0],worker[0][1])
                    temp_paypal = 0 # 记录参与者worker完成任务的paypal
                    psensor = [s[0] for s in worker[1]] # 参与者拥有的传感器id
                    for tsid in tsensor: # 对于任务所需要的每一个传感器
                        for psid in range(len(psensor)):
                            if tsid == psensor[psid]: # 如果任务所需的传感器与参与者具有的传感器匹配上
                                if worker[1][psid][1] == 0: #如果该传感器所需报酬为0，即不存在顾虑，对该传感器支付报酬 1
                                    temp_paypal += 1
                                else: # 否则支付该传感器的顾虑报酬
                                    temp_paypal += worker[1][psid][1]
                                worker[1][psid][2] -= 1   # 参与者的负载减去1
                                break
                    worker[0][0] = task[0][0] # 更新参与者执行完此任务后的经纬度
                    worker[0][1] = task[0][1]
                    worker[0][2] = int(worker[0][2]) + dis*100/config.v  # 更新参与者执行完此任务的时间，参与者当前时间+移动到任务节点的时间
                    temp_paypal += 2*dis # 参与者完成此任务需要的报酬： 传感器报酬 + 移动报酬
                else:
                    # 如果参与者不能执行此任务，则将其需要的报酬设为最大值
                    temp_paypal = sys.maxsize
                    # 移动距离设置为最大致
                    dis = sys.maxsize
                paypal.append(temp_paypal)
                juli.append(dis)
                participant_profile_temp_refer.append(worker)

            # 当计算完，每个参与者执行当前任务所需的移动距离和报酬后，
            # 按照 paypal 从小到大排序
            sort_paypal = sorted(enumerate(paypal),key=lambda x:x[1])
            idx = [x[0] for x in sort_paypal]  # 获取下标
            temp_budget = 0 # 已经支出的预算
            count = 0 # 选择的参与者人数
            temp_dis = 0 # 完成当前任务的总移动距离
            for idxx in idx:
                temp_budget = temp_budget + paypal[idxx]
                if temp_budget<=budget:
                    # 如果还有预算能够招募该用户
                    count += 1
                    temp_dis += juli[idxx]
                else:
                    # 否则就跳出
                    break
                if count==need_people_max:
                    # 或达到最大所需参与者人数
                    break

            # 计算任务完成率
            if count<need_people_min:
                # 如果招募的人数小于任务所需的最少参与者人数，那么该任务没有被完成，有效参与人数为0
                f_i = 0
                global_finish.append(0)   # 实际任务完成率为0
                global_dis.append(sys.maxsize) # 将总移动距离设置为最大
                participant_profile_change_refer.append( participant_profile_temp_2 ) # 依旧将原来的未变化的参与者概貌加入队列
            elif count>=need_people_min and count<=need_people_max: # 如果大于最小值时 且 小于等于最大值时 （前边的任务分配时，在达到最大值时已经跳出）
                f_i = count # 有效参与者数量为实际参与者人数
                if need_people_max == need_people_min: # 如果最大人数等于最小人数 时，按照比例计算。
                    temp_finish = (f_i/need_people_max)*2
                    global_dis.append( temp_dis )
                else:
                    temp_finish = 1+(f_i-need_people_min)*1.0/(need_people_max-need_people_min)
                    global_dis.append( temp_dis )
                global_finish.append(temp_finish)
                change_profile_temp = change_profile( idx[:f_i], participant_profile_temp_2,
                                                      participant_profile_temp_refer )
                participant_profile_change_refer.append( change_profile_temp )
        not_equall_zero = [x for x in global_finish if x != 0]
        not_equall_max = [x for x in global_dis if x != sys.maxsize]
        if len(not_equall_zero)==0 or len(not_equall_max)==0: # 如果不能再进行分配
            break
        sort_finish_rate = sorted(enumerate(global_finish),key=lambda x:x[1],reverse=True)
        idxu = [idx[0] for idx in sort_finish_rate]
        for suif in idxu:
            if global_dis[suif] != sys.maxsize:
                smallest_utility_in_fact = suif
                break
        finish_rate = finish_rate + global_finish[smallest_utility_in_fact]
        print(f"当前分配的任务是{resTask[smallest_utility_in_fact]}")
        print(f"本次分配后增加的任务完成率是{global_finish[smallest_utility_in_fact]}")
        distance = distance + global_dis[smallest_utility_in_fact]
        haved_accomplish += 1
        participant_profile_temp = copy.deepcopy(participant_profile_change_refer[smallest_utility_in_fact])
        resTask.remove(resTask[smallest_utility_in_fact])
        print(f"当前的任务完成率是{finish_rate},移动距离是{distance},已完成的任务数量是{haved_accomplish}")
    return finish_rate,distance,haved_accomplish



if __name__ == '__main__':
    filename = 'newdata_d100data_start_with_sensor/6502.json'
    filename2 = 'ddd/6502.txt'
    GF,JL,TN = allocate_by_first_finish_rate(filename,filename2)
    print("-"*20)
    print(GF,JL,TN)
