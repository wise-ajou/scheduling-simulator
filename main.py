from cluster import Cluster
from job import JobLog
from queue_manager import QueueManager
from scheduling_parameters import SchedulingParameters
from worker import Worker
from scheduler import Scheduler
from monitor import run_monitor
from queue import Queue

import threading
import time
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cluster", type=str, default="cluster")
    parser.add_argument("--job_log", type=str)
    parser.add_argument("--result", type=str)
    parser.add_argument("--scheduling_algorithm", type=str, default="fcfs")
    parser.add_argument("--initial_flush_period", type=int, default="2000")
    parser.add_argument("--time_unit", type=str, default="ms")
    args = parser.parse_args()

    return args


if __name__ == '__main__':
    args = parse_args()

    JOB_LOG_DIR_PATH = './log/'
    RESULT_DIR_PATH = './results/'
    cluster_file_path = args.cluster
    job_log_file_path = JOB_LOG_DIR_PATH + args.job_log
    result_file_path = RESULT_DIR_PATH + args.result

    # cluster: Variable about which host the queue has assigned
    cluster = Cluster(cluster_file_path)

    # each queue가 어떤 호스트를 가지고 있는지에 대한 정보
    host_configure_list = [[] for i in range(cluster.num_queue_types)]

    for host in cluster.hosts:
        host_configure_list[host.queue_type].append(host)

    job_log = JobLog(job_log_file_path)
    total_job_num = len(job_log.jobs)

    queue = Queue(cluster.num_queue_types)
    queue_manager = QueueManager(queue)

    scheduling_parameters = SchedulingParameters(
        args.scheduling_algorithm,
        args.initial_flush_period,
        host_configure_list,
        queue_manager,
        args.time_unit
    )

    worker = Worker()
    scheduler = Scheduler()

    stop_event = threading.Event()
    monitor_thread = threading.Thread(
        target=run_monitor,
        args=(cluster, host_configure_list, result_file_path, stop_event)
    )

    monitor_thread.start()

    while len(job_log.jobs) > 0 or (scheduler.fin_job_num < total_job_num):
        worker.run_worker(job_log)
        scheduler.run_fetcher()

        for queue_type in range(cluster.num_queue_types):
            scheduler.run_dispatcher(host_configure_list, queue_type)

    time.sleep(3)
    stop_event.set()
    monitor_thread.join()

    # results 엑셀화 추가

    print('+++++++++++ simulation finished +++++++++++')
