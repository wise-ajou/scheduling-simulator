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

```commandline
python3 main.py --cluster cluster --job_log log_5th --result log_5th_result --scheduling_algorithm fcfs --initial_flush_period 2000 --time_unit ms 
```

### Parameters
* cluster
  * Name of the cluster file
* job_log
  * Name of the job log file
* result
  * Name of the result file
* scheduling_algorithm
  * Type of the scheduling algorithm ex) fcfs
* initial_flush_period
  * Initially set flush period (※ set to the same unit as time_unit)
* time_unit
  * Time unit ex) s, ms
