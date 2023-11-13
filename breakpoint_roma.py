# -*- coding: utf-8 -*-

"""
question
"""
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import xlrd

save_path ='图片\\'
wb = xlrd.open_workbook('res_roma.xlsx')
sheet_num = wb.nsheets
sheet_namess = wb.sheet_names()

colorlist= ['#95a2ff', '#fa8080', '#ffc076', '#fae768','#87e885', '#3cb9fc']
labellist = ['RTA','DTFTA','QFTA','EFTA','ADHTA-LW','ADHTA-PD']
linestylelist=['s','+','D','o','p','*']


# sheet = wb.sheet_by_index(2)
# rows = sheet.nrows
# columns = sheet.ncols
# width=6
#
# savename = save_path+"distance_change_task_roma.svg"
# xlabel_text = '任务数量'
#
# x =np.arange(50,301,50)
# f, (ax, ax2) = plt.subplots(2, 1, sharex=True,figsize = (8, 5))
# plt.subplots_adjust(wspace=0, hspace=0.08)  # 设置 子图间距
# for i in range(rows):
#     row_data = sheet.row_values(i)
#     ax.bar(x=x+(i-2)*width,height=row_data,width=width-1,label=labellist[i],color=colorlist[i],ec='black',lw=.5)
#     ax2.bar(x=x + (i - 2) * width, height=row_data, width=width - 1, label=labellist[i], color=colorlist[i], ec='black',
#            lw=.5)
#
# ax.set_ylim(20, 30)  # outliers only
# ax2.set_ylim(0, 5)  # most of the data
#
# ax.spines['bottom'].set_visible(False)
# ax2.spines['top'].set_visible(False)
#
# ax.xaxis.tick_top()
# ax.tick_params(labeltop='off')  # don't put tick labels at the top
# ax2.xaxis.tick_bottom()
#
# d = .015  # how big to make the diagonal lines in axes coordinates
# kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
# ax.plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
# ax.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal
#
# kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
# ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
# ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal
#
# ax.tick_params(labelsize=13)
# ax2.tick_params(labelsize=13)
# font2 = {'family' : 'SimHei',
# 'weight' : 'normal',
# 'size'  : 14,
# }
#
# plt.xlabel(xlabel_text,font2)
# plt.ylabel('ATD',font2,y=1)
# plt.rcParams["font.sans-serif"] = ["SimHei"]
# plt.rcParams["axes.unicode_minus"] = False
# ax.legend(loc=1)
# plt.savefig(savename,bbox_inches="tight",dpi=600,format='svg')
# plt.show()


# -------------------------------------------------------------------



sheet = wb.sheet_by_index(5)
rows = sheet.nrows
columns = sheet.ncols
width=6

savename = save_path+"distance_change_participant_roma.svg"
xlabel_text = '参与者数量'

x =np.arange(50,301,50)
f, (ax, ax2) = plt.subplots(2, 1, sharex=True,figsize = (8, 5))
plt.subplots_adjust(wspace=0, hspace=0.08)  # 设置 子图间距
for i in range(rows):
    row_data = sheet.row_values(i)
    ax.bar(x=x+(i-2)*width,height=row_data,width=width-1,label=labellist[i],color=colorlist[i],ec='black',lw=.5)
    ax2.bar(x=x + (i - 2) * width, height=row_data, width=width - 1, label=labellist[i], color=colorlist[i], ec='black',
           lw=.5)

ax.set_ylim(20, 30)  # outliers only
ax2.set_ylim(0, 6)  # most of the data

ax.spines['bottom'].set_visible(False)
ax2.spines['top'].set_visible(False)

ax.xaxis.tick_top()
ax.tick_params(labeltop='off')  # don't put tick labels at the top
ax2.xaxis.tick_bottom()

d = .015  # how big to make the diagonal lines in axes coordinates
kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
ax.plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
ax.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal

kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

ax.tick_params(labelsize=13)
ax2.tick_params(labelsize=13)
font2 = {'family' : 'SimHei',
'weight' : 'normal',
'size'  : 14,
}

plt.xlabel(xlabel_text,font2)
plt.ylabel('ATD',font2,y=1)
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
ax.legend(loc=1)
plt.savefig(savename,bbox_inches="tight",dpi=600,format='svg')
plt.show()
