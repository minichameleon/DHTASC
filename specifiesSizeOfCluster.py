# -*- coding: utf-8 -*-
import copy
import pathlib

import numpy as np
import math
from sklearn.cluster import DBSCAN
import json
import random
"""
将感知任务以地理位置聚类
DBSCAN
"""


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


def readdata(filename: str,flag) -> np.ndarray:
    """
    从filename中读取位置点的经纬度
    :param filename: 存储经纬度的文件名   str
     :return: 存储经纬度的ndarray数组 n*2
    """
    if flag == 0:
        try:
            with open( filename, 'r', encoding='utf-8' ) as f:
                lines = f.readlines( )
                number = len( lines )
                data = np.zeros( shape=(number, 3), dtype="float32" )
                for i in range( number ):
                    temp = lines[i].strip( ).split( ',' )
                    data[i][0] = temp[0]  # 纬度
                    data[i][1] = temp[1]  # 经度
                    data[i][2] = temp[2]  # 时间
        except FileNotFoundError:
            print("文件不存在")
    elif flag==1:
        try:
            with open(filename,'r',encoding='utf-8') as f:
                lines = json.load(f)
                number = len(lines)
                data = np.zeros( shape=(number, 3), dtype="float32" )
                for i in range(number):
                    data[i][0] = lines[str(i)][0][0]
                    data[i][1] = lines[str(i)][0][1]
                    data[i][2] = lines[str(i)][0][2]
        except FileNotFoundError:
            print("文件不存在")
    return data

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


def specifiesSizeOfCluster(filename,filename2,eps,minPts,maxPts,flag=0):
    """
    * 使用DBSCAN对这些地理位置进行密度聚类
    * 并限制聚集团的规模为2-5，即如果某些任务被聚在一起，那么该任务集合的大小应当被调整为2-5
    * 使用dbscan聚类算法，不用确定类的数目
    :return:
    """
    data = readdata(filename,flag)

    DIS = caculateDisBetweenTwoPoint(data)

    # DBSCAN聚类
    db = DBSCAN( eps=eps, min_samples=minPts, metric="precomputed" ).fit( DIS )
    labels = db.labels_
    print(f"db后labels:{0}",labels)
    maxw = max(labels)
    minw = min(labels)

    with open(filename2,'r',encoding='utf-8') as f:
        TASK = json.load( f )

    NumPerClass=getNumPerClass(labels)[0][1:] #index为0的是-1,去掉后，index 0将对应类别0
    # 类内点数量超过maxPts的类别名称
    classidd = np.argwhere(NumPerClass>6) # 这里数组的下标和类的标签id是一一对应的
    for i in classidd:
        pointid = []
        for  j in range(len(labels)):
            if labels[j] ==i:
                pointid.append(j)
        pointidlen = len(pointid)
        sim = [[0 for x in range(pointidlen)] for y in range(pointidlen)]
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




if __name__ == '__main__':

    for bai in range(65, 70):
        for ge in range(1, 25):
            if ge ==1:
                continue
            if ge <= 9:
                addr = 'd100data_end\\' + str(bai) + '0' + str(ge) + '_80.txt'
                addr1 = 'newdata_d100data_end_with_task\\' + str(bai) + '0' + str(ge) + '_80.json'
                writename1 = 'newdata_d100data_end_with_task\\' + str(bai) + '0' + str(ge) + '_80.txt'
                # addr1 = 'ddd\\' + str( bai ) + '0' + str( ge ) + '.json'
                # writename1 = 'ddd\\' + str( bai ) + '0' + str( ge ) + '.txt'
            else:
                addr = 'd100data_end\\' + str(bai) + str(ge) + '.txt'
                addr1 = 'newdata_d100data_end_with_task\\' + str(bai) + str(ge) + '_100.json'
                writename1 = 'newdata_d100data_end_with_task\\' + str(bai) + str(ge) + '_100.txt'
                # addr1 = 'ddd\\' + str( bai ) + str( ge ) + '.json'
                # writename1 = 'ddd\\' + str( bai ) + str( ge ) + '.txt'
            # 如果构造的文件路径不存在，在继续下一个
            filepathx = pathlib.Path(addr)
            if not filepathx.exists():
                continue
            # addr = 'd100data_end/6501.txt'
            clusterRes = specifiesSizeOfCluster(addr,addr1,0.25,3,5)
            ress = getNumPerClass(clusterRes)
            with open( addr1, 'r', encoding='utf-8' ) as f:
                TASK1 = json.load( f )
            for t in range(len(TASK1)):
                TASK1[str(t)][0].append(str(clusterRes[t]))
            print(ress[0])
            print(type(TASK1))

            with open( writename1, 'w', encoding='utf-8' ) as wf2:
                json.dump( TASK1, wf2 )
