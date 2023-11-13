# -*- coding: utf-8 -*-

"""
将感知任务分配给参与者，实现任务完成率最大的同时实现总移动距离最小
"""
import collections
import json
import copy
import math
import sys
import config

def getDistance(lat1, lng1, lat2, lng2):
    """
    依据经纬度计算两点之间的直线距离
    :param lat1: 点1纬度
    :param lng1: 点1经度
    :param lat2: 点2纬度
    :param lng2: 点2经度
    :return: 两点之间的直线距离，单位为km
    """
    EARTH_REDIUS = 6378.137
    lat1 = float(lat1)
    lng1 = float(lng1)
    lat2 = float(lat2)
    lng2 = float(lng2)
    def rad(d):
        return d * math.pi / 180.0

    radLat1 = rad( lat1 )
    radLat2 = rad( lat2 )
    a = radLat1 - radLat2
    b = rad( lng1 ) - rad( lng2 )
    s = 2 * math.asin( math.sqrt(
        math.pow( math.sin( a / 2 ), 2 ) + math.cos( radLat1 ) * math.cos( radLat2 ) * math.pow( math.sin( b / 2 ),
                                                                                                 2 ) ) )
    s = s * EARTH_REDIUS
    return s




def plan_of_exec_sequence(p_profile,Tid,allTask):

    # 整合各个点的位置和时间信息
    # allPoint 的结构为  第0个位置表示参与者概貌的位置时间信息，第1-len(Tid)表示任务集合中各个任务的位置时间信息
    allPoint = [p_profile[0]]  #将p_profile的经纬度、时间取出
    for i in range(len(Tid)):
        allPoint.append(allTask[str(Tid[i])][0][0:3])

    def relax_degree_calcute(now_ponit,res_point,point_info,now_time,distance):
        """
        #计算剩余结点的松弛度
        :param now_ponit: 当前所在结点的概貌
        :param res_point: 还未确定顺序结点的概貌
        :param distance:  还未确定顺序的结点与当前结点之间的距离
        :return: 还未确定顺序的节点的松弛度
        """

        v = 2  # 2m/s 一个成年人正常行走的速度在1.75-2m/s不等

        relax_temp = [0 for i in range(len(res_point))]
        # now_time = int(point_info[now_ponit][2])
        for ri in range(len(res_point)):
            task_deadline = int(point_info[res_point[ri]][2])
            # 因为使用的数据集是采用出租车接送乘客的位置信息，因此任务点之间的距离可能十分大，正常人的移动短时间内无法到达，因此在模拟仿真的过程中将彼此之间的距离缩短10倍
            move_time = distance[res_point[ri]]*1000/v
            relax_temp[ri] = task_deadline - move_time - now_time
        return relax_temp

    v=2  # 2m/s 一个成年人正常行走的速度在1.75-2m/s不等
    # 计算优先顺序 松弛度-距离
    shunxu = []
    juli = 0
    # participantjingwei = p_profile[0]
    dis= [[0 for i in range(len(allPoint))] for j in range(len(allPoint))] # 保存参与者和各个任务结点的距离
    for i in range(len(allPoint)):
        for j  in range(len(allPoint)):
            dis[i][j] = getDistance(allPoint[i][0],allPoint[i][1],allPoint[j][0],allPoint[j][1])

    resid = [ i for i in range(1,len(Tid)+1)] #Tid重新编号
    the_now_ponit_id = 0  #表示当前结点为参与组合所在的位置上
    the_now_time = int(allPoint[the_now_ponit_id][2])
    # 计算返回resid中的节点对当前结点的松弛度
    relax_degree = relax_degree_calcute(the_now_ponit_id,resid,allPoint,the_now_time,dis[0])
    the_candidate_point_id = resid[relax_degree.index(min(relax_degree))]
    # candidate_point  = allTask[str[resid[the_first_point_id]]]
    while len(resid)>0:
        #找到剩余点中距离当前点最近的结点
        dis_x = [dis[the_now_ponit_id][i] for i in resid]
        dis_x_id = dis_x.index(min(dis_x))
        temp_point_id = resid[dis_x_id]
        # temp_point_id = dis[the_now_ponit_id].index(min([dis[the_now_ponit_id][i] for i in resid]))
        # print(f"temp_point_id is {temp_point_id}")
        if temp_point_id == the_candidate_point_id:
            # 此种情况下，最紧迫的任务点也是离得最近的任务点，更新当前节点的位置和时间
            shunxu.append(temp_point_id)
            resid.remove(temp_point_id)
            the_now_time = int(allPoint[the_now_ponit_id][2])+dis[the_now_ponit_id][temp_point_id]*1000/v
            juli = juli + dis[the_now_ponit_id][temp_point_id]
            the_now_ponit_id = temp_point_id
            if len(resid)!=0:
                relax_degree = relax_degree_calcute(the_now_ponit_id,resid,allPoint,the_now_time,dis[the_now_ponit_id])
                the_candidate_point_id = resid[relax_degree.index( min( relax_degree ) )]
            else:
                break
        else:
            if temp_point_id == 0:
                input("等于0了")
            temp_point_idd = resid.index(temp_point_id)  # temp结点的松弛度索引
            now2temp_relax_degree = relax_degree[temp_point_idd]  # temp结点对于当前结点的松弛度
            temp2_candidate_move_time = dis[temp_point_id][the_candidate_point_id]*1000/v   # 从temp结点移动到candidate结点的时间
            the_candidate_point_deadline = int(allPoint[the_candidate_point_id][2]) # 候选节点的任务截止时间
            # the_temp_now_time= allPoint[temp_point_id][2]   #当前时间需要重新计算一下 写的不对 应该是从前一个位置出发的时间加上移动时间
            # the_temp_now_time = int(allPoint[the_now_ponit_id][2])+dis[the_now_ponit_id][temp_point_id]*1000/v
            the_temp_now_time = the_now_time + dis[the_now_ponit_id][temp_point_id] * 1000 / v # 假设参与者先从当前结点旅行至temp结点，则到达temp结点时的时间
            temp2candidate_relax_degree = the_candidate_point_deadline - temp2_candidate_move_time - the_temp_now_time # candidate结点对于temp结点的松弛度

            # 如果 将temp结点添加到当前结点中间后，满足：
            #       1: 当前结点经过temp到达candidate结点的距离 小于 当前结点经过candidate结点到达temp结点的距离
            #       2: 松弛度大于0，即能在任务截止前到达
            #           2.1 temp结点对于当前结点的松弛度>0
            #           2.2 candidate结点对于temp结点的松弛度>0
            if dis[the_now_ponit_id][temp_point_id] + dis[temp_point_id][the_candidate_point_id] <= dis[the_now_ponit_id][the_candidate_point_id]+dis[the_candidate_point_id][temp_point_id] and \
                    (now2temp_relax_degree>0 and temp2candidate_relax_degree>0):
                # 如果满足条件 ，则将temp加入shunxu队列
                shunxu.append(temp_point_id)
                # 将当前结点到temp结点的移动距离加入总得移动距离
                juli = juli + dis[the_now_ponit_id][temp_point_id]
                # 并将其从待安排列表中删除
                resid.remove(temp_point_id)
                # 则当前结点更新为temp结点
                the_now_ponit_id = temp_point_id
                # 当前时间更新为参与者到达temp结点的时间
                the_now_time = the_temp_now_time
                # 当前结点更换，计算以当前结点再次计算松弛度，选择最紧迫需要被执行的点（任务）
                relax_degree = relax_degree_calcute( the_now_ponit_id, resid, allPoint, the_now_time,
                                                     dis[the_now_ponit_id] )
            else:
                # 若不满足条件，则说明候candidate结点时最合适的结点，应当被先执行
                # 将candidate结点接入shunxu队列
                shunxu.append(the_candidate_point_id)
                # 将从当前结点移动到candidate结点的距离加入总移动距离
                juli = juli + dis[the_now_ponit_id][the_candidate_point_id]
                # 将当前时间更新为当前结点到达candidate时的时间
                the_now_time = the_now_time + dis[the_now_ponit_id][the_candidate_point_id]*1000/v
                # 将当前结点更新为candidate
                the_now_ponit_id = the_candidate_point_id
                resid.remove( the_candidate_point_id )
                # candidate结点时当前最紧迫需要去执行的任务，现在已经将candidate结点安排好了（即将candidate更新为当前结点），
                # 那么需要依据当前结点再次计算松弛度，选择最紧迫需要被执行的点（任务）
                relax_degree = relax_degree_calcute(the_now_ponit_id,resid,allPoint,the_now_time,dis[the_now_ponit_id])
                the_candidate_point_id = resid[relax_degree.index(min(relax_degree))]

    last_id = shunxu[-1]
    time_after_exec = the_now_time
    location_after_exec =  allPoint[last_id][0:2]
    shunxu= [Tid[q-1] for q in shunxu ]
    return shunxu,juli,time_after_exec,location_after_exec


