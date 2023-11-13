# -*- coding: utf-8 -*-

"""
计算两个位置之间的距离
"""
import math

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
    lat1 = float(lat1)
    lng1 = float(lng1)
    lat2 = float(lat2)
    lng2 = float(lng2)
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


if __name__ == '__main__':
    # 北京到上海的直线距离
    BJ_lat = '39.913385'
    BJ_lng = '116.400819'
    SH_lat = '31.223704'
    SH_lng = '121.475024'
    dis = getDistance(BJ_lat,BJ_lng,SH_lat,SH_lng)
    print(f"北京到上海的直线距离为{dis}km")