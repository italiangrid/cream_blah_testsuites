import re
import subprocess
import cream_regression
import testsuite_utils

'''
Implemented methods enumeration:
1)  check_error_for_bug_84261
2)  kill_remote_process_with_pid_file
3)  remote_process_is_alive

'''

def check_error_for_bug_84261(err_to_check):
    '''

    '''

    ret_val = ['SUCCESS', 'FAILURE']
    if len(err_to_check) != 0:
        if re.search("/usr/bin/BNotifier: Error creating and binding socket: Address already in use",  err_to_check):
            return ret_val[1]
        else:
            return ret_val[0]
    else:
        ret_val[0]

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
  

