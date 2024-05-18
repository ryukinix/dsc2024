from math import sin, cos, radians
import numpy


def angle_between(p1, p2):
    long1, lat1 = p1
    long2, lat2 = p2
    dLon = (long2 - long1)
    x = cos(radians(lat2)) * sin(radians(dLon))
    y = cos(radians(lat1)) * sin(radians(lat2)) - sin(radians(lat1)) * cos(radians(lat2)) * cos(radians(dLon))
    angle = numpy.arctan2(x, y)
    angle = numpy.degrees(angle)

    # HACK: doesn't makes sense, but works
    angle = abs(angle - 90)

    return angle
