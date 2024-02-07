from timer import cur_time


class SchedulingParameters:
    instance = None
    is_initiated = False

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(SchedulingParameters, cls).__new__(cls)
        return cls.instance

    def __init__(self, scheduling_algorithm, flush_period, cluster, queue_manager, time_unit):
        if self.is_initiated is False:
            self.scheduling_algorithm = scheduling_algorithm
            self.flush_period = flush_period
            self.cluster = cluster
            self.queue_manager = queue_manager
            self.time_unit = time_unit
            self.simulation_start_time = cur_time(self.time_unit)

            self.is_initiated = True
        else:
            raise Exception('SchedulingParameters - 객체 이미 생성된 상태서 init')

    @classmethod
    def get_scheduling_parameters(cls):
        if cls.instance:
            return cls.instance
        else:
            raise Exception('SchedulingParameters - 객체 생성 아직 안된 상태서 get')
