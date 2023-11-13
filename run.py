# -*- coding: utf-8 -*-

"""
在各种数据下评估提出方法的性能
"""

#  序号    |   方法名                 |      方法描述
# ------------------------------------------------------------------------------------------------------------------------------——————————
#  1      |   randomAllocate          |  随机的为每个任务安排参与者                                                                           #
# ----------------------------------------------------------------------------------------------------------------------------------------
#  2      | TA_by_first_distance      |  按照距离优先的原则，为每个个任务选择距离最短的参与者，并进一步迭代贪心选择招募参与者后，所需移动距离最短的任务       #
# ----------------------------------------------------------------------------------------------------------------------------------------
#  3      | TA_by_first_finish_rate   |  按照完成率优先的原则，为每个任务选择花费报酬最少的参与者，并进一步迭代贪心选择招募参与者后，任务完成率最大的任务     #
# ----------------------------------------------------------------------------------------------------------------------------------------
#  4      | task_allocate(不聚类)      |  按照总效用最小的原则，为每个任务选择支付报酬最少的参与者，然后进一步迭代贪心的选择总效用最小的任务                #
# ------------------------------------------------------------------------------------------------------------------------------——————————
#  5      | task_allocate     |  先将位置相近的、任务类型相似的任务聚合起来，将其打包为同一个任务，然后按照总效用最小的原则，为每个任务选择支付报酬最少#
#         |                           |  的参与者，然后进一步迭代贪心的选择总效用最小的任务                                                       #
# ---------------------------------------------------------------------------------------------------------------------------------------

import json
import random

import pandas as pd
import os
import pathlib

from randomAllocate import randomMatch
from new_TA_by_first_finish_rate import allocate_by_first_finish_rate
from TA_by_first_distance import allocate_by_first_distance
from task_allocation import allocate
from allocate_bizhi import allocate_bizhi
# from MTA_TC import MTATC




