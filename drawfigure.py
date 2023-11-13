# -*- coding: utf-8 -*-

"""
根据计算所得的数据绘图
"""

import matplotlib.pyplot as plt
import xlrd
import numpy as np
from matplotlib.pyplot import MultipleLocator



hour = list(range(1,25))

wb = xlrd.open_workbook('C:\\Users\\s-monster\\Desktop\\res.xlsx')
sheet_num = wb.nsheets
sheet_namess = wb.sheet_names()
# 任务完成质量在时间变化下的比较  --- 旧金山
sheet = wb.sheet_by_index(0)
rows = sheet.nrows
columns = sheet.ncols
colorlist=['g','peru','b','darkviolet','k','r']
# labellist = ['RA','DFTA','QFTA','DEFTA','LWGTA','CDGTA']
labellist = ['RA','DFTA','QFTA','DEFTA','TALW','TARD']
linestylelist=['s','+','D','o','p','*']

my_x_ticks=hour
plt.xticks(my_x_ticks)
for i in range(rows):
    row_data = sheet.row_values(i)
    # plt.title('The quality of task accompletion')
    plt.xlabel('time')
    plt.ylabel('TQoT')
    # plt.scatter(hour,row_data,c=colorlist[i],marker=linestylelist[i])
    plt.plot(hour,row_data,marker=linestylelist[i],markersize=5,label=labellist[i],color=colorlist[i],linewidth=0.8,linestyle='-')
plt.legend(loc=1)
x_major_locator=MultipleLocator(2)
ax=plt.gca()
ax.xaxis.set_major_locator(x_major_locator)
plt.savefig(r'C:\Users\s-monster\Desktop\exp_pic\QoT_time.pdf', bbox_inches='tight')
plt.show()


#
# 平均移动距离在时间变化下的比较  ---旧金山
sheet = wb.sheet_by_index(1)
rows = sheet.nrows
columns = sheet.ncols
colorlist=['g','peru','b','darkviolet','k','r']
# labellist = ['random','first_by_dis','first_by_TAR','utility_nocluster','utility_cluster','bizhi_cluster']
linestylelist=['s','+','D','o','p','*']
my_x_ticks=hour
plt.xticks(my_x_ticks)
for i in range(rows):
    row_data = sheet.row_values(i)
    # plt.title('The average distance participants traveled to complete a task')
    plt.xlabel('time')
    plt.ylabel('ADT')
    plt.plot(hour,row_data,marker=linestylelist[i],markersize=5,label=labellist[i],color=colorlist[i],linewidth=0.8,linestyle='-')
plt.legend(loc=7,bbox_to_anchor=(1,0.4))
x_major_locator=MultipleLocator(2)
ax=plt.gca()
ax.xaxis.set_major_locator(x_major_locator)
plt.savefig(r'C:\Users\s-monster\Desktop\exp_pic\distance_time.pdf', bbox_inches='tight')
plt.show()


# 总效用在时间变化下的比较  --- 旧金山
sheet = wb.sheet_by_index(2)
rows = sheet.nrows
columns = sheet.ncols
colorlist=['g','peru','b','darkviolet','k','r']
# labellist = ['random','first_by_dis','first_by_TAR','utility_nocluster','utility_cluster','bizhi_cluster']
linestylelist=['s','+','D','o','p','*']
my_x_ticks=hour
plt.xticks(my_x_ticks)
for i in range(1,rows):
    row_data = sheet.row_values(i)
    # plt.title('total utility')
    plt.xlabel('time')
    plt.ylabel('utility')
    plt.plot(hour,row_data,marker=linestylelist[i],markersize=5,label=labellist[i],color=colorlist[i],linewidth=1,linestyle='-')
plt.legend(loc=1)
x_major_locator=MultipleLocator(2)
ax=plt.gca()
ax.xaxis.set_major_locator(x_major_locator)
plt.show()

