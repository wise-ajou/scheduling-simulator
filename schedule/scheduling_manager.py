from schedule.scheduling_policy.fcfs_policy import FcfsPolicy
from scheduling_parameters import SchedulingParameters


class SchedulingManager:
    def __init__(self):
        self.scheduling_parameters = SchedulingParameters.get_scheduling_parameters()
        self.scheduling_policy = self.set_scheduling_policy()

    def set_scheduling_policy(self):
        scheduling_policy = self.scheduling_parameters.scheduling_policy

        if scheduling_policy == 'fcfs':
            return FcfsPolicy()
    def apply_scheduling_policy(self):
        self.scheduling_policy.apply_policy()