#  不同时间段下的各个方法的性能
def start1():
    count = 0
    header = []
    form1 = [[] for i in range( 6 )]  # 表示任务完成率
    form2 = [[] for i in range( 6 )]  # 表示移动距离
    form3 = [[] for i in range( 6 )]  # 表示总效用
    form4 = [[] for i in range( 6 )]  # 表示任务完成数量
    for bai in range(65, 70):
        for ge in range(1, 25):
            # 拼接生成要读取的数据文件名称
            if ge <= 9:
                # addr = 'newdata_d100data_start_with_sensor\\' + str(bai) + '0' + str(ge) + '.json'  # 参与者概貌
                addr = 'ddd_d100data_start_with_sensor\\' + str( bai ) + '0' + str( ge ) + '.json'  # 参与者概貌
                # addr1 = 'newdata_d100data_end_with_task\\' + str(bai) + '0' + str(ge) + '.txt'
                # addr2 = 'newdata_d100data_end_with_task\\' + str( bai ) + '0' + str( ge ) + '_1.json'
                addr1 = 'ddd_d100data_end_with_task\\' + str( bai ) + '0' + str( ge ) + '.txt'    # 任务概貌（聚类）
                addr2 = 'ddd_d100data_end_with_task\\' + str( bai ) + '0' + str( ge ) + '_1.json'  # 任务概貌（不聚类）
                bianhao = str( bai ) + '0' + str( ge )
            else:
                # addr = 'newdata_d100data_start_with_sensor\\' + str(bai) + str(ge) + '.json'  # 参与者概貌
                addr = 'ddd_d100data_start_with_sensor\\' + str( bai ) + str( ge ) + '.json'  # 参与者概貌
                # addr1 = 'newdata_d100data_end_with_task\\' + str(bai) + str(ge) + '.txt'
                # addr2 = 'newdata_d100data_end_with_task\\' + str( bai ) + str( ge ) + '_1.json'
                addr1 = 'ddd_d100data_end_with_task\\' + str( bai ) + str( ge ) + '.txt'       #任务概貌（聚类）
                addr2 = 'ddd_d100data_end_with_task\\' + str( bai ) + str( ge ) + '_1.json'    # 任务概貌（不聚类）
                bianhao = str( bai )  + str( ge )
            #判断文件是否存在
            filepathx = pathlib.Path( addr )
            if not filepathx.exists( ):
                continue
            # 读取文件
            with open(addr1,'r',encoding='utf-8') as f:
                temp = json.load(f)
            length = len(temp)

            print(f"当前时间段为2008-{bai//10}-{bai%10} {ge-1}:00:00, {length}个任务待分配。文件编号：{bianhao}")

            print("随机分配的结果为：")
            finish_rate_1,distance_1,accomplished_task_num_1 = randomMatch(addr,addr1)
            print(f"任务完成率为{finish_rate_1},总得移动距离为{distance_1}，已完成的任务数量为{accomplished_task_num_1}")
            print("+"+"-"*100+"+")
            form1[0].append( finish_rate_1 )
            form2[0].append( distance_1 )
            form3[0].append( 0 )
            form4[0].append( accomplished_task_num_1 )

            print("移动距离优先策略分配的结果为：")
            finish_rate_2,distance_2,agg_utility_2,accomplished_task_num_2 = allocate_by_first_distance(addr,addr1)
            print( f"任务完成率为{finish_rate_2},总得移动距离为{distance_2}，综合效用为{agg_utility_2},已完成的任务数量为{accomplished_task_num_2}" )
            print( "+" + "-" * 100 + "+" )
            form1[1].append( finish_rate_2 )
            form2[1].append( distance_2 )
            form3[1].append( agg_utility_2 )
            form4[1].append( accomplished_task_num_2 )

            print( "任务完成率优先策略分配的结果为：" )
            finish_rate_3,distance_3,agg_utility_3,accomplished_task_num_3 = allocate_by_first_finish_rate(addr,addr1)
            print( f"任务完成率为{finish_rate_3},总得移动距离为{distance_3}，综合效用为{agg_utility_3},已完成的任务数量为{accomplished_task_num_3}" )
            print( "+" + "-" * 100 + "+" )
            form1[2].append( finish_rate_3 )
            form2[2].append( distance_3 )
            form3[2].append( agg_utility_3 )
            form4[2].append( accomplished_task_num_3 )



            print( "综合效率优先策略（不聚类）分配的结果为：" )
            finish_rate_4,distance_4,agg_utility_4,accomplished_task_num_4 = allocate(addr,addr2)
            print( f"任务完成率为{finish_rate_4},总得移动距离为{distance_4}，综合效用为{agg_utility_4},已完成的任务数量为{accomplished_task_num_4}" )
            print( "+" + "-" * 100 + "+" )

            form1[3].append( finish_rate_4 )
            form2[3].append( distance_4 )
            form3[3].append( agg_utility_4 )
            form4[3].append( accomplished_task_num_4 )

            print( "综合效率优先策略分配的结果为：" )
            finish_rate_5,distance_5,agg_utility_5,accomplished_task_num_5 = allocate(addr,addr1)
            print( f"任务完成率为{finish_rate_5},总得移动距离为{distance_5}，综合效用为{agg_utility_5},已完成的任务数量为{accomplished_task_num_5}" )
            print( "+" + "-" * 100 + "+" )

            form1[4].append( finish_rate_5 )
            form2[4].append( distance_5 )
            form3[4].append( agg_utility_5 )
            form4[4].append( accomplished_task_num_5 )

            print( "综合效率优先策略分配(比值)的结果为：" )
            finish_rate_6, distance_6, agg_utility_6, accomplished_task_num_6 = allocate_bizhi( addr, addr1 )
            print(
                f"任务完成率为{finish_rate_6},总得移动距离为{distance_6}，综合效用为{agg_utility_6},已完成的任务数量为{accomplished_task_num_6}" )
            print( "+" + "-" * 100 + "+" )
            form1[5].append( finish_rate_6 )
            form2[5].append( distance_6 )
            form3[5].append( agg_utility_6 )
            form4[5].append( accomplished_task_num_6 )

            header.append(bianhao)

            print( )
            print( )

    df1 = pd.DataFrame( form1, columns=header )
    df2 = pd.DataFrame( form2, columns=header )
    df3 = pd.DataFrame( form3, columns=header )
    df4 = pd.DataFrame( form4, columns=header )
    # writer = pd.ExcelWriter( 'result222.xlsx' )
    # 测试一下
    writer = pd.ExcelWriter( 'result44444.xlsx' )
    df1.to_excel( writer, sheet_name='finish_rate', index=False )
    df2.to_excel( writer, sheet_name='distance', index=False )
    df3.to_excel( writer, sheet_name='utility', index=False )
    df4.to_excel( writer, sheet_name='task_nums', index=False )
    writer.close( )