# 任务完成数量在时间变化下的比较    --- 旧金山
sheet = wb.sheet_by_index(3)
rows = sheet.nrows
columns = sheet.ncols
colorlist=['g','peru','b','darkviolet','k','r']
# labellist = ['random','first_by_dis','first_by_TAR','utility_nocluster','utility_cluster','bizhi_cluster']
linestylelist=['s','+','D','o','p','*']
my_x_ticks=hour
plt.xticks(my_x_ticks)
for i in range(rows):
    row_data = sheet.row_values(i)
    # plt.title('Total number of tasks completion')
    plt.xlabel('time')
    plt.ylabel('NoT')
    plt.plot(hour,row_data,marker=linestylelist[i],markersize=5,label=labellist[i],color=colorlist[i],linewidth=0.8,linestyle='-')
plt.legend(loc=1)
x_major_locator=MultipleLocator(2)
ax=plt.gca()
ax.xaxis.set_major_locator(x_major_locator)
plt.savefig(r'C:\Users\s-monster\Desktop\exp_pic\tasknum_time.pdf', bbox_inches='tight')
plt.show()


# 任务完成质量在不同参与者数量下的比较   --- 旧金山
sheet = wb.sheet_by_index(4)
rows = sheet.nrows
columns = sheet.ncols
width=6
x =np.arange(50,301,50)
plt.figure(figsize=(8,4))
# bmap = brewer2mpl.get_map('Set2', 'qualitative', 7)
# colors=cycler('color',bmap.mpl_colors)
# plt.rcParams['axes.prop_cycle'] = [colors]
colorlist=['#007eff','#00ffff','#7eff7e','#ffff00','#ff7e00','r']
# labellist = ['random','first_by_dis','first_by_TAR','utility_nocluster','utility_cluster','bizhi_cluster']
for i in range(rows):
    row_data = sheet.row_values(i)
    plt.bar(x=x+(i-2)*width,height=row_data,width=width-1,label=labellist[i],color=colorlist[i],ec='black',lw=.5)
plt.xlabel('The number of participants')
plt.ylabel('QoT')
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
# plt.rcParams["axes.grid"] = True
plt.legend()
plt.savefig(r'C:\Users\s-monster\Desktop\exp_pic\QoT_change_participant.pdf',bbox_inches="tight")
plt.show()

# 平均移动距离在不同的参与者数量下的比较 --- 旧金山
sheet = wb.sheet_by_index(5)
rows = sheet.nrows
columns = sheet.ncols
width=6
x =np.arange(50,301,50)
plt.figure(figsize=(8,4))
# bmap = brewer2mpl.get_map('Set2', 'qualitative', 7)
# colors=cycler('color',bmap.mpl_colors)
# plt.rcParams['axes.prop_cycle'] = [colors]
colorlist=['#007eff','#00ffff','#7eff7e','#ffff00','#ff7e00','r']
# labellist = ['random','first_by_dis','first_by_TAR','utility_nocluster','utility_cluster','bizhi_cluster']
for i in range(rows):
    row_data = sheet.row_values(i)
    plt.bar(x=x+(i-2)*width,height=row_data,width=width-1,label=labellist[i],color=colorlist[i],ec='black',lw=.5)
plt.xlabel('The number of participants')
plt.ylabel('ADT')
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
# plt.rcParams["axes.grid"] = True
plt.legend()
plt.savefig(r'C:\Users\s-monster\Desktop\exp_pic\distance_change_participant.pdf',bbox_inches="tight")
plt.show()

# 任务完成数量在不同的参与者数量下的比较  --- 旧金山
sheet = wb.sheet_by_index(7)
rows = sheet.nrows
columns = sheet.ncols
width=5
x =np.arange(50,301,50)
plt.figure(figsize=(8,4))
colorlist=['#007eff','#00ffff','#7eff7e','#ffff00','#ff7e00','r']
# labellist = ['random','first_by_dis','first_by_TAR','utility_nocluster','utility_cluster','bizhi_cluster']
for i in range(rows):
    row_data = sheet.row_values(i)
    plt.bar(x=x+(i-2)*width,height=row_data,width=width-1,label=labellist[i],color=colorlist[i],ec='black',lw=.5)
plt.xlabel('The number of participants')
plt.ylabel('NoT')
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

plt.legend()
plt.savefig(r'C:\Users\s-monster\Desktop\exp_pic\tasknums_change_participant.pdf',bbox_inches="tight")
plt.show()

