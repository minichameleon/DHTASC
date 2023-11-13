# -*- coding: utf-8 -*-

"""
根据计算所得的数据绘图
"""
import matplotlib.pyplot as plt
import xlrd
import numpy as np
from matplotlib.pyplot import MultipleLocator


save_path ='图片\\'
wb = xlrd.open_workbook('res_roma.xlsx')
sheet_num = wb.nsheets
sheet_namess = wb.sheet_names()

colorlist= ['#95a2ff', '#fa8080', '#ffc076', '#fae768','#87e885', '#3cb9fc']
labellist = ['RTA','DTFTA','QFTA','EFTA','ADHTA-LW','ADHTA-PD']
linestylelist=['s','+','D','o','p','*']

# 任务完成质量在不同任务数量下的比较  --- 罗马
# sheet = wb.sheet_by_index(0)
# rows = sheet.nrows
# columns = sheet.ncols
#
#
parameters = {'axes.labelsize': 14,
          'axes.titlesize': 35}
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams.update(parameters)
#
# width=6
# x =np.arange(50,301,50)
# plt.figure(figsize=(8,5))
# for i in range(rows):
#     row_data = sheet.row_values(i)
#     plt.bar(x=x+(i-2)*width,height=row_data,width=width-1,label=labellist[i],color=colorlist[i],ec='black',lw=.5)
# plt.xlabel('任务数量')
# plt.ylabel('TQoT')
# plt.rcParams["font.sans-serif"] = ["SimHei"]
# plt.rcParams["axes.unicode_minus"] = False
# plt.legend()
# plt.savefig(save_path+"QoT_change_task_roma.svg",bbox_inches="tight",dpi=600,format='svg')
# plt.show()
#
# # 任务完成数量在不同任务数量下的比较  --- 罗马
# sheet = wb.sheet_by_index(1)
# rows = sheet.nrows
# columns = sheet.ncols
# width=6
# x =np.arange(50,301,50)
# plt.figure(figsize=(8,5))
# for i in range(rows):
#     row_data = sheet.row_values(i)
#     plt.bar(x=x+(i-2)*width,height=row_data,width=width-1,label=labellist[i],color=colorlist[i],ec='black',lw=.5)
# plt.xlabel('任务数量')
# plt.ylabel('NoT')
# plt.rcParams["font.sans-serif"] = ["SimHei"]
# plt.rcParams["axes.unicode_minus"] = False
#
# plt.legend()
# plt.savefig(save_path+"tasknums_change_task_roma.svg",bbox_inches="tight",dpi=600,format='svg')
# plt.show()


# 任务完成质量在不同参与者数量下的比较  --- 罗马
sheet = wb.sheet_by_index(3)
rows = sheet.nrows
columns = sheet.ncols
width=6
x =np.arange(50,301,50)
plt.figure(figsize=(8,5))
for i in range(rows):
    row_data = sheet.row_values(i)
    plt.bar(x=x+(i-2)*width,height=row_data,width=width-1,label=labellist[i],color=colorlist[i],ec='black',lw=.5)
plt.xlabel('参与者数量')
plt.ylabel('TQoT')
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
plt.legend()
plt.savefig(save_path+"QoT_change_participant_roma.svg",bbox_inches="tight",dpi=600,format='svg')
plt.show()


# 任务完成数量在不同参与者数量下的比较  --- 罗马
sheet = wb.sheet_by_index(4)
rows = sheet.nrows
columns = sheet.ncols
width=5
x =np.arange(50,301,50)
plt.figure(figsize=(8,5))
for i in range(rows):
    row_data = sheet.row_values(i)
    plt.bar(x=x+(i-2)*width,height=row_data,width=width-1,label=labellist[i],color=colorlist[i],ec='black',lw=.5)
plt.xlabel('参与者数量')
plt.ylabel('NoT')
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
plt.legend()
plt.savefig(save_path+"tasknums_change_participant_roma.svg",bbox_inches="tight",dpi=600,format='svg')
plt.show()
