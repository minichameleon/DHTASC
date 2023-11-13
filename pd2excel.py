
# import math
# import pandas as pd
# import sys
# import os
# import random

# stuID = [50101,50102,50103,50104,50105]
# name = ['张三','李四','王五','孙家','杨燚']
# chinese = [96,99,93,89,90]
# maths = [100,99,99,92,95]
# english = [98,98,95,90,91]
# data1 = {"学号":stuID,"姓名":name,"语文":chinese,"数学":maths,"英语":english}
# pd.DataFrame(data1).to_excel('result.xlsx',sheet_name='Sheet1',index=False)

import json
import pandas as pd
import os
import random



def start():
    count = 0
    header = []
    form1 = [[] for i in range(6)] # 表示任务完成率
    form2 = [[] for i in range(6)] # 表示移动距离
    form3 = [[] for i in range(6)] # 表示总效用
    form4 = [[] for i in range(6)] # 表示任务完成数量
    
    for bai in range(66, 67):
        for ge in range(1, 25):
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

            # with open(addr1,'r',encoding='utf-8') as f:
            #     temp = json.load(f)
            # length = len(temp)

            print(f"当前时间段为2008-{bai//10}-{bai%10} {ge-1}:00:00, 文件编号：{bianhao}")

            print("随机分配的结果为：")
            finish_rate_1,distance_1,accomplished_task_num_1 = random.randint(0,100),random.randint(0,100),random.randint(0,100)
            print(f"任务完成率为{finish_rate_1},总得移动距离为{distance_1}，已完成的任务数量为{accomplished_task_num_1}")
            print("+"+"-"*100+"+")
            form1[0].append(finish_rate_1)
            form2[0].append(distance_1)
            form3[0].append(0)
            form4[0].append(accomplished_task_num_1)

            print("移动距离优先策略分配的结果为：")
            finish_rate_2,distance_2,agg_utility_2,accomplished_task_num_2 = random.randint(0,100),random.randint(0,100),random.randint(0,100),random.randint(0,100)
            print( f"任务完成率为{finish_rate_2},总得移动距离为{distance_2}，综合效用为{agg_utility_2},已完成的任务数量为{accomplished_task_num_2}" )
            print( "+" + "-" * 100 + "+" )

            form1[1].append(finish_rate_2)
            form2[1].append(distance_2)
            form3[1].append(agg_utility_2)
            form4[1].append(accomplished_task_num_2)


            print( "任务完成率优先策略分配的结果为：" )
            finish_rate_3,distance_3,agg_utility_3,accomplished_task_num_3 = random.randint(0,100),random.randint(0,100),random.randint(0,100),random.randint(0,100)
            print( f"任务完成率为{finish_rate_3},总得移动距离为{distance_3}，综合效用为{agg_utility_3},已完成的任务数量为{accomplished_task_num_3}" )
            print( "+" + "-" * 100 + "+" )

            form1[2].append(finish_rate_3)
            form2[2].append(distance_3)
            form3[2].append(agg_utility_3)
            form4[2].append(accomplished_task_num_3)

            print( "综合效率优先策略（不聚类）分配的结果为：" )
            finish_rate_4,distance_4,agg_utility_4,accomplished_task_num_4 = random.randint(0,100),random.randint(0,100),random.randint(0,100),random.randint(0,100)
            print( f"任务完成率为{finish_rate_4},总得移动距离为{distance_4}，综合效用为{agg_utility_4},已完成的任务数量为{accomplished_task_num_4}" )
            print( "+" + "-" * 100 + "+" )

            form1[3].append(finish_rate_4)
            form2[3].append(distance_4)
            form3[3].append(agg_utility_4)
            form4[3].append(accomplished_task_num_4)

            print( "综合效率优先策略分配的结果为：" )
            finish_rate_5,distance_5,agg_utility_5,accomplished_task_num_5 = random.randint(0,100),random.randint(0,100),random.randint(0,100),random.randint(0,100)
            print( f"任务完成率为{finish_rate_5},总得移动距离为{distance_5}，综合效用为{agg_utility_5},已完成的任务数量为{accomplished_task_num_5}" )
            print( "+" + "-" * 100 + "+" )

            form1[4].append(finish_rate_4)
            form2[4].append(distance_4)
            form3[4].append(agg_utility_4)
            form4[4].append(accomplished_task_num_4)

            print( "综合效率优先策略分配(比值)的结果为：" )
            finish_rate_6, distance_6, agg_utility_6, accomplished_task_num_6 = random.randint(0,100),random.randint(0,100),random.randint(0,100),random.randint(0,100)
            print(
                f"任务完成率为{finish_rate_6},总得移动距离为{distance_6}，综合效用为{agg_utility_6},已完成的任务数量为{accomplished_task_num_6}" )
            print( "+" + "-" * 100 + "+" )
            form1[5].append(finish_rate_5)
            form2[5].append(distance_5)
            form3[5].append(agg_utility_5)
            form4[5].append(accomplished_task_num_5)

            header.append(bianhao)
            print( )
            print( )
    print(form1)
    df1 = pd.DataFrame(form1,columns=header)
    df2 = pd.DataFrame(form2,columns=header)
    df3 = pd.DataFrame(form3, columns=header )
    df4 = pd.DataFrame(form4, columns=header )
    writer = pd.ExcelWriter( 'result222.xlsx' )
    df1.to_excel(writer,sheet_name='finish_rate',index=False)
    df2.to_excel(writer,sheet_name='distance',index=False)
    df3.to_excel(writer,sheet_name='utility',index=False)
    df4.to_excel(writer,sheet_name='task_nums',index=False)
    writer.close()
            

if __name__ == '__main__':
    start()