# 不同任务数量下的性能
def start2():
    # 计算在不同的任务规模下，计算各种算法的性能
    # 这里选择了任务数量大于300时间段的任务从中分别随机选择了 50 100 150 200 250 300个任务
    # 这几个时段分别是 6714 6715 6716 6717（294） 6814 6815 6816
    file_id  = [6714,6715,6716,6717,6814,6815,6816]
    nums = list(range(50,301,50))

    header = []
    form1 = [[] for i in range( 6 )]  # 表示任务完成率
    form2 = [[] for i in range( 6 )]  # 表示移动距离
    form3 = [[] for i in range( 6 )]  # 表示总效用
    form4 = [[] for i in range( 6 )]  # 表示任务完成数量

    for num in nums:
        for fid in file_id:
            addr = 'ddd_d100data_start_with_sensor\\' + str( fid ) + '.json'  # 参与者概貌
            addr1 = 'change_task_nums\\task_nums_'+str(num)+"\\"+str(fid)+'.txt'
            addr2 = 'change_task_nums\\task_nums_' + str( num ) + "\\" + str( fid ) + '_1.json'
            with open(addr1,'r',encoding='utf-8') as f:
                temp = json.load(f)
            length = len(temp)

            with open(addr,'r',encoding='utf-8') as f:
                temp = json.load(f)
            length2 = len(temp)

            print( f"当前时间段为2008-{str(fid)[0]}-{str(fid)[1]} {str(fid-1)[2:]}:00:00, {length}个任务待分配。文件编号：{fid}" )
            print(f"参与者的人数时{length2}")
            print( "随机分配的结果为：" )
            finish_rate_1, distance_1, accomplished_task_num_1 = randomMatch( addr, addr1 )
            print( f"任务完成率为{finish_rate_1},总得移动距离为{distance_1}，已完成的任务数量为{accomplished_task_num_1}" )
            print( "+" + "-" * 100 + "+" )
            form1[0].append( finish_rate_1 )
            form2[0].append( distance_1 )
            form3[0].append( 0 )
            form4[0].append( accomplished_task_num_1 )

            print( "移动距离优先策略分配的结果为：" )
            finish_rate_2, distance_2, agg_utility_2, accomplished_task_num_2 = allocate_by_first_distance( addr,
                                                                                                            addr1 )
            print(
                f"任务完成率为{finish_rate_2},总得移动距离为{distance_2}，综合效用为{agg_utility_2},已完成的任务数量为{accomplished_task_num_2}" )
            print( "+" + "-" * 100 + "+" )
            form1[1].append( finish_rate_2 )
            form2[1].append( distance_2 )
            form3[1].append( agg_utility_2 )
            form4[1].append( accomplished_task_num_2 )

            print( "任务完成率优先策略分配的结果为：" )
            finish_rate_3, distance_3, agg_utility_3, accomplished_task_num_3 = allocate_by_first_finish_rate( addr,
                                                                                                               addr1 )
            print(
                f"任务完成率为{finish_rate_3},总得移动距离为{distance_3}，综合效用为{agg_utility_3},已完成的任务数量为{accomplished_task_num_3}" )
            print( "+" + "-" * 100 + "+" )
            form1[2].append( finish_rate_3 )
            form2[2].append( distance_3 )
            form3[2].append( agg_utility_3 )
            form4[2].append( accomplished_task_num_3 )

            print( "综合效率优先策略（不聚类）分配的结果为：" )
            finish_rate_4, distance_4, agg_utility_4, accomplished_task_num_4 = allocate( addr, addr2 )
            print(
                f"任务完成率为{finish_rate_4},总得移动距离为{distance_4}，综合效用为{agg_utility_4},已完成的任务数量为{accomplished_task_num_4}" )
            print( "+" + "-" * 100 + "+" )

            form1[3].append( finish_rate_4 )
            form2[3].append( distance_4 )
            form3[3].append( agg_utility_4 )
            form4[3].append( accomplished_task_num_4 )

            print( "综合效率优先策略分配的结果为：" )
            finish_rate_5, distance_5, agg_utility_5, accomplished_task_num_5 = allocate( addr, addr1 )
            print(
                f"任务完成率为{finish_rate_5},总得移动距离为{distance_5}，综合效用为{agg_utility_5},已完成的任务数量为{accomplished_task_num_5}" )
            print( "+" + "-" * 100 + "+" )

            form1[4].append( finish_rate_5 )
            form2[4].append( distance_5 )
            form3[4].append( agg_utility_5 )
            form4[4].append( accomplished_task_num_5 )

            print( "综合效率优先策略分配(比值)的结果为：" )
            finish_rate_6, distance_6, agg_utility_6, accomplished_task_num_6 = allocate_bizhi( addr, addr1 )
            print(
                f"任务完成率为{finish_rate_6},总得移动距离为{distance_6}，综合效用为{agg_utility_6},已完成的任务数量为{accomplished_task_num_6}" )
            print( "+" + "-" * 100 + "+" )
            form1[5].append( finish_rate_6 )
            form2[5].append( distance_6 )
            form3[5].append( agg_utility_6 )
            form4[5].append( accomplished_task_num_6 )

            header.append( str(fid)+'_'+str(num) )

            print( )
            print( )
    df1 = pd.DataFrame( form1, columns=header )
    df2 = pd.DataFrame( form2, columns=header )
    df3 = pd.DataFrame( form3, columns=header )
    df4 = pd.DataFrame( form4, columns=header )
    # writer = pd.ExcelWriter( 'result_change_task_nums.xlsx' )
    #  测试一下
    writer = pd.ExcelWriter( 'result_change_task_nums——tttttt.xlsx' )
    df1.to_excel( writer, sheet_name='finish_rate', index=False )
    df2.to_excel( writer, sheet_name='distance', index=False )
    df3.to_excel( writer, sheet_name='utility', index=False )
    df4.to_excel( writer, sheet_name='task_nums', index=False )
    writer.close( )

