from schedule.flush_policy.default_flush_policy import DefaultFlushPolicy
from scheduling_parameters import SchedulingParameters
from utils import cur_time


class FlushManager:
    def __init__(self, scheduling_manager):
        self.scheduling_manager = scheduling_manager
        self.scheduling_parameters = SchedulingParameters.get_scheduling_parameters()
        self.flush_count = 0
        self.latest_flush_time = cur_time(self.scheduling_parameters.time_unit)
        self.flush_policy = self.set_flush_policy()

    def set_flush_policy(self):
        scheduling_policy = self.scheduling_parameters.scheduling_policy

        if scheduling_policy == 'fcfs':
            return DefaultFlushPolicy(self, self.scheduling_manager)

    def get_flush_count(self): return self.flush_count
    def add_flush_count(self): self.flush_count += 1
    def get_latest_flush_time(self): return self.latest_flush_time
    def renew_latest_flush_time(self): self.latest_flush_time = cur_time(self.scheduling_parameters.time_unit)

    def is_flush_condition_set(self):
        return self.flush_policy.is_flush_condition_set()

    def flush(self):
        self.flush_policy.flush()