# - ----------------------
# # 任务完成质量在不同的感知任务数量下的比较 ---旧金山
sheet = wb.sheet_by_index(8)
rows = sheet.nrows
columns = sheet.ncols
width=6
x =np.arange(50,301,50)
plt.figure(figsize=(8,4))
# bmap = brewer2mpl.get_map('Set2', 'qualitative', 7)
# colors=cycler('color',bmap.mpl_colors)
# plt.rcParams['axes.prop_cycle'] = [colors]
colorlist=['#007eff','#00ffff','#7eff7e','#ffff00','#ff7e00','r']
# labellist = ['random','first_by_dis','first_by_TAR','utility_nocluster','utility_cluster','bizhi_cluster']
for i in range(rows):
    row_data = sheet.row_values(i)
    plt.bar(x=x+(i-2)*width,height=row_data,width=width-1,label=labellist[i],color=colorlist[i],ec='black',lw=.5)
plt.xlabel('The number of tasks')
plt.ylabel('QoT')
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
# plt.rcParams["axes.grid"] = True
plt.legend()
plt.savefig(r'C:\Users\s-monster\Desktop\exp_pic\QoT_change_task.pdf',bbox_inches="tight")
plt.show()
#
# # 平均移动距离在不用的感知任务数量下的比较 --- 旧金山
sheet = wb.sheet_by_index(9)
rows = sheet.nrows
columns = sheet.ncols
width=6
x =np.arange(50,301,50)
plt.figure(figsize=(8,4))
# bmap = brewer2mpl.get_map('Set2', 'qualitative', 7)
# colors=cycler('color',bmap.mpl_colors)
# plt.rcParams['axes.prop_cycle'] = [colors]
colorlist=['#007eff','#00ffff','#7eff7e','#ffff00','#ff7e00','r']
# labellist = ['random','first_by_dis','first_by_TAR','utility_nocluster','utility_cluster','bizhi_cluster']
for i in range(rows):
    row_data = sheet.row_values(i)
    plt.bar(x=x+(i-2)*width,height=row_data,width=width-1,label=labellist[i],color=colorlist[i],ec='black',lw=.5)
plt.xlabel('The number of tasks')
plt.ylabel('ADT')
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
# plt.rcParams["axes.grid"] = True
plt.legend()
plt.savefig(r'C:\Users\s-monster\Desktop\exp_pic\distance_change_task.pdf',bbox_inches="tight")
plt.show()
#
# # 任务的完成数量在不同的感知任务数量下的比较---旧金山
sheet = wb.sheet_by_index(10)
rows = sheet.nrows
columns = sheet.ncols
width=5
x =np.arange(50,301,50)
plt.figure(figsize=(8,4))
colorlist=['#007eff','#00ffff','#7eff7e','#ffff00','#ff7e00','r']
# labellist = ['random','first_by_dis','first_by_TAR','utility_nocluster','utility_cluster','bizhi_cluster']
for i in range(rows):
    row_data = sheet.row_values(i)
    plt.bar(x=x+(i-2)*width,height=row_data,width=width-1,label=labellist[i],color=colorlist[i],ec='black',lw=.5)
plt.xlabel('The number of tasks')
plt.ylabel('NoT')
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

plt.legend()
plt.savefig(r'C:\Users\s-monster\Desktop\exp_pic\tasknums_change_task.pdf',bbox_inches="tight")
plt.show()

#任务的完成质量在不同的感知任务数量下比较 --- 北京
sheet = wb.sheet_by_index(11)
rows = sheet.nrows
columns = sheet.ncols
width=6
x =np.arange(50,301,50)
plt.figure(figsize=(8,4))
colorlist=['#007eff','#00ffff','#7eff7e','#ffff00','#ff7e00','r']
for i in range(rows):
    row_data = sheet.row_values(i)
    plt.bar(x=x+(i-2)*width,height=row_data,width=width-1,label=labellist[i],color=colorlist[i],ec='black',lw=.5)
plt.xlabel('The number of tasks')
plt.ylabel('QoT')
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
# plt.rcParams["axes.grid"] = True
plt.legend()
plt.savefig(r'C:\Users\s-monster\Desktop\exp_pic\QoT_change_task_beijing.pdf',bbox_inches="tight")
plt.show()


