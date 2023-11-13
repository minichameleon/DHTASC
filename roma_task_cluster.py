# -*- coding: utf-8 -*-

"""
question
"""
import math
import numpy as np
from sklearn.cluster import DBSCAN
import json
import random
import copy

import config

# 任务进行聚类
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


def caculateDisBetweenTwoPoint(matrix: np.ndarray) -> np.ndarray:
    """
    计算数据集中的点的距离矩阵
    :param matrix: type(matrix)= np.ndarry,一个以经纬度方式存放的位置矩阵，第一列表示纬度，第二列表示经度
    :return: distance 各个点之间距离，size(distance) = (n,n),单位为km
    """
    n, m = matrix.shape
    distance = np.zeros( shape=(n, n) )
    for i in range( n ):
        for j in range( n ):
            if i == j:
                continue
            else:
                distance[i][j] = getDistance( matrix[i][0], matrix[i][1], matrix[j][0], matrix[j][1] )

    return distance

def getNumPerClass(labelseq):
    minn = min( labelseq )
    maxn = max( labelseq )
    #最小类为-1时 flag为1，如果最小类大于1，flag则为0
    flag = 1
    if minn == -1:
        res = [0 for i in range( maxn + 2 )]
        classperid = [[] for i in range( maxn + 2 )]
        for i in labelseq:
            res[i + 1] = res[i + 1] + 1
            classperid[i + 1].append(i)
    else:
        res = [0 for i in range( maxn + 1 )]
        classperid = [[] for i in range(maxn+1)]
        for i in labelseq:
            res[i] = res[i] + 1
            classperid[i].append(i)
            flag = 0
    res = np.array( res )

    return res,classperid,flag


def judge(labelseq,maxPts):
    """
    判断分类结果是否已经满足要求：即每类2到5个点
    :param labelseq:
    :return:
    """
    res,classperid,flag = getNumPerClass(labelseq)
    dayu5_index = np.argwhere(res>maxPts)

    reclusterpointid = classperid[dayu5_index]
    classxuhao = dayu5_index
        # 最小的类是-1，即存在独立点

    # if not (len(dayu5_index)==1 and dayu5_index[0]==0):
    #     classxuhao = [y-1 for y in dayu5_index[1:]]
    #     for x in range(len(labelseq)):
    #         if labelseq[x] in classxuhao:
    #             reclusterpointid.append(x)
    return reclusterpointid,classxuhao,flag


def specifiesSizeOfCluster(filename2,eps,minPts,maxPts,flag=0):
    """
    * 对roma数据进行处理
    * 使用DBSCAN对这些地理位置进行密度聚类
    * 并限制聚集团的规模为2-5，即如果某些任务被聚在一起，那么该任务集合的大小应当被调整为2-5
    * 使用dbscan聚类算法，不用确定类的数目
    :return:
    """
    # data = readdata(filename,flag)
    with open(filename2,'r',encoding='utf-8') as f:
        TASK = json.load( f )

    # 获得经纬度坐标数据
    changdu = len(TASK)
    data = np.zeros( shape=(changdu, 3), dtype="float32" )
    for xi in range(changdu):
        data[xi][0] = TASK[str(xi)][0][0]  # 纬度
        data[xi][1] = TASK[str(xi)][0][1]  # 经度
        data[xi][2] = TASK[str(xi)][0][2]  # 时间

    DIS = caculateDisBetweenTwoPoint(data)

    # DBSCAN聚类
    db = DBSCAN( eps=eps, min_samples=minPts, metric="precomputed" ).fit( DIS )
    labels = db.labels_
    print(f"db后labels:{0}",labels)
    maxw = max(labels)
    minw = min(labels)

    NumPerClass=getNumPerClass(labels)[0][1:] #index为0的是-1,去掉后，index 0将对应类别0
    # 类内点数量超过maxPts的类别名称
    classidd = np.argwhere(NumPerClass>6) # 这里数组的下标和类的标签id是一一对应的
    for i in classidd:
        pointid = []
        for  j in range(len(labels)):
            if labels[j] ==i:
                pointid.append(j)
        pointidlen = len(pointid)
        sim = [[0 for x in range(pointidlen)] for y in range(pointidlen)] # 相似度矩阵
        for j1 in range(pointidlen):
            ttemp = set( TASK[str( pointid[j1] )][1] )
            for j2 in range(pointidlen):
                if j1==j2:
                    sim[j1][j2]=0
                else:
                    ttemp2 = set( TASK[str( pointid[j2] )][1] )
                    a = ttemp & ttemp2
                    b = ttemp | ttemp2
                    if len(b) == 0:
                        sim[j1][j2] = 0
                    else:
                        sim[j1][j2] = len( a ) / len( b )
        # 计算需要划分为几组
        zushu = pointidlen//5
        yushu = pointidlen%5
        clusterover = []
        tempres = []
        sss = set(range(pointidlen))
        for zu in range(zushu):
            suijiid = random.sample( sss, 1 )
            zk_t = np.array(copy.copy(sim[suijiid[0]]))
            zk = np.argsort(-zk_t)
            zk1 = suijiid

            for zz in zk:
                if len(zk1)<5:
                    if zz not in tempres:
                        zk1.append(zz)
                else:
                    break

            clusterover.append(zk1)
            tempres=tempres+zk1
            sss = sss-set(zk1)
        if yushu!=0:
            clusterover.append(list(sss))
            zushu = zushu + 1
        # 对新生成的类打上标签，原来的标签加上新生成的标签。
        biaoqian  = list(i) + list(range(maxw+1,maxw+zushu))
        maxw = maxw+zushu-1
        # for p in pointid:
        #     for px in range(zushu):
        #         if p in clusterover[px]:
        #             labels[p] = biaoqian[px]
        #             break
        for px in range(len(biaoqian)):
            for p in clusterover[px]:
                labels[pointid[p]] = biaoqian[px]

    return labels



