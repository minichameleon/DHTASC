# -*- coding: utf-8 -*-

"""
#以任务完成率优先的任务分配方法
"""

import copy
import sys
import json
from tkinter import W

from calculateDis import getDistance
import config

class verify():

    def __init__(self,ttask,wworker) -> None:
        self.task = ttask
        self.worker = copy.deepcopy(wworker)
        self.result = self.judge()
    
    def judge(self):
        # 判断能够在任务的截止日期前到达
        the_now_time = int(self.worker[0][2])
        self.dis = getDistance(self.task[0][0],self.task[0][1],self.worker[0][0],self.worker[0][1])
        move_time = self.dis * 1000 /config.v
        self.arrive_time = the_now_time + move_time
        # 如果达到时间大于任务截止时间，则任务不能被完成
        if self.arrive_time>int(self.task[0][2]):
            self.dis = sys.maxsize
            self.paypal = sys.maxsize
            return False
        
        # 判断传感器类型能否满足要求 以及所需要花费
        tsensor = self.task[1]
        psensor = [s[0] for s in self.worker[1] if s[1]!=sys.maxsize]
        tsensorset = set(tsensor)
        psensorset = set(psensor)
        if not tsensorset.issubset(psensorset): # 如果任务所需的传感器类型不是参与者的子集
            self.dis = sys.maxsize
            self.paypal = sys.maxsize
            return False


        # 判断传感器类型能否满足要求 以及所需要花费
        flag = True
        paypal_temp = 0
        for tsid in tsensor:
            for psid in range(len(psensor)):
                if tsid == psensor[psid]:
                    if self.worker[1][psid][2] < 1:  # 负载不满足
                        flag = False
                        break
                    else: # 负载满足
                        self.worker[1][psid][2] = self.worker[1][psid][2] - 1
                        if self.worker[1][psid][1] == 0:
                            paypal_temp = paypal_temp + 1
                        else:
                            paypal_temp = paypal_temp + self.worker[1][psid][1]
            if flag == False: # 如果不满足
                break
        if flag == False:  # 如果不满足 将距离和成本置为最大值（这样处理在后续选择中永远不会被选择到）
            self.dis = sys.maxsize
            self.paypal = sys.maxsize
        else: # 如果符合要求，则开始计算报酬、到达时间
            self.paypal = paypal_temp + 2 * self.dis
            self.worker[0][0] = self.task[0][0]
            self.worker[0][1] = self.task[0][1]
            self.worker[0][2] = self.arrive_time
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
                
