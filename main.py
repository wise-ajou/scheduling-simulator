from cluster import Cluster
from job import JobLog
from queue_manager import QueueManager
from schedule.flush_manager import FlushManager
from schedule.scheduling_manager import SchedulingManager
from scheduling_parameters import SchedulingParameters
from utils import parse_args, sleep
from schedule.worker import Worker
from schedule.scheduler import Scheduler
from monitor import run_monitor
from queue import Queue

import threading

if __name__ == '__main__':
    args = parse_args()

    JOB_LOG_DIR_PATH = './log/'
    RESULT_DIR_PATH = './results/'
    cluster_file_path = args.cluster
    job_log_file_path = JOB_LOG_DIR_PATH + args.job_log
    result_file_path = RESULT_DIR_PATH + args.result

    # cluster: Variable about which host the queue has assigned
    cluster = Cluster(cluster_file_path)
    # represents which hosts each queue contains (2-d)
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

    scheduling_manager = SchedulingManager()
    flush_manager = FlushManager(scheduling_manager)
    worker = Worker(scheduling_manager, flush_manager)
    scheduler = Scheduler()

    stop_event = threading.Event()
    monitor_thread = threading.Thread(
        target=run_monitor,
        args=(cluster, host_configure_list, result_file_path, stop_event, args.monitoring_period, args.time_unit)
    )

    monitor_thread.start()

    while len(job_log.jobs) > 0 or (scheduler.fin_job_num < total_job_num):
        worker.run_worker(job_log)
        scheduler.run_fetcher()

        for queue_type in range(cluster.num_queue_types):
            scheduler.run_dispatcher(host_configure_list, queue_type)

    sleep(args.monitoring_period, args.time_unit)
    stop_event.set()
    monitor_thread.join()

    # results 엑셀화 추가

    print('+++++++++++ simulation finished +++++++++++')