# 不同参与者数量下的各个算法的性能
def start3():
    # 计算在不同的参与者规模下，计算各种算法的性能
    # 这里选择了任务数量大于300时间段的任务从中分别随机选择了 50 100 150 200 250 300个任务
    # 这几个时段分别是 6714 6715 6716 6717（294） 6814 6815 6816
    file_id = [6714, 6715, 6716, 6717, 6814, 6815, 6816]
    nums = list( range( 50, 301, 50 ) )

    header = []
    form1 = [[] for i in range( 6 )]  # 表示任务完成率
    form2 = [[] for i in range( 6 )]  # 表示移动距离
    form3 = [[] for i in range( 6 )]  # 表示总效用
    form4 = [[] for i in range( 6 )]  # 表示任务完成数量

    for num in nums:
        for fid in file_id:
            addr = 'change_participant_nums\\participant_nums_' +str(num) +"\\"+ str( fid ) + '.json'  # 参与者概貌
            addr1 = 'change_task_nums\\task_nums_300' +  "\\" + str( fid ) + '.txt'
            addr2 = 'change_task_nums\\task_nums_300' + "\\" + str( fid ) + '_1.json'
            with open( addr1, 'r', encoding='utf-8' ) as f:
                temp = json.load( f )
            length = len( temp )

            with open( addr, 'r', encoding='utf-8' ) as f:
                temp = json.load( f )
            length2 = len( temp )

            print( f"当前时间段为2008-{str( fid )[0]}-{str( fid )[1]} {str( fid - 1 )[2:]}:00:00, {length}个任务待分配。文件编号：{fid}" )
            print( f"参与者的人数时{length2}" )
            print( "随机分配的结果为：" )
            finish_rate_1, distance_1, accomplished_task_num_1 = randomMatch( addr, addr1 )
            print( f"任务完成率为{finish_rate_1},总得移动距离为{distance_1}，已完成的任务数量为{accomplished_task_num_1}" )
            print( "+" + "-" * 100 + "+" )
            form1[0].append( finish_rate_1 )
            form2[0].append( distance_1 )
            form3[0].append( 0 )
            form4[0].append( accomplished_task_num_1 )

            print( "移动距离优先策略分配的结果为：" )
            finish_rate_2, distance_2, agg_utility_2, accomplished_task_num_2 = allocate_by_first_distance( addr,
                                                                                                            addr1 )
            print(
                f"任务完成率为{finish_rate_2},总得移动距离为{distance_2}，综合效用为{agg_utility_2},已完成的任务数量为{accomplished_task_num_2}" )
            print( "+" + "-" * 100 + "+" )
            form1[1].append( finish_rate_2 )
            form2[1].append( distance_2 )
            form3[1].append( agg_utility_2 )
            form4[1].append( accomplished_task_num_2 )

            print( "任务完成率优先策略分配的结果为：" )
            finish_rate_3, distance_3, agg_utility_3, accomplished_task_num_3 = allocate_by_first_finish_rate( addr,
                                                                                                               addr1 )
            print(
                f"任务完成率为{finish_rate_3},总得移动距离为{distance_3}，综合效用为{agg_utility_3},已完成的任务数量为{accomplished_task_num_3}" )
            print( "+" + "-" * 100 + "+" )
            form1[2].append( finish_rate_3 )
            form2[2].append( distance_3 )
            form3[2].append( agg_utility_3 )
            form4[2].append( accomplished_task_num_3 )

            print( "综合效率优先策略（不聚类）分配的结果为：" )
            finish_rate_4, distance_4, agg_utility_4, accomplished_task_num_4 = allocate( addr, addr2 )
            print(
                f"任务完成率为{finish_rate_4},总得移动距离为{distance_4}，综合效用为{agg_utility_4},已完成的任务数量为{accomplished_task_num_4}" )
            print( "+" + "-" * 100 + "+" )

            form1[3].append( finish_rate_4 )
            form2[3].append( distance_4 )
            form3[3].append( agg_utility_4 )
            form4[3].append( accomplished_task_num_4 )

            print( "综合效率优先策略分配的结果为：" )
            finish_rate_5, distance_5, agg_utility_5, accomplished_task_num_5 = allocate( addr, addr1 )
            print(
                f"任务完成率为{finish_rate_5},总得移动距离为{distance_5}，综合效用为{agg_utility_5},已完成的任务数量为{accomplished_task_num_5}" )
            print( "+" + "-" * 100 + "+" )

            form1[4].append( finish_rate_5 )
            form2[4].append( distance_5 )
            form3[4].append( agg_utility_5 )
            form4[4].append( accomplished_task_num_5 )

            print( "综合效率优先策略分配(比值)的结果为：" )
            finish_rate_6, distance_6, agg_utility_6, accomplished_task_num_6 = allocate_bizhi( addr, addr1 )
            print(
                f"任务完成率为{finish_rate_6},总得移动距离为{distance_6}，综合效用为{agg_utility_6},已完成的任务数量为{accomplished_task_num_6}" )
            print( "+" + "-" * 100 + "+" )
            form1[5].append( finish_rate_6 )
            form2[5].append( distance_6 )
            form3[5].append( agg_utility_6 )
            form4[5].append( accomplished_task_num_6 )

            header.append( str( fid ) + '_' + str( num ) )

            print( )
            print( )
    df1 = pd.DataFrame( form1, columns=header )
    df2 = pd.DataFrame( form2, columns=header )
    df3 = pd.DataFrame( form3, columns=header )
    df4 = pd.DataFrame( form4, columns=header )
    # writer = pd.ExcelWriter( 'result_change_participant_nums.xlsx' )
    # 测试之前修改一下文件名，不然会覆盖之前的结果
    writer = pd.ExcelWriter( 'result_change_participant_nums_test.xlsx' )
    df1.to_excel( writer, sheet_name='finish_rate', index=False )
    df2.to_excel( writer, sheet_name='distance', index=False )
    df3.to_excel( writer, sheet_name='utility', index=False )
    df4.to_excel( writer, sheet_name='task_nums', index=False )
    writer.close( )
