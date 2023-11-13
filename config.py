# -*- coding: utf-8 -*-

# public
# 参与者与任务生成的参数设置

sensor_name = ['摄像头(图像传感器）', '加速计', '磁强计(磁场传感器）', '陀螺仪', '接近传感器', 'GPS', '麦克风（声音传感器）', '光传感器', '温度传感器',
               '重力传感器', '距离传感器', '压力传感器', '湿度传感器', '压力传感器', '蓝牙', 'GSM', 'WIFI', '气压传感器', '海拔传感器', '指纹传感器',
               '紫外线传感器', '红外传感器', '心率传感器', '血氧传感器', '霍尔传感器', '计步传感器', '雷达传感器', '辐射检测传感器', 'NFC'
               ]
alpha = 0.5 # 权衡因子


# participant

v = 2  # 2m/s 一个成年人正常行走的速度在1.75-2m/s不等

sensor_num = 12 # 系统传感器的数目

left_workload = 5   # 参与者每个传感器的工作负载随机生成的左值
right_workload = 10 # 参与者每个传感器的工作负载随机生成的右值

left_pay = 2  # 参与者每个传感器的期望报酬随机生成的左值
right_pay = 5 # 参与者每个传感器的期望报酬随机生成的右值

# task
# 高斯分布随机生成感知任务需要的传感器数量
mu_sensor_num_of_task = 4  #  高斯分布的均值mu
sigma_sensor_num_of_task = 1  # 高斯分布的均值mu

left_need_people_low = 2   # 感知任务需要最少参与者数量随机生成的左值
right_need_people_low = 4 # 感知任务需要做少参与者数量随机生成的右值

left_need_people_high = 4  # 感知任务需要最多参与者数量随机生成的左值
right_need_people_high = 6 # 感知任务需要最多参与者数量随机生成的右值

# left_per_budget_range = 1
# right_per_budget_range = 3

left_per_budget_range = 2   # 感知任务使用每个传感器的预算随机生成的左值
right_per_budget_range = 4 # 感知任务使用每个传感器的预算随机生成的右值


# adjustTaskBudget

# left_suijiadd = 1
# right_suijiadd = 10
left_suijiadd = 5
right_suijiadd = 15