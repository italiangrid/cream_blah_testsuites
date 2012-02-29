#############################################################################
# Authors:
# Sara Bertocco - sara dot bertocco at pd dot infn dot it
#############################################################################
'''
Implemented methods enumeration:

 1) get_blah_parser_log_file_name
 2) get_job_num_from_jid
 3) get_notifications_in_blah_parser_log
 4) check_notifications_for_normally_finished
 5) check_notifications_for_cancelled
 6) check_notifications_for_resumed
 7) check_if_notifications_list_is_valid
 8) saturate_batch_system
 9) cancel_list_of_jobs

'''

import cream_testsuite_conf, testsuite_exception, testsuite_utils, cream_testing, regression_vars
import re

#############################################################################################################################
##############################################################################################################################
def get_blah_parser_log_file_name():
    '''
       | Description: | Get blah log parser file name from blah testsuite configuration       |
       | Arguments:   | None                                                                  |
       | Returns:     | blah_parser_log_file_name (complete path)                             |
       | Exceptions:  |                                                                       |
    '''

    my_conf = cream_testsuite_conf.CreamTestsuiteConfSingleton()
    blparser_log = my_conf.getParam('blah_specific','parser_log_file')
    if len(blparser_log) == 0:
        raise testsuite_exception.TestsuiteError("Mandatory parameter parser_log_file is empty. Check testsuite configuration")

    print "Blah parser log file name " + blparser_log

    return blparser_log

#############################################################################################################################
##############################################################################################################################
def get_job_num_from_jid(cream_job_id):

    ''' | Description: | gets the job num (9 digits following "CREAM" string) from job ID     |
        | Arguments:   | cream_job_id (cream job identifier)                                  |
        | Returns:     | the job label (string "CREAM" followed by 9 digits)                  |
        | Exceptions:  |                                                                      |
    '''

    first_part, separator, second_part = cream_job_id.partition("CREAM")
    return second_part

#############################################################################################################################
##############################################################################################################################
def get_notifications_in_blah_parser_log(blah_parser_log_file, job_num):
    '''
       | Description: | Checks in a local copy of blah parser log file (received as parameter) |
       |              | the notifications related to the job Job_num (received as parameter)   |
       |              |  nd returns the list of notifications.                                 |
       | Arguments:   | blah_parser_log_file | path name of local copy of blah parser log file |
       |              | job_num              | numeric part of jobid                           |
       | Returns:     | a list of notifications (i.e. a list of digits)                        |
       | Exceptions:  |                                                                        |
    '''

    com = "/bin/grep " + job_num + " " + blah_parser_log_file

    print "Exec remote command: " + com
    
    my_utility = testsuite_utils.CommandMng()
    out, err = my_utility.exec_command(com)
    
    ex = re.compile('(?<=JobStatus=).')
    notifications_list = ex.findall(out)
    print "Notifications list: " + " ".join(notifications_list)

    return notifications_list


def check_notifications_for_normally_finished(notifications_list):
    '''
       | Description: | Given a list of notifications received as input, checks if it is       |
       |              | acceptable as notification list for a job normally finished, i.e.:     |
       |              |  * A notification with JobStatus=1 (this can be missing)               |
       |              |  * A notification with JobStatus=2 (this can be missing)               |
       |              |  * A notification with JobStatus=4 (this must be there)                |
       | Arguments:   | notifications_list | a list of notifications                           |
       | Returns:     | 'NOTIFICATIONS OK'/''NOTIFICATIONS FAILURE'                            |
       | Exceptions:  |                                                                        |  
    '''

    ret_val = ['NOTIFICATIONS OK', 'NOTIFICATIONS FAILURE']
    valid_lists = [['4'], ['1','4'], ['2','4'], ['1','2','4']] 

    if check_if_notifications_list_is_valid(notifications_list, valid_lists):
        return ret_val[0]
    else:
        return ret_val[1]


def check_notifications_for_cancelled(notifications_list):
    '''
       | Description: | Given a list of notifications received as input, checks if it is       |
       |              | acceptable as notification list for a job cancelled, i.e.:             |
       |              | * A notification with JobStatus=1 (this can be missing)                |
       |              | * A notification with JobStatus=2 (this can be missing)                |
       |              | * A notification with JobStatus=3 (this must be there)                 |
       | Arguments:   | notifications_list | a list of notifications                           |
       | Returns:     | 'NOTIFICATIONS OK'/''NOTIFICATIONS FAILURE'                            |
       | Exceptions:  |                                                                        | 
    '''

    ret_val = ['NOTIFICATIONS OK', 'NOTIFICATIONS FAILURE']
    valid_lists = [['3'], ['1','3'], ['2','3'], ['1','2','3']]
    if check_if_notifications_list_is_valid(notifications_list, valid_lists):
        return ret_val[0]
    else:
        return ret_val[1]