#
# def start4():
#     file_id = [6714, 6715, 6716, 6717, 6814, 6815, 6816]
#     nums = list( range( 50, 301, 50 ) )
#
#     header = []
#     form1 = [[]]  # 表示任务完成率
#     form2 = [[]]  # 表示移动距离
#     # form3 = []  # 表示总效用
#     form4 = [[]]  # 表示任务完成数量
#
#     for num in nums:
#         for fid in file_id:
#             addr = 'ddd_d100data_start_with_sensor\\' + str( fid ) + '.json'  # 参与者概貌
#             addr1 = 'change_task_nums\\task_nums_' + str( num ) + "\\" + str( fid ) + '.txt'
#             addr2 = 'change_task_nums\\task_nums_' + str( num ) + "\\" + str( fid ) + '_1.json'
#             with open( addr1, 'r', encoding='utf-8' ) as f:
#                 temp = json.load( f )
#             length = len( temp )
#
#             with open( addr, 'r', encoding='utf-8' ) as f:
#                 temp = json.load( f )
#             length2 = len( temp )
#
#             print( f"当前时间段为2008-{str( fid )[0]}-{str( fid )[1]} {str( fid - 1 )[2:]}:00:00, {length}个任务待分配。文件编号：{fid}" )
#             print( f"参与者的人数时{length2}" )
#             print( "MTA-TC分配的结果为：" )
#             finish_rate_7, distance_7, accomplished_task_num_7 = MTATC( addr, addr2 )
#             print( f"任务完成率为{finish_rate_7},总得移动距离为{distance_7}，已完成的任务数量为{accomplished_task_num_7}" )
#             print( "+" + "-" * 100 + "+" )
#             form1[0].append(finish_rate_7)
#             form2[0].append(distance_7)
#             form4[0].append(accomplished_task_num_7)
#             header.append( str( fid ) + '_' + str( num ) )
#
#             print( )
#             print( )
#     df1 = pd.DataFrame( form1, columns=header )
#     df2 = pd.DataFrame( form2, columns=header )
#     # df3 = pd.DataFrame( form3, columns=header )
#     df4 = pd.DataFrame( form4, columns=header )
#     writer = pd.ExcelWriter( 'result_change_task_nums_comp.xlsx' )
#     df1.to_excel( writer, sheet_name='finish_rate', index=False )
#     df2.to_excel( writer, sheet_name='distance', index=False )
#     # df3.to_excel( writer, sheet_name='utility', index=False )
#     df4.to_excel( writer, sheet_name='task_nums', index=False )
#     writer.close( )
#
#
# def start5():
#     file_id = [6714, 6715, 6716, 6717, 6814, 6815, 6816]
#     nums = list( range( 50, 301, 50 ) )
#
#     header = []
#     form1 = [[]]  # 表示任务完成率
#     form2 = [[]]  # 表示移动距离
#     # form3 = []  # 表示总效用
#     form4 = [[]]  # 表示任务完成数量
#
#     for num in nums:
#         for fid in file_id:
#             addr = 'change_participant_nums\\participant_nums_' + str( num ) + "\\" + str( fid ) + '.json'  # 参与者概貌
#             addr1 = 'change_task_nums\\task_nums_300' + "\\" + str( fid ) + '.txt'
#             addr2 = 'change_task_nums\\task_nums_300' + "\\" + str( fid ) + '_1.json'
#             with open( addr1, 'r', encoding='utf-8' ) as f:
#                 temp = json.load( f )
#             length = len( temp )
#
#             with open( addr, 'r', encoding='utf-8' ) as f:
#                 temp = json.load( f )
#             length2 = len( temp )
#
#             print( f"当前时间段为2008-{str( fid )[0]}-{str( fid )[1]} {str( fid - 1 )[2:]}:00:00, {length}个任务待分配。文件编号：{fid}" )
#             print( f"参与者的人数时{length2}" )
#             print( "MTA-TC分配的结果为：" )
#             finish_rate_7, distance_7, accomplished_task_num_7 = MTATC( addr, addr2 )
#             print( f"任务完成率为{finish_rate_7},总得移动距离为{distance_7}，已完成的任务数量为{accomplished_task_num_7}" )
#             print( "+" + "-" * 100 + "+" )
#             form1[0].append(finish_rate_7)
#             form2[0].append(distance_7)
#             form4[0].append(accomplished_task_num_7)
#             header.append( str( fid ) + '_' + str( num ) )
#
#             print( )
#             print( )
#     df1 = pd.DataFrame( form1, columns=header )
#     df2 = pd.DataFrame( form2, columns=header )
#     # df3 = pd.DataFrame( form3, columns=header )
#     df4 = pd.DataFrame( form4, columns=header )
#     #writer = pd.ExcelWriter( 'result_change_participant_nums_comp.xlsx' )
#     # 测试之前修改文件名 不然会覆盖之前的结果
#     writer = pd.ExcelWriter( 'result_change_participant_nums_comp.xlsx' )
#     df1.to_excel( writer, sheet_name='finish_rate', index=False )
#     df2.to_excel( writer, sheet_name='distance', index=False )
#     # df3.to_excel( writer, sheet_name='utility', index=False )
#     df4.to_excel( writer, sheet_name='task_nums', index=False )
#     writer.close( )


