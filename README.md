# Scheduling Simulator

## Simulator Structure
The simulator consists of four main modules: Worker, Fetcher, Dispatcher, and Monitor.
* Worker 
  * The Worker module specifies the target queue for tasks in the delegation queue based on the current topology status and submits them to the policy-applied task queue.
* Dispatcher
  * The Dispatcher module is responsible for dispatching tasks to the appropriate worker nodes.
* Fetcher
  * The Fetcher module submits tasks in the policy-applied task queue to the standby queue corresponding to their target queue.
* Monitor 
  * To avoid workload affecting monitoring performance, monitor runs in a separate thread and records three metrics for each monitoring cycle: core utilization by host, core utilization by queue, and core utilization across clusters.

## How to execute

```commandline
pip3 install -r requirements.txt
```

### Execution example

time unit - ms

```commandline
python3 main.py --cluster cluster --job_log log_5th_ms --result log_5th_ms_result --scheduling_algorithm fcfs --initial_flush_period 2000 --monitoring_period 3000 --time_unit ms
```

```commandline
python3 main.py --cluster cluster --job_log log_4th_ms --result log_4th_ms_result --scheduling_algorithm fcfs --initial_flush_period 2000 --monitoring_period 3000 --time_unit ms
```

time unit - s

```commandline
python3 main.py --cluster cluster --job_log log_2nd_sec_scale_down_10000 --result log_2nd_sec_scale_down_10000_result --scheduling_algorithm fcfs --initial_flush_period 2 --monitoring_period 3 --time_unit s
```

```commandline
python3 main.py --cluster cluster --job_log log_1st_sec_scale_down_10000 --result log_1st_sec_scale_down_10000_result --scheduling_algorithm fcfs --initial_flush_period 2 --monitoring_period 3 --time_unit s
```

### Parameters
* cluster
  * Name of the cluster file
* job_log
  * Name of the job log file
* result
  * Name of the result file
* scheduling_algorithm
  * Type of the scheduling algorithm ex) fcfs, sdc
* initial_flush_period
  * Initially set flush period (※ set to the same unit as time_unit)
* monitoring_period 
  * Period for recording resource usage of the cluster (※ set to the same unit as time_unit)
* time_unit
  * Time unit ex) s, ms
