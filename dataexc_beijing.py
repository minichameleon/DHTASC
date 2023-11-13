# -*- coding: utf-8 -*-

"""
提取北京出租车形式轨迹信息
随机选择300辆出租车信息
然后在一天的行驶当中随机采集两个点，一个点作为感知任务所在位置，一个作为参与者的位置
"""
import random
import time
import json
import pathlib

import config
from genParticipant import genParticipant
from genTask_new import genTask
from random_gen_data import genData_task, genData_participant
from specifiesSizeOfCluster import specifiesSizeOfCluster, getNumPerClass

carnums = 10357

carid = list(range(1,carnums+1))


# 随机选择300辆出租车
# 并按小时对其进行划分
# 2008-02-03 00:00:00        1201968000

# 2008-02-08 00:00:00        1202400000
#
s_carid = random.sample(carid,carnums)
carlist = []

#
# # 随机选择100辆出租车,按照时间段划分（一小时）
#
for day in range(3,8):
    for hour in range(0,24):
        if hour<10:
            fileid = '2'+str(day)+'0'+str(hour)
            nowtime = '2008-02-0'+str(day)+' 0'+str(hour)+':00:00'
        else:
            fileid = '2'+str(day)+str(hour)
            nowtime = '2008-02-0' + str( day ) + ' ' + str( hour ) + ':00:00'
        # print(fileid)
        # print(nowtime)
        s_t = time.strptime( nowtime, "%Y-%m-%d %H:%M:%S" )
        mkt = int( time.mktime( s_t ) )
        Task = {}
        Participant = {}
        index = 1
        for i in s_carid:
            if index>100:
                break
            add = 'C:\\Users\\s-monster\\Desktop\\T-drive Taxi Trajectories\\release\\taxi_log_2008_by_id\\'+str(i)+'.txt'
            with open(add,'r',encoding='utf-8') as f:
                lines = f.readlines()
                candicate = []
                for line in lines:
                    line = line.strip().split(',')
                    tt_s_t = time.strptime(line[1],"%Y-%m-%d %H:%M:%S")
                    tt_mkt = int(time.mktime(tt_s_t))
                    if  tt_mkt>=mkt and tt_mkt<mkt+3600:
                        candicate.append([line[2],line[3],tt_mkt])
                length = len(candicate)
                if length<6:
                    continue
                carlist.append(i)
                participantsuiji = list(range(0,length//2))
                tasksuiji = list(range(length//2,length))
                tsuijiid = random.sample(tasksuiji,3)
                psuijiid = random.sample(participantsuiji,3)
                # taskid = suijiid[0:3]
                # workerid = suijiid[3:6]
                Task[str((index-1)*3)] = candicate[tsuijiid[0]]
                Task[str( (index - 1) * 3 +1)] = candicate[tsuijiid[1]]
                Task[str( (index - 1) * 3 +2)] = candicate[tsuijiid[2]]
                # Task[str(index)]=candicate[maxid]
                Participant[str((index-1)*3)] = candicate[psuijiid[0]]
                Participant[str( (index - 1) * 3 + 1 )] = candicate[psuijiid[1]]
                Participant[str( (index - 1) * 3 + 2 )] = candicate[psuijiid[2]]
                # Participant[str(index)]=candicate[minid]
                index = index + 1

        filepath_task = 'T-drive_beijing/location_data/task/' + fileid + '.json'
        filepath_participant = 'T-drive_beijing/location_data/participant/' + fileid + '.json'
        with open(filepath_task,'a',encoding='utf-8') as f:
            json.dump(Task,f)
        with open(filepath_participant,'a',encoding='utf-8') as f:
            json.dump(Participant,f)

print(carlist)

# 为每个小时的任务生成任务描述
for bai in range( 23, 28 ):
    for ge in range( 0, 24 ):
        if ge <= 9:
            # task
            addr = 'T-drive_beijing/location_data/task/' + str( bai ) + '0' + str( ge ) + '.json'
            writename1 = 'T-drive_beijing/d100data_end_with_task/' + str( bai ) + '0' + str( ge ) + '.json'
            # partcipant
            addr2 = 'T-drive_beijing/location_data/participant/' + str( bai ) + '0' + str( ge ) + '.json'
            writename2 = 'T-drive_beijing/d100data_start_with_sensor/' + str( bai ) + '0' + str( ge ) + '.json'
            timestamp = str( bai ) + '0' + str( ge )
        else:
            # task
            addr = 'T-drive_beijing/location_data/task/' + str( bai ) + str( ge ) + '.json'
            writename1 = 'T-drive_beijing/d100data_end_with_task/' + str( bai ) + str( ge ) + '.json'
            # participant
            addr2 = 'T-drive_beijing/location_data/participant/' + str( bai ) + str( ge ) + '.json'
            writename2 = 'T-drive_beijing/d100data_start_with_sensor/' + str( bai ) + str( ge ) + '.json'
            timestamp = str( bai ) + str( ge )
        # 如果构造的文件路径不存在，在继续下一个
        filepathx = pathlib.Path( addr )
        if not filepathx.exists( ):
            continue

        # addr = 'd100data_end\\6501.txt'
        TASK = genTask( addr,1 )
        PARTICIPANT = genParticipant(addr2,timestamp,1)
        nums = len( TASK )
        for i in range( nums ):
            print( TASK[str( i )] )
        print('--'*20)
        for i in range( nums ):
            print( PARTICIPANT[str( i )] )
        with open( writename1, 'w', encoding='utf-8' ) as wf2:
            json.dump( TASK, wf2 )
        with open(writename2,'w',encoding='utf-8') as wf3:
            json.dump(PARTICIPANT,wf3)

#-----------------------------------------------------------------------------------

for bai in range( 23, 28 ):
    for ge in range( 0, 24 ):
        if ge <= 9:
            # task
            addr = 'T-drive_beijing/d100data_end_with_task/' + str( bai ) + '0' + str( ge ) + '.json'
            writename1 = 'T-drive_beijing/d100data_end_with_task/' + str( bai ) + '0' + str( ge ) + '.txt' # 聚类
            # writename1 = 'T-drive_beijing/d100data_end_with_task/' + str( bai ) + '0' + str( ge ) + '_1.json' #不聚类

        else:
            # task
            addr = 'T-drive_beijing/d100data_end_with_task/' + str( bai ) + str( ge ) + '.json'
            writename1 = 'T-drive_beijing/d100data_end_with_task/' + str( bai ) + str( ge ) + '.txt'  # 聚类
            # writename1 = 'T-drive_beijing/d100data_end_with_task/' + str( bai ) + str( ge ) + '_1.json'  # 不聚类

        # 如果构造的文件路径不存在，在继续下一个
        filepathx = pathlib.Path( addr )
        if not filepathx.exists( ):
            continue

        # addr = 'd100data_end/6501.txt'
        clusterRes = specifiesSizeOfCluster( addr, addr, 0.3, 3, 5, 1 )
        ress = getNumPerClass( clusterRes )
        with open( addr, 'r', encoding='utf-8' ) as f:
            TASK1 = json.load( f )
        for t in range( len( TASK1 ) ):
            TASK1[str( t )][0].append( str( clusterRes[t] ) )
            # TASK1[str( t )][0].append( str( t))
        print( ress[0] )
        print( type( TASK1 ) )
        with open( writename1, 'w', encoding='utf-8' ) as wf2:
            json.dump( TASK1, wf2 )

# #
for bai in range( 23, 28 ):
    for ge in range( 0, 24 ):
        if ge <= 9:

            addr1 =  'T-drive_beijing/d100data_end_with_task/' + str( bai ) + '0' + str( ge ) + '.txt'     # 任务概貌（聚类）
            addr2 =  'T-drive_beijing/d100data_end_with_task/' + str( bai ) + '0' + str( ge ) + '_1.json'  # 任务概貌（不聚类）
            writename1 = 'T-drive_beijing/d100data_end_with_task/' + str( bai ) + '0' + str( ge ) + '.txt'   # 任务概貌（聚类）
            writename2 =  'T-drive_beijing/d100data_end_with_task/' + str( bai ) + '0' + str( ge ) + '_1.json'  # 任务概貌（不聚类）
            bianhao = str( bai ) + '0' + str( ge )
        else:
            addr1 = 'T-drive_beijing/d100data_end_with_task/' + str( bai ) + str( ge ) + '.txt'  # 任务概貌（聚类）
            addr2 = 'T-drive_beijing/d100data_end_with_task/' + str( bai ) + str( ge ) + '_1.json'     # 任务概貌（不聚类）
            writename1 = 'T-drive_beijing/d100data_end_with_task/' + str( bai ) + str( ge ) + '.txt'  # 任务概貌（聚类）
            writename2 = 'T-drive_beijing/d100data_end_with_task/' + str( bai ) + str( ge ) + '_1.json'   # 任务概貌（不聚类）

            bianhao = str( bai ) + str( ge )

        filepathx = pathlib.Path( addr1 )
        if not filepathx.exists( ):
            continue
        with open( addr1, 'r', encoding='utf-8' ) as f:
            TASK = json.load( f )
        with open( addr2, 'r', encoding='utf-8' ) as f:
            TASK_no = json.load( f )

        tasklen = len( TASK )
        classnum = int( max( TASK.values( ), key=lambda a: int( a[0][3] ) )[0][3] ) + 1  # 非-1类的个数
        per_class_id = [[] for i in range( classnum )]
        classId = [i for i in range( classnum )]
        for i in range( tasklen ):
            classType = int( TASK[str( i )][0][3] )
            if classType == -1:
                per_class_id.append( [i] )
                # TASK[str( i )][0][3] = classnum
                # classnum = classnum + 1
            else:
                per_class_id[classType].append( i )
        for i in classId:
            task_id_in_class = per_class_id[i]
            shuliang = len( task_id_in_class )
            # 获取同一类的任务概貌
            alltask = [TASK[str( x )] for x in task_id_in_class]
            budget = [alltask[x][2] for x in range( shuliang )]
            max_budget = max( budget )
            max_id = budget.index( max_budget )
            all_trans_budget = 0
            for j in range( shuliang ):
                if max_id == j:
                    # TASK[str( task_id_in_class[j] )][2] = int( TASK[str( task_id_in_class[j] )][2] ) * 4
                    # TASK_no[str( task_id_in_class[j] )][2] = int( TASK_no[str( task_id_in_class[j] )][2] ) * 4
                    continue
                else:
                    trans_budget =  int( TASK[str( task_id_in_class[j] )][2] ) // 2
                    TASK[str( task_id_in_class[j] )][2] = trans_budget
                    TASK_no[str( task_id_in_class[j] )][2] = trans_budget
                    all_trans_budget = all_trans_budget + trans_budget
            suijizengjia = random.randint(config.left_suijiadd,config.right_suijiadd)
            TASK[str( task_id_in_class[max_id] )][2] = all_trans_budget + TASK[str( task_id_in_class[max_id] )][2] +suijizengjia
            TASK_no[str( task_id_in_class[max_id] )][2] = all_trans_budget + TASK[str( task_id_in_class[max_id] )][2] + suijizengjia
        with open( writename1, 'w', encoding='utf-8' ) as f:
            json.dump( TASK, f )

        with open( writename2, 'w', encoding='utf-8' ) as f:
            json.dump( TASK_no, f )

# 改变任务和参与者的数量
for bai in range( 23, 28 ):
    for ge in range( 0, 24 ):
        if ge <= 9:
            addr1 = 'T-drive_beijing/d100data_end_with_task/' + str( bai ) + '0' + str( ge ) + '.txt'  # 任务概貌（聚类）
            addr2 = 'T-drive_beijing/d100data_end_with_task/' + str( bai ) + '0' + str( ge ) + '_1.json'  # 任务概貌（不聚类）
            addr3 = 'T-drive_beijing/d100data_start_with_sensor/' + str( bai ) + '0' + str( ge ) + '.json'  # 任务概貌（不聚类）
        else:
            addr1 = 'T-drive_beijing/d100data_end_with_task/' + str( bai ) + str( ge ) + '.txt'  # 任务概貌（聚类）
            addr2 = 'T-drive_beijing/d100data_end_with_task/' + str( bai ) + str( ge ) + '_1.json'  # 任务概貌（不聚类）
            addr3 = 'T-drive_beijing/d100data_start_with_sensor/' + str( bai ) + str( ge ) + '.json'  # 任务概貌（不聚类）
        for i in range(50,301,50):
            genData_task(addr1,addr2,i)
        for i in range(50,301,50):
            genData_participant(addr3,i)