# 平均移动距离在不用的感知任务数量下的比较 --- 北京
sheet = wb.sheet_by_index(12)
rows = sheet.nrows
columns = sheet.ncols
width=6
x =np.arange(50,301,50)
plt.figure(figsize=(8,4))
colorlist=['#007eff','#00ffff','#7eff7e','#ffff00','#ff7e00','r']
for i in range(rows):
    row_data = sheet.row_values(i)
    plt.bar(x=x+(i-2)*width,height=row_data,width=width-1,label=labellist[i],color=colorlist[i],ec='black',lw=.5)
plt.xlabel('The number of tasks')
plt.ylabel('ADT')
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
# plt.rcParams["axes.grid"] = True
plt.legend()
plt.savefig(r'C:\Users\s-monster\Desktop\exp_pic\distance_change_task_beijing.pdf',bbox_inches="tight")
plt.show()

# 任务的完成数量在不同的感知任务数量下的比较---北京
sheet = wb.sheet_by_index(13)
rows = sheet.nrows
columns = sheet.ncols
width=5
x =np.arange(50,301,50)
plt.figure(figsize=(8,4))
colorlist=['#007eff','#00ffff','#7eff7e','#ffff00','#ff7e00','r']
for i in range(rows):
    row_data = sheet.row_values(i)
    plt.bar(x=x+(i-2)*width,height=row_data,width=width-1,label=labellist[i],color=colorlist[i],ec='black',lw=.5)
plt.xlabel('The number of tasks')
plt.ylabel('NoT')
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
plt.legend()
plt.savefig(r'C:\Users\s-monster\Desktop\exp_pic\tasknums_change_task_beijing.pdf',bbox_inches="tight")
plt.show()

# --------------------------------------------------------------------------------------------------------------------
# 任务的完成质量在不同的参与者数量下比较 --- 北京
sheet = wb.sheet_by_index(14)
rows = sheet.nrows
columns = sheet.ncols
width=6
x =np.arange(50,301,50)
plt.figure(figsize=(8,4))
colorlist=['#007eff','#00ffff','#7eff7e','#ffff00','#ff7e00','r']
for i in range(rows):
    row_data = sheet.row_values(i)
    plt.bar(x=x+(i-2)*width,height=row_data,width=width-1,label=labellist[i],color=colorlist[i],ec='black',lw=.5)
plt.xlabel('The number of participants')
plt.ylabel('QoT')
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
# plt.rcParams["axes.grid"] = True
plt.legend()
plt.savefig(r'C:\Users\s-monster\Desktop\exp_pic\QoT_change_participant_beijing.pdf',bbox_inches="tight")
plt.show()


# 平均移动距离在不用的参与者数量下的比较 --- 北京
sheet = wb.sheet_by_index(15)
rows = sheet.nrows
columns = sheet.ncols
width=6
x =np.arange(50,301,50)
plt.figure(figsize=(8,4))
colorlist=['#007eff','#00ffff','#7eff7e','#ffff00','#ff7e00','r']
for i in range(rows):
    row_data = sheet.row_values(i)
    plt.bar(x=x+(i-2)*width,height=row_data,width=width-1,label=labellist[i],color=colorlist[i],ec='black',lw=.5)
plt.xlabel('The number of participants')
plt.ylabel('ADT')
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
# plt.rcParams["axes.grid"] = True
plt.legend()
plt.savefig(r'C:\Users\s-monster\Desktop\exp_pic\distance_change_participant_beijing.pdf',bbox_inches="tight")
plt.show()

# 任务的完成数量在不同的参与者数量下的比较---北京
sheet = wb.sheet_by_index(16)
rows = sheet.nrows
columns = sheet.ncols
width=5
x =np.arange(50,301,50)
plt.figure(figsize=(8,4))
colorlist=['#007eff','#00ffff','#7eff7e','#ffff00','#ff7e00','r']
for i in range(rows):
    row_data = sheet.row_values(i)
    plt.bar(x=x+(i-2)*width,height=row_data,width=width-1,label=labellist[i],color=colorlist[i],ec='black',lw=.5)
plt.xlabel('The number of participants')
plt.ylabel('NoT')
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
plt.legend()
plt.savefig(r'C:\Users\s-monster\Desktop\exp_pic\tasknums_change_participant_beijing.pdf',bbox_inches="tight")
plt.show()
