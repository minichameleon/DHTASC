# -*- coding: utf-8 -*-

"""
在roma数据集上测试各个算法
"""
import json
import pandas as pd
import os
import pathlib

from randomAllocate import randomMatch
from new_TA_by_first_finish_rate import allocate_by_first_finish_rate
from TA_by_first_distance import allocate_by_first_distance
from task_allocation import allocate
from allocate_bizhi import allocate_bizhi

# xuhao = ['06', '07', '10', '12', '16', '18', '19', '20', '23']

# 改变任务数量
xuhao = ['07','10','16','20']
header = []
form1 = [[] for i in range( 6 )]  # 表示任务完成率
form2 = [[] for i in range( 6 )]  # 表示移动距离
form3 = [[] for i in range( 6 )]  # 表示总效用
form4 = [[] for i in range( 6 )]  # 表示任务完成数量
for t in range(50,301,50):
    for xh in xuhao:
        addr = "roma_gen\\change_participant\\participant_300\\02-05-"+ xh + "_p.json"
        addr1 = "roma_gen\\change_task\\task_" + str(t) +"\\02-05-" + xh + "_cluster.json" # 聚类
        addr2 = "roma_gen\\change_task\\task_" + str(t) + "\\02-05-" + xh + "_bc.json"  # 不聚类

        # addr = "roma\\02-05-" + xh + "_p.json"
        # addr1 = "roma\\02-05-" + xh + "_cluster.json"  # 聚类
        # addr2 = "roma\\02-05-" + xh + "bc.json"  # 聚类

        with open( addr1, 'r', encoding='utf-8' ) as f:
            temp = json.load( f )
        length = len( temp )

        with open( addr, 'r', encoding='utf-8' ) as f:
            temp = json.load( f )
        length2 = len( temp )

        print( f"当前时间段为2014-02-05 {xh}:00:00, {length}个任务待分配。" )
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
        header.append( xh + '_' + str( t ) )

df1 = pd.DataFrame( form1, columns=header )
df2 = pd.DataFrame( form2, columns=header )
df3 = pd.DataFrame( form3, columns=header )
df4 = pd.DataFrame( form4, columns=header )
# writer = pd.ExcelWriter( 'result_change_task_nums.xlsx' )
#  测试一下
writer = pd.ExcelWriter( 'result_change_task_nums——roma.xlsx' )
df1.to_excel( writer, sheet_name='finish_rate', index=False )
df2.to_excel( writer, sheet_name='distance', index=False )
df3.to_excel( writer, sheet_name='utility', index=False )
df4.to_excel( writer, sheet_name='task_nums', index=False )
writer.close( )

# ========================================================================================================================
# 改变参与者人数
# xuhao = ['07','10']
xuhao = ['16','20']
header = []
form1 = [[] for i in range( 6 )]  # 表示任务完成率
form2 = [[] for i in range( 6 )]  # 表示移动距离
form3 = [[] for i in range( 6 )]  # 表示总效用
form4 = [[] for i in range( 6 )]  # 表示任务完成数量
for t in range(250,301,50):
    for xh in xuhao:
        addr = "roma_gen\\change_participant\\participant_"+str(t)+"\\02-05-"+ xh + "_p.json"
        addr1 = "roma_gen\\change_task\\task_300\\02-05-" + xh + "_cluster.json" # 聚类
        addr2 = "roma_gen\\change_task\\task_300\\02-05-" + xh + "_bc.json"  # 不聚类

        # addr = "roma\\02-05-" + xh + "_p.json"
        # addr1 = "roma\\02-05-" + xh + "_cluster.json"  # 聚类
        # addr2 = "roma\\02-05-" + xh + "bc.json"  # 聚类

        with open( addr1, 'r', encoding='utf-8' ) as f:
            temp = json.load( f )
        length = len( temp )

        with open( addr, 'r', encoding='utf-8' ) as f:
            temp = json.load( f )
        length2 = len( temp )

        print( f"当前时间段为2014-02-05 {xh}:00:00, {length}个任务待分配。" )
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
        header.append( xh + '_' + str( t ) )

df1 = pd.DataFrame( form1, columns=header )
df2 = pd.DataFrame( form2, columns=header )
df3 = pd.DataFrame( form3, columns=header )
df4 = pd.DataFrame( form4, columns=header )
# writer = pd.ExcelWriter( 'result_change_task_nums.xlsx' )
#  测试一下
writer = pd.ExcelWriter( 'result_change_participant_nums——roma_250-300.xlsx' )
df1.to_excel( writer, sheet_name='finish_rate', index=False )
df2.to_excel( writer, sheet_name='distance', index=False )
df3.to_excel( writer, sheet_name='utility', index=False )
df4.to_excel( writer, sheet_name='task_nums', index=False )
writer.close( )