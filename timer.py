import time
import math


def cur_time(time_unit):
    now = math.floor(time.time_ns() / 1000000) if time_unit == 'ms' else math.floor(time.time())
    return now
