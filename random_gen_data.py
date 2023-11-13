# -*- coding: utf-8 -*-

"""
随机选择生成指定规模的参与者或者任务集合
"""
import json
import random
def genData_task(filename,filename2,nums):

    # name1 = filename.split('\\')[1]
    # name2 = filename2.split('\\')[1]
    # writename1 = 'change_task_nums\\task_nums_'+str(nums)+"\\"+name1  # 任务概貌（聚类）
    # writename2 = 'change_task_nums\\task_nums_'+str(nums)+"\\"+name2  # 任务概貌（不聚类）

    name1 = filename.split( '/' )[2]
    name2 = filename2.split( '/' )[2]
    writename1 = 'T-drive_beijing/location_data/change_task_nums/task_nums_' + str( nums ) + "/" + name1  # 任务概貌（聚类）
    writename2 = 'T-drive_beijing/location_data/change_task_nums/task_nums_' + str( nums ) + "/" + name2  # 任务概貌（不聚类）
    with open(filename,'r',encoding='utf-8') as f:
        data1 = json.load(f)
    with open(filename2,'r',encoding='utf-8') as f:
        data2 = json.load(f)
    length = len(data1)
    if nums>length:
        res1 = data1
        res2 = data2
    else:
        xulie = list( range( length ) )
        sid = random.sample( xulie, nums )
        res1 = {}
        res2 = {}
        for xid in range( nums ):
            res1[str( xid )] = data1[str( sid[xid] )]
            res2[str( xid )] = data2[str( sid[xid] )]

    with open( writename1, 'w', encoding='utf-8' ) as f:
        json.dump(res1,f)
    with open(writename2, 'w', encoding='utf-8') as f:
        json.dump(res2,f)


def genData_participant(filename,nums):

    # name1 = filename.split('\\')[1]
    # writename1 = 'change_participant_nums\\participant_nums_'+str(nums)+"\\"+name1  # 任务概貌（聚类）
    name1 = filename.split('/')[2]
    writename1 = 'T-drive_beijing/location_data/change_participant_nums/participant_nums_' + str( nums ) + "/" + name1  # 任务概貌（聚类）
    with open(filename,'r',encoding='utf-8') as f:
        data1 = json.load(f)
    length = len(data1)
    if nums>length:
        res1 = data1
    else:
        xulie = list( range( length ) )
        sid = random.sample( xulie, nums )
        res1 = {}
        for xid in range( nums ):
            res1[str( xid )] = data1[str( sid[xid] )]

    with open( writename1, 'w', encoding='utf-8' ) as f:
        json.dump(res1,f)



if __name__ == '__main__':
    # 任务数量大于300的时间段：6814 6815 6816  6714 6715 6716 6717（294）
    # addr1 = 'ddd_d100data_end_with_task\\6717.txt'  # 任务概貌（聚类）
    # addr2 = 'ddd_d100data_end_with_task\\6717_1.json'  # 任务概貌（不聚类）
    addr1 = 'T-drive_beijing/d100data_end_with_task/2309.txt'  # 任务概貌（聚类）
    addr2 = 'T-drive_beijing/d100data_end_with_task/2309_1.json'  # 任务概貌（不聚类）
    for i in range(50,301,50):
        genData_task(addr1,addr2,i)
    # 任务数量大于300的时间段：6814 6815 6816  6714 6715 6716 6717（294）
    # addr = 'ddd_d100data_start_with_sensor\\6816.json'
    # for i in range(50,301,50):
    #     genData_participant(addr,i)

