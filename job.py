class Job:
    def __init__(self, job_id, queue_type, submitted_time, required_num_cores, runtime):
        self.job_id = job_id
        self.queue_type = queue_type
        self.submitted_time = submitted_time
        self.required_num_cores = required_num_cores
        self.runtime = runtime

        self.alloc_host = None
        self.execute_start_time = None
        self.score = None

    def __str__(self):
        return f'job_id : {self.job_id} \
            queue_type : {self.queue_type} \
            submitted_time : {self.submitted_time} \
            required_num_cores : {self.required_num_cores} \
            runtime : {self.runtime}'


class JobLog:

    def __init__(self, file_name):
        self.jobs = []
        self.parse_job_log(file_name)

    def parse_job_log(self, file_name):
        with open(file_name, 'r') as file:
            lines = file.read().split('\n')

            for line in lines:
                line = [int(e) for e in line.split(' ')]
                self.jobs.append(Job(*line))


#job_log = JobLog('./log/2nd_log_10000_scale_sec')

#for job in job_log.jobs[:5]:
    #print(job)
#for job in job_log.jobs[-5:]:
    #print(job)