import math

def lines_intersect(p1, p2, p3, p4):
    """Determines whether 2 lines intersect"""
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    denominator = (x4-x3)*(y1-y2) - (x1-x2)*(y4-y3)
    # If the denominator is 0, it means that the lines are parallel
    # or collinear – they are the same line
    # Since we will be looking at both diagonals of the wall square,
    # if the line is parallel to one diagonal, it will be perpendicular to the other
    # Therefore it is safer to say that it will intersect when the denominator is 0
    if denominator == 0:
        return True
    # Finds the intersection point between the 2 lines
    intersection_x = ((x2*y1-x1*y2)*(x4-x3)-(x4*y3-x3*y4)*(x2-x1))/denominator
    intersection_y = ((x2*y1-x1*y2)*(y4-y3)-(x4*y3-x3*y4)*(y2-y1))/denominator
    # If the intersection point falls within any of the line segments, the 2 line (segments) intersect
    between_x = in_range(intersection_x, x1, x2)
    between_y = in_range(intersection_y, y1, y2)
    return between_x and between_y

def in_range(val, lower, upper):
    """Determines whether a value is in range of [lower, upper]"""
    return val >= lower and val <= upper

def distance(p1, p2):
    """Determines the distance between 2 2D coordinates"""
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def signed_basic_angle(angle):
    """Finds the basic angle of any angle, while keeping the sign"""
    if in_range(angle, -math.pi/2, math.pi/2):
        basic = angle
    if in_range(angle, -math.pi, -math.pi/2) or angle > math.pi:
        basic = abs(angle)-math.pi
    if in_range(angle, math.pi/2, math.pi) or angle < -math.pi:
        basic = math.pi-abs(angle)
    return basic
