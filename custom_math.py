import math

def move_curve(p1, p2, p3, p4, t):
        t = t / 100
        x = ((-t**3 + 2*t**2 - t)*p1[0] + (3*t**3 - 5*t**2 + 2)*p2[0]
             + (-3*t**3 + 4*t**2 + t)*p3[0] + (t**3 - t**2)*p4[0])/2
        y = ((-t**3 + 2*t**2 - t)*p1[1] + (3*t**3 - 5*t**2 + 2)*p2[1]
             + (-3*t**3 + 4*t**2 + t)*p3[1] + (t**3 - t**2)*p4[1])/2
        return x, y


def move_line(start, end, t):
    t = t / 100
    x = (1 - t) * start[0] + t * end[0]
    y = (1 - t) * start[1] + t * end[1]
    return x, y


def angle_between(start, dest):
    hypoteneus = math.sqrt((dest[0] - start[0])**2 + (dest[1] - start[1])**2)
    result_cos = (dest[0] - start[0])/hypoteneus

    radian = math.acos(result_cos)
    angle = math.degrees(radian)

    if dest[1] < start[1]:
        angle = 360 - angle

    return angle