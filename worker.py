from scheduling_manager import SchedulingManager
from flush_manager import FlushManager
from scheduling_parameters import SchedulingParameters


class Worker:
    def __init__(self):
        self.scheduling_manager = SchedulingManager()
        self.flush_manager = FlushManager(self.scheduling_manager)
        self.scheduling_parameters = SchedulingParameters.get_scheduling_parameters()

    def run_worker(self, job_log):
        time_unit = self.scheduling_parameters.time_unit
        simulation_start_time = self.scheduling_parameters.simulation_start_time
        queue_manager = self.scheduling_parameters.queue_manager
        # job log의 마지막 job까지 가져옴 & 직전에 delegate queue에 누적된 job이 없음
        if self.is_finished(job_log):
            return

        # submit time이 된 job들을 delegate queue에 submit
        queue_manager.submit_jobs(job_log, time_unit, simulation_start_time)

        # flush manager : 1) flush timing인지 검사 2) flush 수행
        if self.flush_manager.is_flush_condition_set():
            self.flush_manager.flush()

    def is_finished(self, job_log):
        delegate_queue = self.scheduling_parameters.queue_manager.get_delegate_queue()

        return len(job_log.jobs) == 0 and len(delegate_queue) == 0
