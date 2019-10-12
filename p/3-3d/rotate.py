import math

px = 150
py = 150


cx = 200
cy = 200


d = math.sqrt(math.pow((cy - py), 2) + math.pow((cx - px), 2))

theta = math.asin((cy - py) / d)

print(theta)

theta += 1
py = cy - d * math.sin(theta)

print(py)