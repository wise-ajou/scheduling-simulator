from schedule.scheduling_policy.scheduling_policy import SchedulingPolicy
from scheduling_parameters import SchedulingParameters


class FcfsPolicy(SchedulingPolicy):

    def __init__(self):
        self.scheduling_parameters = SchedulingParameters.get_scheduling_parameters()

    def apply_policy(self):
        queue_manager = self.scheduling_parameters.queue_manager
        delegate_queue = queue_manager.get_delegate_queue()
        submitted_job_queue = queue_manager.get_submitted_job_queue()

        for i in range(len(delegate_queue)):
            job = delegate_queue[i]
            submitted_job_queue.append(job)

        delegate_queue.clear()
