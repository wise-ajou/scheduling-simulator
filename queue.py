class Queue:
    def __init__(self, num_queue_types):
        self.delegate_queue = []
        self.submitted_job_queue = []
        self.waiting_job_queues = [[] for _ in range(num_queue_types)]
        self.executing_job_queues = [[] for _ in range(num_queue_types)]
        self.finished_job_queues = [[] for _ in range(num_queue_types)]
