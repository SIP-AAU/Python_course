import random
import time
import pp

# http://www.parallelpython.com/content/view/18/32/
# using pp 1.6.4

# in another terminal run:
# ppserver.py -w 4 -a -d
# to setup 4 workers, autoconnect, debug logging to terminal

NBR_ESTIMATES = 1e7


def calculate_pi(nbr_estimates):
    steps = xrange(int(nbr_estimates))
    nbr_trials_in_unit_circle = 0
    for step in steps:
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        is_in_unit_circle = x * x + y * y <= 1.0
        nbr_trials_in_unit_circle += is_in_unit_circle

    return nbr_trials_in_unit_circle


if __name__ == "__main__":
    #NBR_PROCESSES = 4 + 2 + 1
    #NBR_PROCESSES = 4 + 2
    NBR_JOBS = 4  # 1024
    NBR_LOCAL_CPUS = 0
    ppservers = ("*",)  # set IP list to be auto-discovered
    job_server = pp.Server(ppservers=ppservers, ncpus=NBR_LOCAL_CPUS)  # specify no local workers in this process

    #job_server = pp.Server(ppservers=ppservers)  # by default this would enable 8 workers
    print "Starting pp with", job_server.get_ncpus(), "local workers"
    nbr_trials_per_process = [NBR_ESTIMATES] * NBR_JOBS
    t1 = time.time()
    jobs = []
    for input_args in nbr_trials_per_process:
        job = job_server.submit(calculate_pi, (input_args,), (), ("random",))
        jobs.append(job)

    job_server.print_stats()  # dump some debug info
    # each job blocks until the result is ready
    nbr_in_unit_circles = [job() for job in jobs]
    job_server.print_stats()  # dump some debug info

    processors_in_cluster = 0
    for machine_id, stats in job_server.get_stats().items():
        print "Found", machine_id
        processors_in_cluster += stats.ncpus
    print "Across the cluster we have {} CPUs".format(processors_in_cluster)

    print "Amount of work:", sum(nbr_trials_per_process)
    print "Sum of trials inside the unit circle", sum(nbr_in_unit_circles)
    print sum(nbr_in_unit_circles) * 4 / NBR_JOBS / NBR_ESTIMATES
    print calculate_pi.func_name
    overall_time = time.time() - t1
    print "Delta:", overall_time
    print "Average time", overall_time / NBR_JOBS
