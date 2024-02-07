from timer import cur_time


class QueueManager:
    def __init__(self, queues):
        self.queues = queues

    def get_delegate_queue(self):
        return self.queues.delegate_queue

    def get_submitted_job_queue(self):
        return self.queues.submitted_job_queue

    def get_waiting_job_queues(self):
        return self.queues.waiting_job_queues

    def get_executing_job_queues(self):
        return self.queues.executing_job_queues

    def get_finished_job_queues(self):
        return self.queues.finished_job_queues

    def submit_jobs(self, job_log, time_unit, simulation_start_time):
        current_time = cur_time(time_unit)

        while len(job_log.jobs) > 0:
            job = job_log.jobs[0]
            submit_time = job.submitted_time
            is_time_to_submit = True if (current_time - simulation_start_time > submit_time) else False

            if is_time_to_submit:
                job = job_log.jobs.pop(0)
                # submitted_time : 로그 상의 submit time => 시뮬레이터에서 실제 delegate queue로 submit time으로 변경 (waiting time 구할 때 사용)
                job.submitted_time = cur_time(time_unit)
                self.queues.delegate_queue.append(job)
            else:
                break