def check_notifications_for_resumed(notifications_list):
    '''
       | Description: | Given a list of notifications received as input, checks if it is       |
       |              | acceptable as notification list for a job suspended and resumed, i.e.: |
       |              | * A notification with JobStatus=1 (this can be missing)                |
       |              | * A notification with JobStatus=2 (this can be missing)                |
       |              | * A notification with JobStatus=5 (this must be there)                 |
       |              | * A notification with JobStatus=2 (this can be missing)                |
       |              | * A notification with JobStatus=4 (this must be there)                 |
       | Arguments:   | notifications_list | a list of notifications                           |
       | Returns:     | 'NOTIFICATIONS OK'/''NOTIFICATIONS FAILURE'                            |
       | Exceptions:  |                                                                        | 
    '''

    ret_val = ['NOTIFICATIONS OK', 'NOTIFICATIONS FAILURE']
    valid_lists = [['5','4'],['1','5','4'], ['2','5','4'],['5','2','4'], ['1','2','5','4'],['2','5','2','4'],['1','5','2','4'],['1','2','5','2','4']] 

    if check_if_notifications_list_is_valid(notifications_list, valid_lists):
        return ret_val[0]
    else:
        return ret_val[1]


def check_if_notifications_list_is_valid(list_to_check, good_notification_lists):
    '''
       | Description: | Given a generic list of notifications, checks if it is included in a  |
       |              | set of permissible lists of notifications.                            |
       | Arguments:   | list_to_check           | list to be checked                          |
       |              | good_notification_lists | set of permissible lists                    |
       | Returns:     | true if list_to_check is in good_notification_lists, false otherwise  |
       | Exceptions:  |                                                                       | 
    '''

    list_is_valid = False

    for list in good_notification_lists:
        if list_to_check == list:
            list_is_valid = True

    return list_is_valid


def saturate_batch_system():
    '''
       | Description: | Reads from test suite configuration file the value of total CPU number |
       |              | present in the batch cluster and submits a number of jobs equal to     |
       |              | the total CPU number, to saturete the batch system reading submission  |
       |              | parameters from configuration file.                                    |
       | Arguments:   | None                                                                   |
       | Returns:     | The list of cream job ids of submitted jobs                            |
       | Exceprtions: | TestsuiteError | if an error is present in parameters read from config |
    '''
    my_conf = cream_testsuite_conf.CreamTestsuiteConfSingleton()
    tot_cpu_in_batch_cluster = my_conf.getParam('batch_system','tot_cpu_num')
    vo = my_conf.getParam('submission_info','vo')
    proxy_pass = my_conf.getParam('submission_info','proxy_pass')
    ce_endpoint = my_conf.getParam('submission_info','ce_endpoint')
    cream_queue = my_conf.getParam('submission_info', 'cream_queue')
    #output_dir = my_conf.getParam('testsuite_behaviour','tmp_dir')
    output_dir = regression_vars.tmp_dir

    ce = ce_endpoint + "/" + cream_queue


    if len(tot_cpu_in_batch_cluster) == 0: 
        raise testsuite_exception.TestsuiteError("Mandatory parameter tot_cpu_num is empty. Check testsuite configuration")
    if len(vo) == 0:
        raise testsuite_exception.TestsuiteError("Mandatory parameter vo is empty. Check testsuite configuration")
    if len(ce_endpoint) == 0:
        raise testsuite_exception.TestsuiteError("Mandatory parameter ce_endpoint is empty. Check testsuite configuration")
    if len(cream_queue) == 0:
        raise testsuite_exception.TestsuiteError("Mandatory parameter cream_queue is empty. Check testsuite configuration")
    if len(output_dir) == 0:
        raise testsuite_exception.TestsuiteError("Mandatory parameter tmp_dir is empty. Check testsuite configuration")

    print "Creating proxy ..."
    cream_testing.create_proxy(proxy_pass, vo)
    print "Creating jdl"
    jdl_fname = cream_testing.sleep_jdl(vo, "300", output_dir)

    cream_job_ids = list()
    for i in range(int(tot_cpu_in_batch_cluster)):
        cream_job_id = cream_testing.submit_job(jdl_fname, ce)
        cream_job_ids.append(cream_job_id)
     
    print cream_job_ids

    return cream_job_ids


def cancel_list_of_jobs(job_ids_list):
    '''
      | Description: | Given a list of cream job ids, cancel them.          |
      | Arguments:   | The list of job ids to cancel.                       |
      | Returns:     | Nothing.                                             |
      | Exceptions:  |                                                      |
    '''

    for cream_job_id in job_ids_list:
        cream_testing.cancel_job(cream_job_id)


