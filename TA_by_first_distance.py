# -*- coding: utf-8 -*-

"""
以移动距离为目标进行任务分配
"""

import json
import copy
import sys

from calculateDis import getDistance
import config



def verify(ttask,tworker):
    """验证参与者tworker能否完成任务ttask"""

    # 验证到达时间
    dis = getDistance(ttask[0][0],ttask[0][1],tworker[0][0],tworker[0][1])
    the_now_time = int(tworker[0][2])
    move_time = dis*100/config.v
    arrive_time = the_now_time  + move_time
    if arrive_time > int(ttask[0][2]):
        return False

    # 验证传感器能否满足
    psensor = [s[0] for s in tworker[1] if s[1]!=sys.maxsize]
    tsensor = ttask[1]
    psensorset = set(psensor)
    tsensorset = set(tsensor)
    if not tsensorset.issubset(psensorset):
        return False
    flag = True
    for tsid in tsensor:
        for psid in range(len(psensor)):
            if tsid == psensor[psid]:
                if tworker[1][psid][2]<1:
                # 传感器匹配上，且负载数量满足要求
                    flag = False
                    return flag
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
    # 多重列表需要使用copy
    copy_raw_profile= copy.deepcopy( raw_profile )
    replace_len = len(replaceid)
    for i in range(replace_len):
        copy_raw_profile[str(replaceid[i])] = refer_profile[replaceid[i]]
    return copy_raw_profile




def allocate_by_first_distance(filename,filename2):
    # -- 参与者数据
    with open( filename, 'r', encoding='utf-8' ) as f:
        participant = json.load( f )

    # -- 感知任务数据
    with open( filename2, 'r', encoding='utf-8' ) as f:
        Task = json.load( f )


    taskLen = len( Task )
    participantLen = len( participant )
    resTask = list( range( taskLen ) )
    participant_profile_temp = copy.deepcopy(participant)  # 用来描述参与者与任务的匹配后的参与者的概貌变化
    finish_rate = 0
    distance = 0
    haved_accomplish = 0
    utility = 0
    while (len( resTask ) > 0):
        global_finish = []
        global_dis = []
        participant_profile_change_refer = []  # 用来表示参与者在执行各个任务时的参与者情况变化
        for tid in resTask:
            task = copy.deepcopy( Task[str( tid )] )
            budget = int( task[2] )
            tsensor = task[1]
            paypal = []
            juli = []
            participant_profile_temp_2 = copy.deepcopy( participant_profile_temp )  # 对每个任务进行分配时，将参与者信息恢复
            need_people_min = task[3][0]
            need_people_max = task[3][1]
            participant_profile_temp_refer = [] # 用来记录参与者完成某个任务后，状态的变化
            for pid in range( participantLen ):
                worker = copy.deepcopy( participant_profile_temp[str( pid )] )
                if verify( task, worker ):
                    dis = getDistance( task[0][0], task[0][1], worker[0][0], worker[0][1] )
                    temp_paypal = 0 # 累加，计算参与者worker完成任务task的支付报酬
                    psensor = [s[0] for s in worker[1] if s[1]!=sys.maxsize]  # 参与者具有的传感器
                    for tsid in tsensor: # 对于任务所需的每一个传感器
                        for psid in range( len( psensor ) ): #遍历参与者具有的传感器
                            if tsid == psensor[psid]: # 如果参与者id与
                                if worker[1][psid][1] == 0:
                                    temp_paypal += 1
                                else:
                                    temp_paypal += worker[1][psid][1]
                                worker[1][psid][2] -= 1
                                break
                    worker[0][0] = task[0][0]
                    worker[0][1] = task[0][1]
                    worker[0][2] = int( worker[0][2] ) + dis * 100 / config.v
                    temp_paypal += 2 * dis
                else:
                    # 不能满足直接置为最大值   报酬和距离
                    temp_paypal = sys.maxsize
                    dis = sys.maxsize
                paypal.append( temp_paypal )
                juli.append( dis )
                participant_profile_temp_refer.append( worker )
            # 按照 juli 从小到大排序
            sort_paypal = sorted( enumerate( juli ), key=lambda x: x[1] )
            idx = [x[0] for x in sort_paypal]
            temp_budget = 0
            count = 0
            temp_dis = 0
            for idxx in idx:
                temp_budget = temp_budget + paypal[idxx]
                if temp_budget <= budget:
                    count += 1
                    temp_dis += juli[idxx]
                else:
                    break
                if count == need_people_max:
                    break

            # 计算任务完成率
            if count < need_people_min: # 小于最小值
                f_i = 0
                global_finish.append( 0 )
                global_dis.append( sys.maxsize )
                participant_profile_change_refer.append(participant_profile_temp_2)
            elif count >= need_people_min and count <= need_people_max:  # 刚好在区间范围内
                f_i = count
                if need_people_max == need_people_min:
                    temp_finish = (f_i / need_people_max) * 2
                    global_dis.append( temp_dis )
                else:
                    temp_finish = 1 + (f_i - need_people_min) / (need_people_max - need_people_min)
                    global_dis.append( temp_dis )
                global_finish.append( temp_finish )
                temp_profile = change_profile(idx[:f_i],participant_profile_temp_2,participant_profile_temp_refer)
                participant_profile_change_refer.append(temp_profile)
        not_equall_zero = [x for x in global_finish if x != 0]
        not_equall_max = [x for x in global_dis if x != sys.maxsize]
        if len( not_equall_zero ) == 0 or len( not_equall_max ) == 0: # 如果不能再次分配了 就结束
            break

        sort_dis2 = sorted( enumerate( global_dis ), key=lambda x: x[1] )
        idxu = [idx[0] for idx in sort_dis2]
        finish_rate = finish_rate + global_finish[idxu[0]]
        #  ------------------计算综合效用-------------------------------------------------
        global_task_loss_rate = [2-bl for bl in global_finish]
        max_loss_rate = max(global_task_loss_rate)
        min_loss_rate = min(global_task_loss_rate)
        max_dis = max( not_equall_max )
        min_dis = min( not_equall_max )
        if max_loss_rate == min_loss_rate:
            lin_loss_rate = 0
        else:
            lin_loss_rate = (global_finish[idxu[0]]-min_loss_rate)/(max_loss_rate-min_loss_rate)
        if max_dis == min_dis:
            lin_dis = 0
        else:
            lin_dis = (global_dis[idxu[0]]-min_dis)/(max_dis-min_dis)
        temp_utility = config.alpha*lin_loss_rate + (1-config.alpha)*lin_dis
        utility = utility + temp_utility
        # ----------------------------------------------------------------------------------
        # print( f"当前分配的任务是{resTask[idxu[0]]}" )
        # print( f"本次分配后增加的任务完成率是{global_finish[idxu[0]]}" )
        distance = distance + global_dis[idxu[0]]
        # print( f"本次分配后增加的移动距离是{global_dis[idxu[0]]}" )
        haved_accomplish += 1
        participant_profile_temp = copy.deepcopy(participant_profile_change_refer[idxu[0]])
        resTask.remove( resTask[idxu[0]] )
        # print( f"当前的任务完成率是{finish_rate},移动距离是{distance},已完成的任务数量是{haved_accomplish}" )
    return finish_rate, distance,utility, haved_accomplish


if __name__ == '__main__':
    filename = 'newdata_d100data_start_with_sensor/6501.json'
    filename2 = 'newdata_d100data_end_with_task/6501.txt'
    GF, JL, TN = allocate_by_first_distance( filename, filename2 )
    print( "-" * 20 )
    print( GF, JL, TN )
