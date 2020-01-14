import os
from PIL import Image
import math


def are_intervals_overlap(I_1, W_1, I_2, W_2):
    if I_1 <= I_2 and I_1 + W_1 <= I_2:
        return False
    if I_1 >= I_2 + W_2 and I_1 + W_1 >= I_2 + W_2:
        return False
    return True

def interval_overlap(I_1, W_1, I_2, W_2):
    C_1 = I_1 + W_1/2
    C_2 = I_2 + W_2/2
    side = -1 if C_1 > C_2 else 1
    return side * max((W_1 + W_2)/2 - abs(C_1 - C_2), 0)

def dist(x1,y1,x2,y2):
    dx = x2-x1
    dy = y2-y1
    return math.sqrt(dx*dx + dy*dy)
