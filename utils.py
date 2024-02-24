import argparse
import math
import time


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cluster", type=str, default="cluster")
    parser.add_argument("--job_log", type=str)
    parser.add_argument("--result", type=str)
    parser.add_argument("--scheduling_algorithm", type=str, default="fcfs")
    parser.add_argument("--initial_flush_period", type=int, default="2000")
    parser.add_argument("--monitoring_period", type=int, default="3000")
    parser.add_argument("--time_unit", type=str, default="ms")
    args = parser.parse_args()

    return args


def cur_time(time_unit):
    now = (
        math.floor(time.time_ns() / 1000000)
        if time_unit == "ms"
        else math.floor(time.time())
    )
    return now


def sleep(sleep_time, time_unit):
    sleep_time_sec = (sleep_time / 1000) if time_unit == "ms" else sleep_time
    time.sleep(sleep_time_sec)
