from schedule.flush_policy.flush_policy import FlushPolicy
from scheduling_parameters import SchedulingParameters
from utils import cur_time


class DefaultFlushPolicy(FlushPolicy):
    def __init__(self, flush_manager, scheduling_manager):
        self.flush_manager = flush_manager
        self.scheduling_manager = scheduling_manager
        self.scheduling_parameters = SchedulingParameters.get_scheduling_parameters()

    def is_flush_condition_set(self):
        delegate_queue = self.scheduling_parameters.queue_manager.get_delegate_queue()
        flush_period = self.scheduling_parameters.flush_period
        time_unit = self.scheduling_parameters.time_unit
        latest_flush_time = self.flush_manager.get_latest_flush_time()
        elapsed_time_after_latest_flush = cur_time(time_unit) - latest_flush_time

        if len(delegate_queue) == 0:
            return False

        return elapsed_time_after_latest_flush > flush_period

    def flush(self):
        self.scheduling_manager.apply_scheduling_policy()
        self.flush_manager.renew_latest_flush_time()
