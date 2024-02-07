from scheduling_parameters import SchedulingParameters
from timer import cur_time


class Scheduler:
    def __init__(self):
        self.scheduling_parameters = SchedulingParameters.get_scheduling_parameters()
        self.start_time = cur_time(self.scheduling_parameters.time_unit)
        self.fin_job_num = 0

    def run_fetcher(self):
        queue_manager = self.scheduling_parameters.queue_manager
        waiting_job_queues = queue_manager.get_waiting_job_queues()
        submitted_job_queue = queue_manager.get_submitted_job_queue()

        for job in submitted_job_queue:
            waiting_job_queues[job.queue_type].append(job)

        submitted_job_queue.clear()

    def run_dispatcher(self, host_configure_list, queue_type):
        queue_manager = self.scheduling_parameters.queue_manager
        time_unit = self.scheduling_parameters.time_unit
        temp_waiting_job_queue = []
        waiting_job_queue = queue_manager.get_waiting_job_queues()[queue_type]

        for job in waiting_job_queue:
            req_core = job.required_num_cores
            queue_type = job.queue_type

            for i in range(len(host_configure_list[queue_type])):
                if host_configure_list[queue_type][i].avail_num_cores >= req_core:
                    host_configure_list[queue_type][i].avail_num_cores -= req_core
                    job.alloc_host = i
                    job.execute_start_time = cur_time(time_unit)
                    # waiting time 계산
                    job.waiting_time = job.execute_start_time - job.submitted_time

                    queue_manager.get_executing_job_queues()[queue_type].append(job)

                    break

                if i == (len(host_configure_list[queue_type]) - 1):
                    temp_waiting_job_queue.append(job)

        waiting_job_queue.clear()

        for job in temp_waiting_job_queue:
            waiting_job_queue.append(job)
        temp_waiting_job_queue.clear()

        self.execute_job(queue_type)
        self.release_resource(host_configure_list, queue_type)

    def execute_job(self, queue_type):
        time_unit = self.scheduling_parameters.time_unit
        executing_job_queue = self.scheduling_parameters.queue_manager.get_executing_job_queues()[queue_type]
        finished_job_queue = self.scheduling_parameters.queue_manager.get_finished_job_queues()[queue_type]
        temp_executing_job_queue = []

        for job in executing_job_queue:
            cur = cur_time(time_unit)
            cur_runtime = cur - job.execute_start_time
            is_execution_finished = True if (cur_runtime >= job.runtime) else False

            if is_execution_finished:
                finished_job_queue.append(job)
            else:
                temp_executing_job_queue.append(job)

        executing_job_queue.clear()
        for job in temp_executing_job_queue:
            executing_job_queue.append(job)
        # executing_job_queue = temp_executing_job_queue[:]
        temp_executing_job_queue.clear()

    def release_resource(self, host_configure_list, queue_type):
        finished_job_queue = self.scheduling_parameters.queue_manager.get_finished_job_queues()[queue_type]
        fin_job_list = []

        for job in finished_job_queue:
            host_configure_list[queue_type][job.alloc_host].avail_num_cores += job.required_num_cores
            fin_job_list.append(job)
            self.fin_job_num += 1

        finished_job_queue.clear()
