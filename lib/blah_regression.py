import cream_regression
import testsuite_utils
import submission_thread
import blah_testing
import cream_testsuite_conf

import re
import subprocess
import threading
import time
import datetime
import os
import Queue

'''
Implemented methods enumeration:
1)  check_error_for_bug_84261
2)  kill_remote_process_with_pid_file
3)  remote_process_is_alive
4)  monitor_ce_memory_while_submitting
'''


class _error(Exception):

        def __init__(self,string):
                self.string = string
        def __str__(self):
                return str(self.string)

def check_error_for_bug_84261(err_to_check):
    '''

    '''

    res = ""
    ret_val = ['SUCCESS', 'FAILURE']
    if len(err_to_check) != 0:
        if re.search("/usr/bin/BNotifier: Error creating and binding socket: Address already in use",  err_to_check):
            res = ret_val[1]
        else:
            res = ret_val[0]
    else:
        res = ret_val[0]

    return res

def kill_remote_process_with_pid_file(pid_file):
    '''

    '''
    proc_pid, error = cream_regression.get_remote_command_result("cat %s" % pid_file)
    command = "/bin/kill %s" % proc_pid
    output, error = cream_regression.get_remote_command_result(command)


def remote_process_is_alive(process_name):
    '''

    '''
    command = "/bin/ps -ef |grep %s |grep -v grep |awk \'{print $2}\'" % process_name
    my_utility = testsuite_utils.CommandMng()

    print "Exec remote command: " + command
    outStr, errStr = my_utility.exec_remote_command(command)

    if len(outStr) == 0:
        print "Remote execution output of %s is EMPTY" % command
        return False
    else:
        print "Process %s alive with PID = %s" % (process_name, outStr)
        return True
  
def get_remote_process_pid(process_name):
    '''

    '''
    command = "/bin/ps -ef |grep %s |grep -v grep |awk \'{print $2}\'" % process_name
    my_utility = testsuite_utils.CommandMng()

    print "Exec remote command: " + command
    outStr, errStr = my_utility.exec_remote_command(command)

    if len(errStr) != 0:
        raise _error("Error " + errStr + " executing " + command)

    if len(outStr) == 0:
        print "Remote execution output of %s is EMPTY" % command
        raise _error("Process %s not running" % process_name)
    else:
        print "Process %s alive with PID = %s" % (process_name, outStr)
        return outStr


def get_remote_proc_RSS(process_name):
    '''

    '''
    process_PID = get_remote_process_pid(process_name)
    process_rss = cream_regression.get_remote_command_result("/bin/ps -o rss " + process_PID)
    process_rss = "".join(process_rss)
    first, sep, last = process_rss.partition("RSS")
    process_rss = last.strip(" \n")
    print "process_rss = #" + process_rss + "#"

    return  process_rss

def monitor_ce_memory_while_submitting(job_num, sample_period, jdl_fname, submission_timeout, procs_to_monitor):
    '''
      | Description: | Submit n jobs on a thread and monitor ce memory consumption every m seconds |
      |              | in delta time                                                               |
      | Arguments:   | job_num            | number of jobs to submit                               |
      |              | sample_period      | the sample period in seconds                           |
      |              | jdl_fname          | the jdl file to submit                                 |
      |              | submission_timeout | timeout to apply to submission thread (in seconds)     |
      |              | procs_to_monitor   | the list of names of process to monitor                |
      | Returns:     | a matrix comtaining sampled memory values for given processes.              |
      |              | Access memory samples as matrix[(proc_name, sample_index)]                  |
      | Exceptions:  |                                                                             |
    '''

    RSS_values = list()
    msg_queue = Queue.Queue()
    t = submission_thread.SubmissionThread(msg_queue, job_num, jdl_fname);
    t.start()

    start_time = datetime.datetime.now()
    rss_matrix = {}
    index = 0
    while t.still_working():
        for proc in procs_to_monitor:
            proc_resident_set_size = get_remote_proc_RSS(proc)
            rss_matrix.setdefault(proc, []).append(proc_resident_set_size)
        index = index + 1
        time.sleep(sample_period)
        print "I am waiting submission thread finish work"
        try:
            exc = msg_queue.get(block=False)
        except Queue.Empty:
            pass
        else:
            exc_type, exc_obj, exc_trace = exc
            # deal with the exception
            print exc_type, exc_obj
            print exc_trace
        if (datetime.datetime.now() - start_time) > datetime.timedelta(seconds=submission_timeout):
            break

    t.stop()
    t.is_stopped()

    return rss_matrix

def check_for_bug_94414(jobs_list):
    '''
      | Description: | Given a dictionary of couples cream_job_id:job_status    |
      |              | check if status is DONE-OK and if in blparser log file   |
      |              | notifications for suspended and resumed jobs are present |
      | Arguments:   | jobs_statuses | dictionary of couples                    |
      |              | cream_job_id:job_status                                  |
      | Returns:     | SUCCESS/FAILED                                           |
      | Exceptions:  |                                                          |
    '''

    ret_val = ['CHECK SUCCESSFUL', 'CHECK FAILED']
    final_ret_val = ret_val[0]

    my_conf = cream_testsuite_conf.CreamTestsuiteConfSingleton()
    output_dir = my_conf.getParam('testsuite_behaviour','tmp_dir')

    print "Getting final jobs status ... "
    jobs_final_states, failed_jobs = cream_regression.get_n_job_status(jobs_list, "DONE-OK", 200)

    keys = jobs_final_states.keys()
    for index in keys:
       print "Job " + str(index) + " --- " + jobs_final_states[index]

    if len(failed_jobs) == 0:
        print "Statuses check successful"
        final_ret_val = ret_val[0]
    else:
        print "Statuses check failed"
        final_ret_val =  ret_val[1]

    # Check also blparser notifications because cream has a mechanism to detect job done independently by blparser
    blparser_log = blah_testing.get_blah_parser_log_file_name()
    local_blah_parser_log_file = cream_regression.get_file_from_ce(blparser_log, output_dir)
    for cream_job_id in keys:
        batch_job_id = blah_testing.get_job_num_from_jid(cream_job_id)
        notifications_list = blah_testing.get_notifications_in_blah_parser_log(local_blah_parser_log_file, batch_job_id)
        result = blah_testing.check_notifications_for_normally_finished(notifications_list)
        if result == 'NOTIFICATIONS OK':
            print "Notifications check successful for job " + cream_job_id
        else:
            print "Notifications failure for job " + cream_job_id
            final_ret_val =  ret_val[1]

    return final_ret_val




    
