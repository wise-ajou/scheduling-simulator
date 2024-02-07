from scheduling_parameters import SchedulingParameters
from timer import cur_time
from scheduling_manager import SchedulingManager

class FlushManager():
    def __init__(self, scheduling_manager):
        self.scheduling_manager = scheduling_manager
        self.scheduling_parameters = SchedulingParameters.get_scheduling_parameters()
        self.flush_count = 0
        self.latest_flush_time = cur_time(self.scheduling_parameters.time_unit)

    def is_flush_condition_set(self):
        delegate_queue = self.scheduling_parameters.queue_manager.get_delegate_queue()
        time_unit = self.scheduling_parameters.time_unit
        flush_period = self.scheduling_parameters.flush_period

        if len(delegate_queue) == 0:
            return False
        
        elapsed_time_after_latest_flush = cur_time(time_unit) - self.latest_flush_time
        
        return elapsed_time_after_latest_flush >= flush_period

    def flush(self):
        time_unit = self.scheduling_parameters.time_unit
        self.scheduling_manager.apply_scheduling_policy()

        self.latest_flush_time = cur_time(time_unit)
        self.flush_count += 1
