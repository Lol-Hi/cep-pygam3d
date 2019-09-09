import math

def lines_intersect(p1, p2, p3, p4):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    denominator = (x4-x3)*(y1-y2) - (x1-x2)*(y4-y3)
    if denominator == 0:
        return True
    ta = ((y3-y4)*(x1-x3) + (x4-x3)*(y1-y3))/denominator
    tb = ((y1-y2)*(x1-x3) + (x2-x1)*(y1-y3))/denominator
    return in_range(ta, 0, 1) and in_range(tb, 0, 1)

def in_range(val, lower, upper):
    return val >= lower and val <= upper
