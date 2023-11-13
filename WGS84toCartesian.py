#!/usr/bin/python3

"""
Convert GPS position information to XYZ position information, and back.
Author: buaa_szx
time:   2022.1.25
Modified from the following code:
https://github.com/PX4/PX4-Autopilot/blob/master/src/lib/geo/geo.cpp
"""

import math
import numpy as np


class PositionConvert(object):
    CONSTANTS_RADIUS_OF_EARTH = 6371000.     # meters (m)


    def GPStoXY(self, lat, lon, ref_lat, ref_lon):
        # input GPS and Reference GPS in degrees
        # output XY in meters (m) X:North Y:East
        lat_rad = math.radians(lat)
        lon_rad = math.radians(lon)
        ref_lat_rad = math.radians(ref_lat)
        ref_lon_rad = math.radians(ref_lon)

        sin_lat = math.sin(lat_rad)
        cos_lat = math.cos(lat_rad)
        ref_sin_lat = math.sin(ref_lat_rad)
        ref_cos_lat = math.cos(ref_lat_rad)

        cos_d_lon = math.cos(lon_rad - ref_lon_rad)

        arg = np.clip(ref_sin_lat * sin_lat + ref_cos_lat * cos_lat * cos_d_lon, -1.0, 1.0)
        c = math.acos(arg)

        k = 1.0
        if abs(c) > 0:
            k = (c / math.sin(c))

        x = float(k * (ref_cos_lat * sin_lat - ref_sin_lat * cos_lat * cos_d_lon) * self.CONSTANTS_RADIUS_OF_EARTH)
        y = float(k * cos_lat * math.sin(lon_rad - ref_lon_rad) * self.CONSTANTS_RADIUS_OF_EARTH)

        return x, y

    def XYtoGPS(self,x, y, ref_lat, ref_lon):
        x_rad = float(x) / self.CONSTANTS_RADIUS_OF_EARTH
        y_rad = float(y) / self.CONSTANTS_RADIUS_OF_EARTH
        c = math.sqrt(x_rad * x_rad + y_rad * y_rad)

        ref_lat_rad = math.radians(ref_lat)
        ref_lon_rad = math.radians(ref_lon)

        ref_sin_lat = math.sin(ref_lat_rad)
        ref_cos_lat = math.cos(ref_lat_rad)

        if abs(c) > 0:
            sin_c = math.sin(c)
            cos_c = math.cos(c)

            lat_rad = math.asin(cos_c * ref_sin_lat + (x_rad * sin_c * ref_cos_lat) / c)
            lon_rad = (ref_lon_rad + math.atan2(y_rad * sin_c, c * ref_cos_lat * cos_c - x_rad * ref_sin_lat * sin_c))

            lat = math.degrees(lat_rad)
            lon = math.degrees(lon_rad)

        else:
            lat = math.degrees(ref_lat)
            lon = math.degrees(ref_lon)

        return lat, lon


if __name__ == '__main__':
    PC = PositionConvert()
    test = 4
    ref_lat = (473566094 / 1e7)
    ref_lon = (85190237 / 1e7)
    if test == 1:
        x = 0.5
        y = 1
        lat_new, lon_new = PC.XYtoGPS(x, y, ref_lat, ref_lon)
        x_new, y_new = PC.GPStoXY(lat_new, lon_new, ref_lat, ref_lon)
        print(x_new, y_new)
    elif test == 2:
        lat = 47.356616973876953
        lon = 8.5190505981445313
        x, y = PC.GPStoXY(lat, lon, ref_lat, ref_lon)
        lat_new, lon_new = PC.XYtoGPS(x, y, ref_lat, ref_lon)
        print(lat_new, lon_new)
    elif test == 3:
        x = 10000.0
        y = 0.0
        lat_new, lon_new = PC.XYtoGPS(x, y, ref_lat, ref_lon)
        print(ref_lat, ref_lon)
        print(lat_new, lon_new)
    elif test == 4:
        x = 0.0
        y = 10000.0
        lat_new, lon_new = PC.XYtoGPS(x, y, ref_lat, ref_lon)
        print(ref_lat, ref_lon)
        print(lat_new, lon_new)
