import math

def lines_intersect(p1, p2, p3, p4):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    denominator = (x4-x3)*(y1-y2) - (x1-x2)*(y4-y3)
    if denominator == 0:
        return True
    intersection_x = ((x2*y1-x1*y2)*(x4-x3)-(x4*y3-x3*y4)*(x2-x1))/denominator
    intersection_y = ((x2*y1-x1*y2)*(y4-y3)-(x4*y3-x3*y4)*(y2-y1))/denominator
    between_x = in_range(intersection_x, x1, x2)
    between_y = in_range(intersection_y, y1, y2)
    return between_x and between_y

def in_range(val, lower, upper):
    return val >= lower and val <= upper

def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def signed_basic_angle(angle):
    if in_range(angle, -math.pi/2, math.pi/2):
        basic = angle
    if in_range(angle, -math.pi, -math.pi/2) or angle > math.pi:
        basic = abs(angle)-math.pi
    if in_range(angle, math.pi/2, math.pi) or angle < -math.pi:
        basic = math.pi-abs(angle)
    return basic