xuhao = ['06', '07', '10', '12', '16', '18', '19', '20', '23']

for xh in xuhao:
    read_file_name = "roma\\02-05-" + xh + '.json'
    write_file_name_cluster = "roma\\02-05-" + xh + "_cluster.json"
    write_file_name_bc = "roma\\02-05-" + xh + "bc.json"
    #
    res_label = list(specifiesSizeOfCluster( read_file_name, 0.25, 2, 5))
    with open(read_file_name,'r',encoding='utf-8') as rf:
        orgin = json.load(rf)
    orgin_no_c = copy.deepcopy(orgin)
    changdu = len(orgin)
    adjust_budget ={}
    for i in range(changdu):
        if res_label[i]!=-1:
            if str(res_label[i]) not in adjust_budget.keys():
                adjust_value = random.randint(config.left_suijiadd,config.right_suijiadd)
                orgin[str( i )][2] = orgin[str( i )][2] + adjust_value
                orgin_no_c[str( i )][2] = orgin_no_c[str( i )][2] + adjust_value
                adjust_budget[str(res_label[i])] = -adjust_value
            else:
                orgin[str( i )][2] = orgin[str( i )][2] + adjust_budget[str(res_label[i])]
                orgin_no_c[str( i )][2] = orgin_no_c[str( i )][2] + adjust_budget[str( res_label[i] )]
                adjust_budget.pop(str(res_label[i]))
        orgin[str(i)][0].append(str(res_label[i]))
        orgin_no_c[str( i )][0].append(-1)
        print(f"cluster:{orgin[str(i)][0]},no:{orgin_no_c[str( i )][0]}")
    with open(write_file_name_cluster,'w',encoding='utf-8') as wf:
        json.dump(orgin,wf)
    with open(write_file_name_bc,'w',encoding='utf-8') as wf:
        json.dump(orgin_no_c,wf)



#   随机选择任务和参与者随机将其分别分为 50 100 150 200 250 300个
xuhao = ['07','10','16','20']
for xh in xuhao:
    # 拼接数据文件名称
    read_file_name_bc = "roma\\02-05-" + xh + "bc.json"
    read_file_name_cluster = "roma\\02-05-" + xh + "_cluster.json"
    read_file_name_p = "roma\\02-05-" + xh + "_p.json"
    with open(read_file_name_bc,'r',encoding='utf-8') as rf:
        Task_bc = json.load(rf)
    with open(read_file_name_cluster,'r',encoding='utf-8') as rf:
        Task_cluster = json.load(rf)

    with open(read_file_name_p,'r',encoding='utf-8') as rf:
        participant = json.load(rf)

    task_len = len(Task_bc)
    participant_len = len(participant)
    for i in range(50,301,50):
        s_id_task = random.sample(list(range(task_len)),i)
        s_id_participant = random.sample( list( range( participant_len ) ), i )
        write_file_name_bc = 'roma_gen\\change_task\\task_'+str(i)+'\\02-05-' + xh + '_bc.json'
        write_file_name_cluster = 'roma_gen\\change_task\\task_'+str(i)+'\\02-05-' + xh + '_cluster.json'
        write_file_name_p = 'roma_gen\\change_participant\\participant_' + str( i ) + '\\02-05-' + xh +'_p.json'

        write1_bc_content = {}
        write_cluster_content = {}
        write_participant_content = {}
        for j in range(i):
            write1_bc_content[str(j)] = Task_bc[str(s_id_task[j])]
            write_cluster_content[str(j)] = Task_cluster[str(s_id_task[j])]
            write_participant_content[str(j)] = participant[str(s_id_participant[j])]

        with open(write_file_name_bc,'w',encoding='utf-8') as wf:
            json.dump(write1_bc_content,wf)
        with open(write_file_name_cluster,'w',encoding='utf-8') as wf:
            json.dump(write_cluster_content,wf)
        with open(write_file_name_p,'w', encoding='utf-8') as wf:
            json.dump(write_participant_content,wf)