def verify_execution_capability(participant_sensor,practical_task_sensor):
    """
    验证参与者是否具有完成任务集合的能力
    :param participant_sensor: 参与者的传感器情况：[传感器类型，传感器期望报酬，传感器负载】
    :param practical_task_sensor: 任务的传感器情况{传感器类型:所需数目,传感器类型：所需数目}
    :return: True or False
    """
    flag = True
    p_sensor_type_list = [x[0] for x in participant_sensor if x[1]!=sys.maxsize]
    t_sensor_type_list = list(practical_task_sensor.keys())
    for pts in t_sensor_type_list:
        if pts in p_sensor_type_list:
            sensor_index = p_sensor_type_list.index(pts)
            # 如果参与者这项传感器的负载大于任务所需的数量，则继续判断
            if participant_sensor[sensor_index][2]>=practical_task_sensor[pts]:
                # participant_sensor[sensor_index] = participant_sensor[sensor_index] -  practical_task_sensor[pts]
                continue
            else:
                flag = False
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



def allocate(filename,filename2):
    # 载入数据

    # -- 参与者数据
    with open(filename,'r',encoding='utf-8') as f:
        participant = json.load(f)

    # -- 感知任务数据
    with open(filename2,'r',encoding='utf-8') as f:
        Task = json.load(f)
    # task存储样例： {"0": [["37.80113", "-122.42468", "1212598532", "-1"], [8, 9, 4, 7, 11], 30, [2, 5]],
    #将相同类的感知任务放在一起
    classmax = int(max(Task.values(),key=lambda a:int(a[0][3]))[0][3])+1 #非-1类的个数
    per_class_id = [[] for i in range(classmax)]
    # 将类别标签为-1的单独归为一类
    TaskLen = len( Task )

    for i in range(TaskLen):
        classType = int(Task[str(i)][0][3])
        if classType==-1:
            per_class_id.append([i])
            Task[str(i)][0][3] = classmax
            classmax = classmax + 1
        else:
            per_class_id[classType].append(i)

    # 在所有的任务中选择任务完成率和移动距离作为综合效用最大的一个任务分配

    # 表示还未被分配参与者的任务集合,刚开始还未分配的任务是所有的任务
    resTASK = list( range( TaskLen ) )
    participant_profile_temp = copy.deepcopy(participant)  # 用来描述参与者与任务的匹配后的参与者的概貌变化
    TFR = 0
    TPD = 0
    TPU = 0
    haved_allocated_task_num = 0
    while len(resTASK)>0:
        # 表示在某轮迭代中还没分配的任务
        resTASK2 = copy.deepcopy(resTASK)
        participant_profile_change_refer = []
        global_finish_rate = []
        global_distance = []
        global_task_loss_rate= []
        utility= []
        avg_global_task_loss_rate = []
        # 尝试的任务顺序
        seq_of_attempted_tasks = []
        for i in range(TaskLen):
            if i not in resTASK:
                # 如果任务已经分配了，则跳过执行下一个
                continue
            else:
                if i not in resTASK2:
                    # 尝试遍历每一个任务进行分配，如果在当前遍历过程中，已经对其做出安排，主要是指同一类的任务被同时分配的情况
                    continue

            participant_profile_temp_2 = copy.deepcopy(participant_profile_temp)
            # 获取当前任务的类型，并从per_class_id中获取该类型所有任务的id
            taskid = per_class_id[int(Task[str(i)][0][3])]
            seq_of_attempted_tasks.append(taskid)
            # 如果这个任务所在类中的任务数量>1
            if(len(taskid)>1):
                # 将 此类中所有任务的预算合并
                budget = 0
                # 各个任务所需的传感器取并集
                need_sensor = set()
                # 取每个任务所需最小参与者人数的最大值作为任务集合所需的最少参与者人数
                need_participant_min = 0
                need_participant_max = 0
                need_sensor_all = []
                # 对于任务集合中的每个任务
                for tid in taskid:
                    budget = budget + Task[str(tid)][2]
                    dangqian_task_sensor = Task[str(tid)][1]
                    need_sensor_all = need_sensor_all + dangqian_task_sensor
                    need_sensor = need_sensor.union(set(dangqian_task_sensor))
                    need_participant_min = max(need_participant_min,Task[str(tid)][3][0])
                    need_participant_max = max(need_participant_max,Task[str(tid)][3][1])
                participantLen = len(participant_profile_temp_2)
                need_sensor_num = collections.Counter(need_sensor_all) # 该任务集合需要各种传感器的数量
                paypal = []  # 用来记录每个参与者要完成该任务所需的报酬
                participant_profile_temp_refer = [] # 用来记录参与者完成某个任务后，状态的变化
                total_dis_temp = [] # 用来记录每个参与者完成该任务集合的移动距离
                for pid in range(participantLen):
                    paypal_temp=0
                    # 因为在任务临时分配的过程中改变参与者的某些值，因此将其copy一份，使其不影响原值
                    worker = copy.deepcopy(participant_profile_temp_2[str(pid)])
                    # 如果任务中包含参与者不具备的传感器，则该参与者不能执行此任务（这个策略还需要改进，可能会有很多参与者因此不能执行此任务）
                    sensor_p = set([s[0] for s in worker[1]])
                    can_exec_s = need_sensor.issubset(sensor_p)  # 在类型上判断能否执行
                    can_exec_n = verify_execution_capability(worker[1],need_sensor_num)   # 判断负载是否满足任务要求
                    # 如果类型和数量均满足执行条件
                    if can_exec_s and can_exec_n:
                        # 规划执行顺序
                        panticipant_exec_shunxu,juli,the_time_after_exec,location_after_exec  = plan_of_exec_sequence(worker,taskid,Task)
                        # 按照顺序模拟执行过程（支付报酬和移动距离）
                        sensor_used_flag = [0 for suf in range(len(worker[1]))]
                        for shunxuid  in panticipant_exec_shunxu:
                            # 从顺序列表中取出任务id ，并获得该任务的传感器描述
                            taskt = Task[str(shunxuid)][1]
                            for taskt_sensor in taskt: # 对于该任务所需的每一个传感器
                                for p_sensor_id in range(len(worker[1])): # 找到参与者与任务匹配的传感器
                                    if taskt_sensor == worker[1][p_sensor_id][0]:
                                        if worker[1][p_sensor_id][1] != 0 and sensor_used_flag[p_sensor_id] == 0:
                                            # 如果该传感器期望报酬不为0，并且在此任何集合中没被使用的话
                                            paypal_temp = paypal_temp + worker[1][p_sensor_id][1]
                                            sensor_used_flag[p_sensor_id] = 1
                                        else:
                                            paypal_temp = paypal_temp + 1
                                        # 将使用了的传感的负载减一
                                        worker[1][p_sensor_id][2] = worker[1][p_sensor_id][2] - 1
                                        # 匹配上后就跳出对参与者传感器的遍历，开始下一个任务要求的传感器
                                        break
                        paypal_temp = paypal_temp + 2*juli  # 总得支付报酬为传感器报酬加上距离报酬
                        paypal.append(paypal_temp)
                        total_dis_temp.append(juli)
                        # 参与者执行结束，更新位置及时间信息
                        worker[0][2] = the_time_after_exec
                        worker[0][0] = location_after_exec[0]
                        worker[0][1] = location_after_exec[1]
                    else:
                        paypal.append(sys.maxsize)
                        total_dis_temp.append(sys.maxsize)  # 如果参与者不能执行任务，将其移动距离置为最大值
                    participant_profile_temp_refer.append(worker)
                # 在所有的参与者中选出执行该任务集合的参与者
                sorted_paypal = sorted(enumerate(paypal),key=lambda x:x[1])  # 将 paypal从小到大排序
                idx = [i[0] for i in sorted_paypal]
                count = 0
                expenditure_budget = 0
                for selectid in idx:
                    if expenditure_budget + paypal[selectid] <= budget:
                        count = count + 1
                        expenditure_budget = expenditure_budget+paypal[selectid]
                    else:
                        break
                    if count >= need_participant_max:
                        break
                finish_rate = 0
                task_loss_rate = len(taskid) * 2  # 完成率分为两部分 基础 + 增益
                if count>=need_participant_min:
                    # 如果达到最小所需人数，那么就是一次合理的分配，则更新执行该任务的参与者改名
                    change_profile_temp = change_profile( idx[:count], participant_profile_temp_2,
                                                              participant_profile_temp_refer )
                    participant_profile_change_refer.append( change_profile_temp )
                    total_dis = sum([total_dis_temp[dd] for dd in idx[:count]])
                    global_distance.append(total_dis)
                    # 计算此时该任务集合任务完成率
                    for tid in taskid:
                        min_num = Task[str( tid )][3][0]
                        max_num = Task[str( tid )][3][1]
                        if min_num == max_num:
                            # 如果该任务的最少参与者人数和最多参与者人数相等（换句话说该任务没有那么严格）
                            if count < min_num:
                                # 则有效任务数量为0，该任务的任务完成率也为0
                                f_i = count
                            else:
                                f_i = min_num
                                finish_rate = (finish_rate + (f_i/min_num)*2)
                        else:
                            if count < min_num:
                                f_i = 0
                            else:
                                if count >= min_num and count < max_num:
                                    f_i = count
                                else:
                                    f_i = max_num
                                finish_rate = finish_rate + 1 + (f_i - min_num) * 1.0 / (max_num - min_num)
                    # 任务能够被参与者完成，则将这些任务从待分配列表中删除
                    for tid in taskid:
                        if tid not in  resTASK2:
                            input()
                        resTASK2.remove(tid)
                else:
                    # 如果不满足任务人数要求，就不改变参与者概貌
                    participant_profile_change_refer.append( participant_profile_temp_2 )
                    global_distance.append(sys.maxsize)
                    finish_rate = 0
                    # 不满任务人数要求，那么相应的不安排参与者去执行该任务，则该任务的任务完成率为0
                task_loss_rate = task_loss_rate - finish_rate
                if task_loss_rate<0:
                    input()
                global_finish_rate.append(finish_rate)
                global_task_loss_rate.append(task_loss_rate)
                avg_task_loss_rate = task_loss_rate*1.0/(2*len(taskid))
                avg_global_task_loss_rate.append(avg_task_loss_rate)
            # 如果这个任务所在的类中任务数量只有一项
            else:
                need_sensor = set(Task[str(taskid[0])][1])
                budget = int(Task[str(taskid[0])][2])
                need_participant_min = Task[str(taskid[0])][3][0]  # 只有一个任务，则此时该任务的最少或最多需要的参与者人数就是集合的
                need_participant_max = Task[str(taskid[0])][3][1]
                participantLen = len( participant )  # 参与者人数
                need_sensor_num = collections.Counter( need_sensor )
                paypal = []
                participant_profile_temp_refer = []
                total_dis_temp=[]
                for pid in range( participantLen ):
                    worker = copy.deepcopy( participant_profile_temp_2[str(pid)] )
                    # 如果任务中包含参与者不具备的传感器，则该参与者不能执行此任务（这个策略还需要改进，可能会有很多参与者因此不能执行此任务）
                    sensor_p = set( [s[0] for s in worker[1] if s[1]!=sys.maxsize])
                    can_exec_s = need_sensor.issubset( sensor_p )  # 在类型上判断能否执行
                    paypal_temp = 0
                    can_exec_n = verify_execution_capability(worker[1],need_sensor_num)
                    if can_exec_s and can_exec_n:
                        taskt = Task[str( taskid[0] )][1]
                        for taskt_sensor in taskt:
                            for p_sensor_id in range( len( worker[1] ) ):
                                if taskt_sensor == worker[1][p_sensor_id][0]:
                                    if worker[1][p_sensor_id][1] != 0:
                                        paypal_temp = paypal_temp + worker[1][p_sensor_id][1]
                                    else:
                                        paypal_temp = paypal_temp + 1
                                    worker[1][p_sensor_id][2] = worker[1][p_sensor_id][2] - 1
                                    break
                        juli = getDistance(Task[str(taskid[0])][0][0],Task[str(taskid[0])][0][1],worker[0][0],worker[0][1])
                        paypal_temp = paypal_temp + 2*juli
                        the_time_after_exec = int(worker[0][2]) + int(juli*1000/config.v)  #因为利用的是出租车的位置信息，将距离缩短10倍
                        worker[0][2] = the_time_after_exec
                        worker[0][0] = Task[str(taskid[0])][0][0]
                        worker[0][1] = Task[str(taskid[0])][0][1]
                        paypal.append(paypal_temp)
                        total_dis_temp.append( juli )
                    else:
                        paypal.append(sys.maxsize)
                        total_dis_temp.append((sys.maxsize))
                    participant_profile_temp_refer.append( worker )
                # 选择
                sorted_paypal = sorted( enumerate( paypal ), key=lambda x: x[1] )  # 将 paypal从小到大排序
                idx = [i[0] for i in sorted_paypal] #对应原来的位置
                count = 0
                expenditure_budget = 0
                for selectid in idx:
                    if expenditure_budget+paypal[selectid] <= budget:
                        count = count + 1
                        expenditure_budget = expenditure_budget + paypal[selectid]
                    else:
                        break
                    if count>=need_participant_max:
                        break
                #计算任务的完成率
                if count<need_participant_min:
                    f_i = 0
                    participant_profile_change_refer.append( participant_profile_temp_2 )
                    global_distance.append(sys.maxsize)
                elif count>=need_participant_min and count <need_participant_max:
                    f_i = count
                    change_profile_temp = change_profile( idx[:f_i], participant_profile_temp_2,
                                                          participant_profile_temp_refer )
                    participant_profile_change_refer.append( change_profile_temp )
                    total_dis = sum( [total_dis_temp[dd] for dd in idx[:f_i]] )
                    global_distance.append( total_dis )
                    # resTASK2.remove(taskid[0])
                else:
                    f_i = need_participant_max
                    change_profile_temp = change_profile( idx[:f_i], participant_profile_temp_2,
                                                          participant_profile_temp_refer )
                    participant_profile_change_refer.append( change_profile_temp )
                    total_dis = sum( [total_dis_temp[dd] for dd in idx[:f_i]] )
                    global_distance.append( total_dis )

                # finish_rate =  (f_i-need_participant_min)/(need_participant_max-need_participant_min)
                if need_participant_max == need_participant_min:
                    finish_rate = (f_i/need_participant_min)*2
                else:
                    finish_rate = 0 if f_i == 0 else (
                                1 + (f_i - need_participant_min) / (need_participant_max - need_participant_min))
                task_loss_rate = 2 - finish_rate
                if task_loss_rate < 0:
                    input()
                global_finish_rate.append(finish_rate)
                global_task_loss_rate.append(task_loss_rate)
                avg_task_loss_rate = task_loss_rate * 1.0 / len( taskid )
                avg_global_task_loss_rate.append( avg_task_loss_rate )
                resTASK2.remove( taskid[0] )
            # print(f"当前任务完成率{finish_rate}")

        # 将所有的任务完成率归一化，移动距离归一化，做权重和计算总的效用。
        loss_rate_max = max(global_task_loss_rate)
        loss_rate_min = min(global_task_loss_rate)
        tttt = [maxd for maxd in global_distance if maxd != sys.maxsize]
        cccc = [mind for mind in global_finish_rate if mind != 0]
        if len(tttt)==0 or len(cccc)==0:
            # 若为global_distance钟均为最大值，则说明剩余的任务没有任何参与者能去完成
            # 若global_distance均为0，则说明，剩余任何一个任务都不能被完成
            break
        dis_max = max(tttt)  # 不考虑哪些没被分配到任务的参与者
        dis_min = min([mind for mind in global_distance if  mind !=sys.maxsize])   # 不考虑哪些没被分配到任务的参与者
        avg_lossrate_max=max(avg_global_task_loss_rate)
        avg_lossrate_min = min(avg_global_task_loss_rate)
        gui_global_distance = copy.deepcopy(global_distance)
        gui_global_task_loss_rate = copy.deepcopy(global_task_loss_rate)
        gui_avg_global_task_loss_rate = copy.deepcopy(avg_global_task_loss_rate)
        for gui in range(len(global_task_loss_rate)):
            gui_global_task_loss_rate[gui] = (global_task_loss_rate[gui] - loss_rate_min) / (loss_rate_max - loss_rate_min)
            gui_avg_global_task_loss_rate[gui] = (avg_global_task_loss_rate[gui]-avg_lossrate_min)/(avg_lossrate_max-avg_lossrate_min)
            if global_distance[gui]<sys.maxsize:
                if dis_max==dis_min:
                    # 如果最大值等于最小值，则说明其中可能只存在一种值，此时，将所有非最大值的元素设置为1
                    gui_global_distance[gui] = 0
                else:
                    gui_global_distance[gui] = (global_distance[gui] - dis_min) / (dis_max - dis_min)
        for i in range(len(global_task_loss_rate)):
            if global_finish_rate[i] == 0:
                utility_temp = sys.maxsize
            else:
                utility_temp = config.alpha * gui_avg_global_task_loss_rate[i] + (1-config.alpha) * gui_global_distance[i]
            utility.append(utility_temp)
        sorted_utility = sorted( enumerate( utility ), key=lambda x: x[1] )  # 将 paypal从小到大排序
        idxu = [i[0] for i in sorted_utility]
        # allocaed_task_id = resTASK[idxu[0]]
        # 寻找效用最小的，因为目标是最小化。并且如果任务的完成率为0的话，则跳过
        for suif in idxu:
            if global_finish_rate[suif] != 0 and gui_global_distance[suif]!=sys.maxsize:
                smallest_utility_in_fact = suif
                break
        haved_allocated_task_num = haved_allocated_task_num + len( seq_of_attempted_tasks[smallest_utility_in_fact] )

        # try:
        #     print(f"本轮分配中的第{smallest_utility_in_fact}个")
        #     print(f"实际分配任务id为{seq_of_attempted_tasks[smallest_utility_in_fact]}")
        #     print(f"本次完成任务后增加的任务完成率是{global_finish_rate[smallest_utility_in_fact]}")
        #     print(f"本次完成任务的移动距离是{global_distance[smallest_utility_in_fact]}")
        #     print(f"已经分配的任务数量{haved_allocated_task_num}")
        # except NameError:
        #     print("任务完成率全部为0")

        for allocaed_task_id in seq_of_attempted_tasks[smallest_utility_in_fact]:
            resTASK.remove(allocaed_task_id)
        # 根据分配结果更新参与者信息
        participant_profile_temp = copy.deepcopy(participant_profile_change_refer[smallest_utility_in_fact])
        TFR = TFR + global_finish_rate[smallest_utility_in_fact]
        TPD = TPD + global_distance[smallest_utility_in_fact]
        TPU = TPU + utility[smallest_utility_in_fact]
        # print(f"当前任务完成率为{TFR},移动距离为{TPD},综合效用为{TPU}")
    return TFR,TPD,TPU,haved_allocated_task_num
    return TFR,TPD,TPU,haved_allocated_task_num

if __name__ == "__main__":
    print( 6501 )
    filename = 'newdata_d100data_start_with_sensor/6502_1.json'
    # filename = 'd100data_start_with_sensor/6502.json'
    # filename2 = 'newdata_d100data_end_with_task/6501_1.json'
    filename2 = 'ddd_d100data_end_with_task/6502.txt'
    # filename2 = 'ddd_d100data_end_with_task/6502_1.json'
    # filename2 = 'ddd_d100data_end_with_task/6617.txt'
    tfr,tpd,tpu,aclocated_task_num = allocate(filename,filename2)
    print("-"*20)
    print(tfr,tpd,tpu,aclocated_task_num)