# 任务分配
def allocate_by_first_finish_rate(filename,filename2):
    # -- 参与者数据
    with open( filename, 'r', encoding='utf-8' ) as f:
        participant = json.load( f )

    # -- 感知任务数据
    with open( filename2, 'r', encoding='utf-8' ) as f:
        Task = json.load( f )

    # 任务的数量
    taskLen = len(Task)
    # 参与者的数量
    participantLen = len(participant)
    # 将任务序列化
    resTask = list(range(taskLen)) # 还未被完成的任务
    # 初始化各个变量
    total_finish_rate = 0
    total_dis = 0
    have_accomplished = 0
    pariticipant_profile = copy.deepcopy(participant) # 记录尝试为每一个任务分配参与者时的参与者状态
    utility=0
    # 迭代的尝试选择一个任务与参与者的组合使得任务完成率最大
    while(len(resTask)>0):

        global_finish = []
        global_dis = []
        pariticipant_profile_refer = []

        for tid in range(taskLen):
            # 如果tid任务已经被分配了，则继续下一个
            if tid not in resTask:
                continue
            # 获取当前任务信息
            task = Task[str(tid)]
            tsensor = task[1]            # 完成该任务所需的传感器类型
            budget = int(task[2])        # 该任务所能提供的预算
            need_people_min = task[3][0] # 该任务所需要的最少参与者人数
            need_people_max = task[3][1] # 该任务所需要的最多参与者人数

            # 参与者初始化（因为是在所有任务中选择一对组合，所以，对于每个任务来说参与者的状态应该是一致的）
            pariticipant_profile_temp = copy.deepcopy(pariticipant_profile)

            # 初始化各个变量
            juli = []       # 记录每个参与者完成当前任务时的移动距离
            paypal = []     # 记录每个参与者完成当前任务所要求的的支付报酬
            pariticipant_profile_temp_refer = [] #用来记录为了完成当前任务参与者的状态变化

            for pid in range(participantLen):
                # 因为参与者在执行任务的过程中会改变位置以及负载，因此先复制一份
                worker = copy.deepcopy(pariticipant_profile_temp[str(pid)])

                # 验证参与者是否具备完成此任务的条件：
                    # 能否在截止日期前到达
                    # 传感器类型能否满足
                    # 传感器负载能否满足
                yanzheng = verify(task,worker)
                juli.append(yanzheng.dis)
                paypal.append(yanzheng.paypal)
                pariticipant_profile_temp_refer.append(yanzheng.worker)
            sort_paypal = sorted(enumerate(paypal),key=lambda x:x[1])
            # 按照支付报酬大小排序的结果
            id_paypal = [i[0] for i in sort_paypal]
            # 根据预算尽可能的选择参与者
            have_spent_paypal = 0 # 表示为了选择参与者已经花费的预算
            count = 0 # 表示已经为当前用户选择的参与者人数
            temp_dis = 0 #为完成该任务，参与者移动的距离
            for pselectid in id_paypal:
                have_spent_paypal = have_spent_paypal + paypal[pselectid]
                # 如果超出预算，则跳出；没超过继续选择
                if have_spent_paypal > budget:
                    break
                else:
                    count = count + 1
                    temp_dis = temp_dis + juli[pselectid]
            if count < need_people_min: # 如果小于任务要求参与者人数的最小值
                f_i = 0 
            elif count>=need_people_min and count < need_people_max:  # 如果招募到参与者人数介于最小值和最大值之间
                f_i = count
            else: # 如果招募到的参与者人数大于最大值
                f_i = need_people_max
            if need_people_max == need_people_min: # 任务所需最小参与者人数和最大参与者人数相等的情况
                finish_rate = (f_i/need_people_max)*2
            else: # 不相等的情况
                if f_i==0:
                    finish_rate = 0
                else:
                    finish_rate = 1 + (f_i-need_people_min)/(need_people_max-need_people_min)
            if finish_rate == 0: # 完成率为0时 不做改变
                pariticipant_profile_refer.append(pariticipant_profile_temp)
            else: # 否则更新
                pariticipant_profile_refer.append(change_profile(id_paypal[:f_i],pariticipant_profile_temp,pariticipant_profile_temp_refer))
            global_finish.append(finish_rate)
            global_dis.append(temp_dis)
        if len([x for x in global_finish if x!=0])==0 or len([x for x in global_dis if x!= sys.maxsize])==0:
            break
        sort_finish = sorted(enumerate(global_finish),key=lambda x:x[1]) # 排序选择最大的
        for sf in sort_finish:
            if global_dis[sf[0]] != sys.maxsize:
                best_task_id = sf[0]
        pariticipant_profile=copy.deepcopy(pariticipant_profile_refer[best_task_id])
        have_accomplished = have_accomplished + 1
        # print(f"本轮分配中的第{best_task_id}个")
        # print(f"实际分配任务id为{resTask[best_task_id]}")
        # print(f"本次完成任务后增加的任务完成率是{global_finish[best_task_id]}")
        # print(f"本次完成任务后增加的移动距离是{global_dis[best_task_id]}")
        # print(f"已经分配的任务数量{have_accomplished}")
        #  ------------------计算综合效用-------------------------------------------------
        global_task_loss_rate = [2 - bl for bl in global_finish]
        max_loss_rate = max( global_task_loss_rate )
        min_loss_rate = min( global_task_loss_rate )
        max_dis = max( [x for x in global_dis if x != sys.maxsize] )
        min_dis = min( [x for x in global_dis if x != sys.maxsize] )
        if max_loss_rate == min_loss_rate:
            lin_loss_rate = 0
        else:
            lin_loss_rate = (global_finish[best_task_id] - min_loss_rate) / (max_loss_rate - min_loss_rate)
        if max_dis == min_dis:
            lin_dis = 0
        else:
            lin_dis = (global_dis[best_task_id] - min_dis) / (max_dis - min_dis)
        temp_utility = config.alpha * lin_loss_rate + (1 - config.alpha) * lin_dis
        utility = utility + temp_utility
        # ----------------------------------------------------------------------------------
        resTask.remove(resTask[best_task_id])
        total_finish_rate = total_finish_rate + global_finish[best_task_id]
        total_dis = total_dis + global_dis[best_task_id]
        # print(f"当前任务完成率为{total_finish_rate},移动距离为{total_dis},已经分配的任务数量{have_accomplished}")
    return total_finish_rate,total_dis,utility,have_accomplished


if __name__ == '__main__':
    print( 6507 )
    filename = 'newdata_d100data_start_with_sensor/6507.json'
    filename2 = 'newdata_d100data_end_with_task/6507.txt'
    GF,JL,TN ,xx= allocate_by_first_finish_rate(filename,filename2)
    print("-"*20)
    print(GF,JL,TN)