from scheduling_parameters import SchedulingParameters


class SchedulingManager():
    def __init__(self):
        self.scheduling_parameters = SchedulingParameters.get_scheduling_parameters()

    def apply_scheduling_policy(self):
        scheduling_algorithm = self.scheduling_parameters.scheduling_algorithm

        if scheduling_algorithm == 'fcfs':
            self.apply_fcfs_policy()

    def apply_fcfs_policy(self):
        delegate_queue = self.scheduling_parameters.queue_manager.get_delegate_queue()
        submitted_job_queue = self.scheduling_parameters.queue_manager.get_submitted_job_queue()

        for i in range(len(delegate_queue)):
            job = delegate_queue[i]
            submitted_job_queue.append(job)

        delegate_queue.clear()