def start_BJ1():
    file_id = list(range(2400,2424))
    nums = list( range( 50, 301, 50 ) )

    header = []
    form1 = [[] for i in range( 6 )]  # 表示任务完成率
    form2 = [[] for i in range( 6 )]  # 表示移动距离
    form3 = [[] for i in range( 6 )]  # 表示总效用
    form4 = [[] for i in range( 6 )]  # 表示任务完成数量


    for num in nums:
        for fid in file_id:

            # # 这是改变任务数量的
            # addr = 'T-drive_beijing/d100data_start_with_sensor'+ "/" + str( fid ) + '.json'  # 参与者概貌
            # addr1 = 'T-drive_beijing/location_data/change_task_nums/task_nums_' +str(num)+ "\\" + str( fid ) + '.txt'
            # addr2 = 'T-drive_beijing/location_data/change_task_nums/task_nums_' +str(num)+ "\\" + str( fid ) + '_1.json'


            # 这是改变参与者数量的
            addr = 'T-drive_beijing/location_data/change_participant_nums/participant_nums_' + str( num )+ '/'+str( fid ) + '.json'  # 参与者概貌
            addr1 = 'T-drive_beijing/location_data/change_task_nums/task_nums_300'  + "/" + str(
                fid ) + '.txt'
            addr2 = 'T-drive_beijing/location_data/change_task_nums/task_nums_300'  + "/" + str(
                fid ) + '_1.json'
            with open( addr1, 'r', encoding='utf-8' ) as f:
                temp = json.load( f )
            length = len( temp )

            with open( addr, 'r', encoding='utf-8' ) as f:
                temp = json.load( f )
            length2 = len( temp )

            print( f"当前时间段为2008-{str( fid )[0]}-{str( fid )[1]} {str( fid - 1 )[2:]}:00:00, {length}个任务待分配。文件编号：{fid}" )
            print( f"参与者的人数时{length2}" )
            print( "随机分配的结果为：" )
            finish_rate_1, distance_1, accomplished_task_num_1 = randomMatch( addr, addr1 )
            print( f"任务完成率为{finish_rate_1},总得移动距离为{distance_1}，已完成的任务数量为{accomplished_task_num_1}" )
            print( "+" + "-" * 100 + "+" )
            form1[0].append( finish_rate_1 )
            form2[0].append( distance_1 )
            form3[0].append( 0 )
            form4[0].append( accomplished_task_num_1 )

            print( "移动距离优先策略分配的结果为：" )
            finish_rate_2, distance_2, agg_utility_2, accomplished_task_num_2 = allocate_by_first_distance( addr,
                                                                                                            addr1 )
            print(
                f"任务完成率为{finish_rate_2},总得移动距离为{distance_2}，综合效用为{agg_utility_2},已完成的任务数量为{accomplished_task_num_2}" )
            print( "+" + "-" * 100 + "+" )
            form1[1].append( finish_rate_2 )
            form2[1].append( distance_2 )
            form3[1].append( agg_utility_2 )
            form4[1].append( accomplished_task_num_2 )

            print( "任务完成率优先策略分配的结果为：" )
            finish_rate_3, distance_3, agg_utility_3, accomplished_task_num_3 = allocate_by_first_finish_rate( addr,
                                                                                                               addr1 )
            print(
                f"任务完成率为{finish_rate_3},总得移动距离为{distance_3}，综合效用为{agg_utility_3},已完成的任务数量为{accomplished_task_num_3}" )
            print( "+" + "-" * 100 + "+" )
            form1[2].append( finish_rate_3 )
            form2[2].append( distance_3 )
            form3[2].append( agg_utility_3 )
            form4[2].append( accomplished_task_num_3 )

            print( "综合效率优先策略（不聚类）分配的结果为：" )
            finish_rate_4, distance_4, agg_utility_4, accomplished_task_num_4 = allocate( addr, addr2 )
            print(
                f"任务完成率为{finish_rate_4},总得移动距离为{distance_4}，综合效用为{agg_utility_4},已完成的任务数量为{accomplished_task_num_4}" )
            print( "+" + "-" * 100 + "+" )

            form1[3].append( finish_rate_4 )
            form2[3].append( distance_4 )
            form3[3].append( agg_utility_4 )
            form4[3].append( accomplished_task_num_4 )

            print( "综合效率优先策略分配的结果为：" )
            finish_rate_5, distance_5, agg_utility_5, accomplished_task_num_5 = allocate( addr, addr1 )
            print(
                f"任务完成率为{finish_rate_5},总得移动距离为{distance_5}，综合效用为{agg_utility_5},已完成的任务数量为{accomplished_task_num_5}" )
            print( "+" + "-" * 100 + "+" )

            form1[4].append( finish_rate_5 )
            form2[4].append( distance_5 )
            form3[4].append( agg_utility_5 )
            form4[4].append( accomplished_task_num_5 )

            print( "综合效率优先策略分配(比值)的结果为：" )
            finish_rate_6, distance_6, agg_utility_6, accomplished_task_num_6 = allocate_bizhi( addr, addr1 )
            print(
                f"任务完成率为{finish_rate_6},总得移动距离为{distance_6}，综合效用为{agg_utility_6},已完成的任务数量为{accomplished_task_num_6}" )
            print( "+" + "-" * 100 + "+" )
            form1[5].append( finish_rate_6 )
            form2[5].append( distance_6 )
            form3[5].append( agg_utility_6 )
            form4[5].append( accomplished_task_num_6 )

            header.append( str( fid ) + '_' + str( num ) )

            print( )
            print( )
    df1 = pd.DataFrame( form1, columns=header )
    df2 = pd.DataFrame( form2, columns=header )
    df3 = pd.DataFrame( form3, columns=header )
    df4 = pd.DataFrame( form4, columns=header )
    #writer = pd.ExcelWriter( 'beijing_result_change_participant_nums(24).xlsx' )
    # 测试验证的时候把文件名改一下 不然会覆盖之前的结果。
    writer = pd.ExcelWriter( 'beijing_result_change_participant_nums(24)_test.xlsx' )
    df1.to_excel( writer, sheet_name='finish_rate', index=False )
    df2.to_excel( writer, sheet_name='distance', index=False )
    df3.to_excel( writer, sheet_name='utility', index=False )
    df4.to_excel( writer, sheet_name='task_nums', index=False )
    writer.close( )


if __name__ == '__main__':
    # 在这里打开相关函数的注释 实现不同的实验
    # start1()
    start2()
    # start3()
    # start5()
    # start_BJ1()
