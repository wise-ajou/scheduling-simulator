from scheduling_parameters import SchedulingParameters
from utils import cur_time

def prioritize(delegate_queue):
    if len(delegate_queue) <= 1:
        return

    normalized_req_num_cores_list = get_normalized_req_num_cores_list(delegate_queue)
    normalized_pending_time_list = get_normalized_pending_time_list(delegate_queue)
    lambda_val = calculate_lambda()

    for i in range(len(delegate_queue)):
        get_score(delegate_queue, i, lambda_val, normalized_pending_time_list, normalized_req_num_cores_list)


def get_score(delegate_queue, i, lambda_val, normalized_pending_time_list, normalized_req_num_cores_list):
    delegate_queue[i].score = lambda_val * normalized_req_num_cores_list[i] + \
                              (1 - lambda_val) * normalized_pending_time_list[i]


def calculate_lambda():
    scheduling_parameters = SchedulingParameters.get_scheduling_parameters()
    period_queue = scheduling_parameters.period_queue
    lambda_val = 1 / ((period_queue[1] / period_queue[0]) + 1)

    return lambda_val


def get_normalized_pending_time_list(delegate_queue):
    scheduling_parameters = SchedulingParameters.get_scheduling_parameters()
    time_unit = scheduling_parameters.time_unit
    flush_period = scheduling_parameters.flush_period
    pending_time_list = list(
        map(lambda x: (cur_time(time_unit) - x.submitted_time) / flush_period,
            delegate_queue))
    min_pending_time = min(pending_time_list)
    max_pending_time = max(pending_time_list)

    if min_pending_time < max_pending_time:
        normalized_pending_time_list = list(
            map(lambda x: (x - min_pending_time) / (max_pending_time - min_pending_time),
                pending_time_list))
    else:
        normalized_pending_time_list = list(map(lambda x: 0.5, pending_time_list))
    return normalized_pending_time_list


def get_normalized_req_num_cores_list(delegate_queue):
    req_num_cores_list = list(map(lambda x: x.required_num_cores, delegate_queue))
    min_core = min(req_num_cores_list)
    max_core = max(req_num_cores_list)

    if min_core < max_core:
        normalized_req_num_cores_list = list(
            map(lambda x: (x - min_core) / (max_core - min_core), req_num_cores_list))
    else:
        normalized_req_num_cores_list = list(map(lambda x: 0.5, req_num_cores_list))

    return normalized_req_num_cores_list
