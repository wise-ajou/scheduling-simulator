class Host:
    def __init__(self, host_type, queue_type, num_cores, avail_num_cores=None):
        self.host_type = host_type
        self.queue_type = queue_type
        self.num_cores = num_cores
        self.avail_num_cores = num_cores if avail_num_cores is None else avail_num_cores

    def __str__(self):
        return f'host_type : {self.host_type} |\
                queue_type : {self.queue_type} |\
                num_cores : {self.num_cores} |\
                avail_num_cores : {self.avail_num_cores}'


def get_cluster_by_deep_copy(cluster):
    copied_cluster = []

    for i in range(len(cluster)):
        copied_cluster.append([])

        for j in range(len(cluster[i])):
            original_host = cluster[i][j]
            copied_host = Host(original_host.host_type, original_host.queue_type, original_host.num_cores,
                               original_host.avail_num_cores)
            copied_cluster[i].append(copied_host)

    return copied_cluster


def get_total_num_cores(cluster):
    total_core_sum = 0

    for queue in cluster:
        for host in queue:
            total_core_sum += host.num_cores

    return total_core_sum


def get_avail_num_cores(cluster):
    avail_core_sum = 0

    for queue in cluster:
        for host in queue:
            avail_core_sum += host.avail_num_cores

    return avail_core_sum


class Cluster:
    def __init__(self, file_name):
        self.hosts = []
        self.num_host_types = 0
        self.num_queue_types = 0
        self.num_total_cores = 0

        self.parse_cluster_log(file_name)

    def parse_cluster_log(self, file_name):
        with open(file_name, 'r') as file:
            lines = file.read().split('\n')
            self.num_host_types, self.num_queue_types, self.num_total_cores = [int(e) for e in lines[1].split(' ')]
            print(self.num_host_types, self.num_queue_types, self.num_total_cores)

            for line in lines[2:]:
                line = [int(e) for e in line.split(' ')]
                self.hosts.append(Host(*line))


def get_host_configure_list_by_deep_copy(host_configure_list):
    host_configure_list_copy = []

    for i in range(len(host_configure_list)):
        host_configure_list_copy.append([])

        for j in range(len(host_configure_list[i])):
            original_host = host_configure_list[i][j]
            copied_host = Host(original_host.host_type, original_host.queue_type, original_host.num_cores,
                               original_host.avail_num_cores)
            host_configure_list_copy[i].append(copied_host)

    return host_configure_list_copy
