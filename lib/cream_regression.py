'''
Job Handling
--
exec_cream_cli_command(), check_allowed_submission(), get_n_job_status(), suspend_n_jobs(), resume_n_jobs(), exec_jobDBAdminPurger_sh(), job_db_admin_purger_script_check(), delete_job_from_batch_system(), check_if_job_purged(), job_status_should_be_in() 

Proxy Handling
--
create_rfc_proxy(), 

Data Manipulation
--
get_job_output()

JDL Creation
--
create_jdl_87492()

Utils
--
Exec Remote Command(), get_remote_command_result(), exec_local_command(), get_file_from_ce(), put_file_on_ce(), check_parameter(), check_parameter_value(), change_conf_param_in_file()

CREAM Utils
--
exec_cream_cli_command(), get_job_label_from_jid(), get_cream_db_user_password_from_config(), append_string_to_file_on_ce()

YAIM Handling
--
get_yaim_param(), get_cream_sandbox_from_yaim_conf(), get_cream_concurrency_level_from_yaim_conf(), run_yaim_func(), configure_ce_by_yaim()

Information Provider Handling:
--
check_ce_GlueForeignKey_GlueCEUniqueID(), check_cream_dynamic_info()

Bug specifics
--
check_job_out_87492(), check_job_out_89489(), check_bug_83338(), check_bug_95552(), check_bug_95356(), check_bug_59871(), check_bug_87361()

Exceptions
--
_error()


Implemente methods enumeration:
--
1)  Exec Remote Command
2)  get_remote_command_result
3)  exec_cream_cli_command
4)  exec_local_command
5)  get_job_output
6)  check_allowed_submission
7)  create_rfc_proxy
8)  get_n_job_status
9)  suspend_n_jobs
10) resume_n_jobs
11) create_jdl_87492
12) check_job_out_87492
13) check_job_out_89489
14) get_job_label_from_jid
15) get_file_from_ce
16) put_file_on_ce
17) check_parameter
18) check_parameter_value
19) get_yaim_param
20) get_cream_sandbox_from_yaim_conf
21) get_cream_concurrency_level_from_yaim_conf
22) get_cream_db_user_password_from_config
23) exec_jobDBAdminPurger_sh
24) job_db_admin_purger_script_check
25) delete_job_from_batch_system
26) change_conf_param_in_file
27) run_yaim_func
28) configure_ce_by_yaim
29) check_if_job_purged
30) job_status_should_be_in
31) append_string_to_file_on_ce
32) check_ce_GlueForeignKey_GlueCEUniqueID
33) check_cream_dynamic_info
34) check_bug_83338
35) check_bug_95552
36) check_bug_95356
37) check_bug_59871
38) check_bug_87361

'''

import subprocess , shlex , os , sys , time , datetime, re , string , paramiko
from string import Template
import batch_sys_mng, cream_testing, testsuite_utils, cream_config_layout_mng, cream_testsuite_conf, mysql_mng
import regression_vars
import MySQLdb as mdb

class _error(Exception):

    '''
       | Description: | Generic exception                                                           |
       | Arguments:   | string | containing the error message                                       | 
       | Returns:     | nothing.                                                                    |
    '''

    def __init__(self,string):
        self.string = string
    def __str__(self):
        return str(self.string)

##############################################################################################################################
##############################################################################################################################

def exec_remote_command(command):

    '''
       | Description: | Executes a generic unix command on the indicated host with provided         |
       |              | admin name and password.                                                    |
       | Arguments:   | string | command to execute                                                 |
       | Returns:     | nothing.                                                                    |
    '''

    my_utility = testsuite_utils.CommandMng()

    print "Exec remote command: " + command

    my_utility.exec_remote_command(command)

##############################################################################################################################
##############################################################################################################################
def get_remote_command_result(command):

    '''
        | Description: | Executes a generic unix command ion the ce under test                      |   
        | Arguments:   | string | command to execute                                                | 
        | Returns:     | command output an command error as strings.                                |
    '''

    my_utility = testsuite_utils.CommandMng()

    print "Exec remote command: " + command

    outStr, errStr = my_utility.exec_remote_command(command)

    return outStr, errStr 

##############################################################################################################################
##############################################################################################################################
def exec_cream_cli_command(command):

    '''
        | Description: | Executes a generic cream client command.                                   |
        | Arguments:   | string | cream-cli command.                                                |
        | Returns:     | nothing.                                                                   |
    '''

    print "Executing command %s" % command

    my_utility = testsuite_utils.CommandMng()

    try:
        output, error = my_utility.exec_command(command) 
    except Exception as exc:
        print exc
        raise _error("Cream cli command " + command + " execution failed")
   
    if len(error) != 0:
        raise _error("Cream cli command " + command + " execution failed with error:\n" + error)

    return output


##############################################################################################################################
##############################################################################################################################
def exec_local_command(command):

    '''
        | Description: | Executes a local shell command.                                            |
        | Arguments:   | string | command                                                           |
        | Returns:     | nothing                                                                    |
    ''' 

    print "Executing local command %s" % command

    my_utility = testsuite_utils.CommandMng()

    try:
        output, error = my_utility.exec_command(command)
    except Exception as exc:
        print exc
        raise _error("Command " + command + " execution failed")

    if len(error) != 0:
        raise _error("Command " + command + " execution failed with error:\n" + error)

    return output


##############################################################################################################################
##############################################################################################################################
def get_job_output(target_dir_path, job_id):

    '''
        | Description: | Retrieve the job output saving it in the provided directory                 |
        | Arguments:   | string | path where store the output                                        |
        |              | string | cream job identifier                                               |
        | Returns:     | path where the output is stored                                             |
        | Exception:   |                                                                             |
    '''

    regex = re.compile('/$')
    if re.search(regex,target_dir_path):
        target_dir_path = target_dir_path[:-1]

    com="/usr/bin/glite-ce-job-output -D %s %s" % (target_dir_path, job_id)
    ret=exec_cream_cli_command(com)
    out = "".join(ret)
    out = out.strip()

    first, sep, last = out.partition("output will be stored in the dir ")
    print "first = " + first
    print "sep = " + sep 
    print "last = " + last 
    output_path = "".join(last.split())

    print output_path

    return output_path


#############################################################################################################################
##############################################################################################################################
def check_allowed_submission(ce_endpoint):

    '''
        | Description: | Cheks if the job submission in the given cream endpoint is enabled.        |
        | Arguments:   | cream endpoint.                                                            |
        | Returns:     | glite-ce-allowed-submission command output.                                |
    '''
    time.sleep(20)
    com="/usr/bin/glite-ce-allowed-submission %s" % ce_endpoint
    ret=exec_cream_cli_command(com)
    out = "".join(ret)
    out = out.strip()
    out = out.replace (" ", "_")
    out = out.lower()

    return out

##############################################################################################################################
##############################################################################################################################
def create_rfc_proxy(password, vo, cert=None, key=None, time=None):
    '''
        |  Description:  |  Create a user proxy.                                                    |\n
        |  Arguments:    |  password  |  the user's proxy password                                  |
        |                |  vo        |  for the voms extention.                                    |
        |                |  cert      |  non standard certificate path                              |
        |                |  key       |  non standard key path                                      |
        |                |  time      |  the validity period of the proxy. Form: HH:MM              |\n
        |  Returns:      |  nothing.                                                                |
    '''


    com = "/usr/bin/voms-proxy-init -pwstdin --voms %s -rfc" % vo

    if cert != None and key != None:
        com = com + ' -cert ' + cert + ' -key ' + key
    if time != None:
        pattern = "\d\d\:\d\d"
        match = re.search(pattern,time)
        if match:
            com = com + ' -valid ' + time
        else:
            raise _error("Wrong time format for proxy creation! It must be in the form HH:MM")

    if (cert != None and key == None) or (cert == None and key != None):
        raise _error("Wrong arguments for proxy creation: " + password + " " + vo + " " + cert + " " + key)

    args = shlex.split(com.encode('ascii'))
    proc = subprocess.Popen( args , shell=False , stderr=subprocess.STDOUT , stdout=subprocess.PIPE , stdin=subprocess.PIPE)
    (stdoutdata, stderrdata) = proc.communicate(input=password)

    retVal=proc.wait()

    if stdoutdata is not None and len(stdoutdata) != 0:
        stdoutdata = "".join(stdoutdata)
    else:
        stdoutdata = ""
    if stderrdata is not None and len(stderrdata) != 0:
        stderrdata = "".join(stderrdata)
    else:
        stderrdata = ""
    print "Command " + com + " output: \n" + stdoutdata
    print "Command " + com + " error \n" + stderrdata

    if retVal != 0 :
        raise _error("Rfc proxy creation failed.")

    return stdoutdata

##############################################################################################################################
##############################################################################################################################
def get_n_job_status(jobs_id_list, expected_status, timeout=200):
    '''
        | Description:    | Wait for a fixed time (timeout defaulted in 200s) that jobs received as |
        |                 | input (jobs_id_list)                                                    |
        |                 | gain the expected status and return a dictionary of pairs               |
        |                 | job_id:final_status                                                     |
        | Arguments:      | jobs_id_list    | list of job ids of jobs to check.                     |
        |                 | expected_status | status to be rached by jobs                           |
        |                 | waith thath job job_id reach expected status for a given time, then the |
        |                 | job is treated as failed.                                               |
        | Returns:        | a dictionary of pairs job_id:final_status  and a list of failed jobs    |
        | Exceptions:     |                                                                         |
    '''
    print "Getting jobs status ... "
    print "Job list = " 
    print jobs_id_list
    print "Expected status = " + expected_status
    jobs_final_states = {}
    failed_jobs = list()
    final_job_status = ""
    for item in jobs_id_list:
        try:
            final_job_status = cream_testing.wait_for_status(item, expected_status, timeout)
            final_job_status = cream_testing.get_current_status(item) 
            print "Job " + str(item) + " successful with status = " + final_job_status
            jobs_final_states[item] = final_job_status
        except:
            final_job_status = cream_testing.get_current_status(item)
            print "Job " + str(item) + " failed with status " + final_job_status
            jobs_final_states[item] = final_job_status
            failed_jobs.append(item)

    print "Final jobs state"
    print jobs_final_states
    print "Failed jobs"
    print failed_jobs
    return jobs_final_states, failed_jobs

#############################################################################################################################
##############################################################################################################################
def suspend_n_jobs(jobs_to_suspend):
    '''
        | Description:    | Try to suspend jobs received as input. If the operation fails, a list   |
        |                 | of jobs not suspended                                                   |
        |                 | is returned.                                                            |
        | Arguments:      | jobs_to_suspend | a list of cream job ids.                              |
        | Returns:        | a list of job ids corresponding to failures in suspend operation.       |
        |                 | Prints the errors.                                                      |
        | Exceptions:     |                                                                         |
    '''
    failed_jobs = list()

    print "Try to suspend all jobs"
    for item in jobs_to_suspend:
        try:
            cream_testing.suspend_job(item)
        except Exception as e:
            print "Caught an exception trying to suspend job " 
            print item
            print e
            failed_jobs.append(item)

    return failed_jobs

#############################################################################################################################
##############################################################################################################################
def resume_n_jobs(jobs_to_resume):
    '''
        | Description:    | Try to resume  jobs received as input. If the operation fails, a list   |
        |                 | of jobs not resumed                                                     |
        |                 | is returned.                                                            |
        | Arguments:      | jobs_to_resume | a list of cream job ids.                               |
        | Returns:        | a list of job ids corresponding to failures in resume  operation.       |
        |                 | Prints the errors.                                                      |
        | Exceptions:     |                                                                         |
    '''
    failed_jobs = list()

    print "Resuming jobs ..."
    for item in jobs_to_resume:
        try:
            cream_testing.resume_job(item)
        except Exception as e:
            print "Caught an exception trying to resuming job "
            print item
            print e
            failed_jobs.append(item)

    return failed_jobs


#############################################################################################################################
##############################################################################################################################
def create_jdl_87492(vo, output_dir):
    '''
        | Description:    | Create a jdl specific to test bug #87492                                |
        | Arguments:      |   vo           |   virtual organisation                                 |
        |                 |   output_dir   |   the directory to put the file in                     | 
        | Returns:        | The created jdl path                                                    |
        | Exceptions:     |                                                                         |
    '''
    
    folder = output_dir
    
    jdl_identifier = 'bug87492'
    jdl_name = 'cream_regression-' + str(time.time()) + '-' + jdl_identifier + '.jdl'
    jdl_path = folder + '/' + jdl_name
    jdl_file = open(jdl_path,'w')
    
    jdl_contents =  '[\n'\
                    'Environment = {\n'\
                    '"GANGA_LCG_VO=\'camont:/camont/Role=lcgadmin\'",\n'\
                    '"LFC_HOST=\'lfc0448.gridpp.rl.ac.uk\'",\n'\
                    '"GANGA_LOG_HANDLER=\'WMS\'"\n'\
                    '};\n'\
                    'executable="/bin/env";\n'\
                    'stdoutput="out.out";\n'\
                    'outputsandbox={"out.out"};\n'\
                    'outputsandboxbasedesturi="gsiftp://localhost";\n'\
                    ']\n'


    jdl_file.write(jdl_contents)
    jdl_file.close()

    return jdl_path


#############################################################################################################################
#############################################################################################################################
def check_job_out_87492(job_output_location):
    '''
        | Description:    | Receive job output as input and checks if it contains                   |
        |                 | expected variables with expected values                                 |
        | Arguments:      | string | job output location                                            |
        | Returns:        | check result                                                            |
        | Exceptions:     |                                                                         |
    '''

    ret_val = ['CHECK SUCCESSFUL', 'CHECK FAILED']

    job_out_file = job_output_location + "/out.out"

    my_utility = testsuite_utils.Utils()

    check1 = 1
    check2 = 1
    check3 = 1
    ret, param_val = my_utility.check_param_in_conf_file(job_out_file, "GANGA_LCG_VO")
    print "GANGA_LCG_VO = " + param_val
    if param_val == "camont:/camont/Role=lcgadmin":
        check1 = 0
    ret, param_val = my_utility.check_param_in_conf_file(job_out_file, "LFC_HOST")
    print "LFC_HOST = " + param_val
    if param_val == "lfc0448.gridpp.rl.ac.uk":
        check2 = 0
    ret, param_val = my_utility.check_param_in_conf_file(job_out_file, "GANGA_LOG_HANDLER")
    print "GANGA_LOG_HANDLER = " + param_val
    if param_val == "WMS":
        check3 = 0

    if check1 or check2 or check3:
        return ret_val[1]
    else:
        return ret_val[0]

#############################################################################################################################
#############################################################################################################################
def check_job_out_89489(job_output):
    '''
        | Description:    | Receive a string (output of a command) as input and                     |
        |                 | checks if it contains the expected string                               |
        | Arguments:      | string | command output                                                 |
        | Returns:        | check result                                                            |
        | Exceptions:     |                                                                         |
    '''

    ret_val = ['CHECK SUCCESSFUL', 'CHECK FAILED']

    result = re.search("INFO: Executing function: config_cream_gip_scheduler_plugin_check", job_output)

    if result is None:
        return ret_val[1]
    else:
        return ret_val[0]


#############################################################################################################################
##############################################################################################################################
def get_job_label_from_jid(cream_job_id):
    '''
        | Description: | gets the job label (string "CREAM" followed by 9 digits) from job ID       |
        | Arguments:   | cream_job_id | (cream job identifier)                                      |
        | Returns:     | the job label (string "CREAM" followed by 9 digits)                        |
        | Exceptions:  |                                                                            |
    '''

    first_part, separator, second_part = cream_job_id.partition("CREAM")
    return separator + second_part

#############################################################################################################################
##############################################################################################################################
def get_file_from_ce(file_to_get, output_dir):
    '''
        | Description: | Gets the file_to_get from the cream endpoint provided.                     |
        | Arguments:   | file to get (full path name)                                               |
        |              | directory where to save the local file copy                                |
        | Returns:     | local full path of retrieved file.                                         |
    '''

    my_utility = testsuite_utils.Utils()

    return my_utility.get_file_from_ce(file_to_get, output_dir) 

#############################################################################################################################
##############################################################################################################################
def put_file_on_ce(file_to_put, file_dest):
    '''
        | Description: | Puts the file_to_put in file_dest on ce cream under test.                  |
        | Arguments:   | local file to put                                                          |
        |              | remote file destination                                                    |
        | Returns:     | local full path of retrieved file.                                         |
    '''

    my_utility = testsuite_utils.Utils()

    return my_utility.put_file_on_ce(file_to_put, file_dest)

#############################################################################################################################
##############################################################################################################################
def check_parameter(conf_f, param_to_check):
    '''
        | Description: | This function searches if the parameter param_to_check is present          |
        |              | in the (locally) provided configuration file                               |    
        | Arguments:   | param_to_check: name of the parameter to search                            |
        |              | conf_f: file where search the parameter.                                   |
        | Returns:     | INITIALIZED, NOT_PRESENT, or NOT_INITIALIZED                               |
    '''

    my_utility = testsuite_utils.Utils()
    ret_val, param_value = my_utility.check_param_in_conf_file(conf_f, param_to_check)

    return ret_val

#############################################################################################################################
##############################################################################################################################
def check_parameter_value(conf_f, param_to_check):
    '''
        | Description: | This function searches if the parameter param_to_check is present          |
        |              | in the provided configuration file                                         |    
        | Arguments:   | param_to_check: name of the parameter to search                            |
        |              | conf_f: file where search the parameter.                                   |
        | Returns:     | INITIALIZED, NOT_PRESENT, or NOT_INITIALIZED and parameter value           |
    '''

    my_utility = testsuite_utils.Utils()
    ret_val, param_value = my_utility.check_param_in_conf_file(conf_f, param_to_check)

    return ret_val, param_value
    
#############################################################################################################################
##############################################################################################################################
def get_yaim_param(param_name):
    '''
        | Description: | Call remote object cream_config_layout_mng.CreamConfigLayoutMng            |
        |              | to obtain the value of the parameter param_name                            |
        | Arguments:   | param_name | the parameter name                                            |
        | Returns:     | the parameter value                                                        |
        | Exception:   |                                                                            |
    '''

    cream_conf_layout_mng = cream_config_layout_mng.CreamConfigLayoutMng()

    param_value = cream_conf_layout_mng.check_yaim_param(param_name)

    if len(param_value) != 0:
        return param_value
    else:
        raise _error("Parameter " + param_value  + " NOT FOUND in yaim configurations files")

#############################################################################################################################
##############################################################################################################################
def get_cream_sandbox_from_yaim_conf():
    '''
        | Description: | Uses the get_yaim_param to get the CREAM_SANDBOX_PATH from yaim            |
        |              | configuration on ce and then parses the result to manage the case          |
        |              | of default value                                                           |
        |              | CREAM_SANDBOX_PATH=${GLITE_CREAM_LOCATION_VAR}/cream_sandbox               |
        | Arguments:   | None                                                                       |
        | Returns:     | CREAM_SANDBOX_PATH value configured in yaim                                |
        | Exception:   |                                                                            |
    '''

    my_conf = cream_testsuite_conf.CreamTestsuiteConfSingleton()
    cream_sandbox_var_name = my_conf.getParam('cream_parameters','cream_sandbox_path')
    glite_env_location_var_name = my_conf.getParam('cream_parameters','glite_cream_location_var')
    glite_env_location_var_value = my_conf.getParam('srv_environment','GLITE_CREAM_LOCATION_VAR')

    sandbox_path = get_yaim_param(cream_sandbox_var_name)
    print "sandbox_path = " + sandbox_path
    
    final_cream_sandbox_path = sandbox_path
    if re.search(glite_env_location_var_name, sandbox_path):
        #s = Template(sandbox_path)
        #print "glite_env_location_var_name = " + glite_env_location_var_name
        print "glite_env_location_var_value = " + glite_env_location_var_value
        #final_cream_sandbox_path = s.substitute(glite_env_location_var_name=glite_env_location_var_value)
        #final_cream_sandbox_path = s.substitute(GLITE_CREAM_LOCATION_VAR=glite_env_location_var_value)
        final_cream_sandbox_path = sandbox_path.replace("${" + glite_env_location_var_name + "}", glite_env_location_var_value)
        if re.search(glite_env_location_var_name, final_cream_sandbox_path):
            final_cream_sandbox_path = sandbox_path.replace("$" + glite_env_location_var_name, glite_env_location_var_value)   
    print "final_cream_sandbox_path = " + final_cream_sandbox_path

    return final_cream_sandbox_path


#############################################################################################################################
##############################################################################################################################
def get_cream_concurrency_level_from_yaim_conf():
    '''
        | Description: | Because the cream_concurrency_level parameter is indicated with another name |
        |              | in EMI2 cream configuration file, it has been needed to have parametre name  |
        |              | and parameter value both configurable. This function reads the parameter name|
        |              | from the testsuite configuration file and its value from yaim configuration  |
        |              | file of the ce under test.                                                   |
        | Arguments:   | None                                                                         |
        | Returns:     | cream_concurrency_level parameter value                                      |
    '''
    cream_concurrency_level_name = regression_vars.cream_concurrency_level_yaim_name
    print "cream_concurrency_level_name = " + cream_concurrency_level_name
    cream_concurrency_level_value = get_yaim_param(cream_concurrency_level_name)
    print "cream_concurrency_level_value = " + cream_concurrency_level_value 

    return cream_concurrency_level_value

#############################################################################################################################
##############################################################################################################################
def get_cream_db_user_password_from_config():
    '''
        | Description: | Search cream database username and password in cream configuration file.   |
        | Arguments:   | None                                                                       |
        | Returns:     | dbuser, dbpassword.                                                        |
    '''
    
    cream_conf_layout_mng = cream_config_layout_mng.CreamConfigLayoutMng()

    return cream_conf_layout_mng.get_cream_db_user_password()

#############################################################################################################################
##############################################################################################################################
def exec_jobDBAdminPurger_sh(db_usr_name, db_usr_pass, conf_f, options):

    '''
        | Description: | Call  remote object cream_config_layout_mng.CreamConfigLayoutMng to        |
        |              | obtain cream database username and object and then call                    |
        |              | Call cream_testsuite_mng.CommandMng remote object ito exec job purging     |
        |              | operation                                                                  |
        | Argument:    | options string to add to the jobDBAdminPurger command                      |
        | Returns:     | output and error of the command execution                                  |
        | Exception:   |                                                                            |
    '''
    my_conf = cream_testsuite_conf.CreamTestsuiteConfSingleton()
    catalina_home = regression_vars.catalina_home 
    middleware_version = my_conf.getParam('middleware', 'middleware_version')
    com = ""
    if middleware_version.lower() == "emi1":
        print "middleware_version = %s" % middleware_version.lower()
        com = "export CATALINA_HOME=%s; /usr/sbin/JobDBAdminPurger.sh -c %s -u %s -p %s %s" % (catalina_home, conf_f, db_usr_name, db_usr_pass, options)
    elif middleware_version.lower() == "emi2":
        print "middleware_version = %s" % middleware_version.lower()
        com = "export CATALINA_HOME=%s; /usr/sbin/JobDBAdminPurger.sh -c %s %s" % (catalina_home, conf_f, options)
    else:
        print "middleware_version = %s" % middleware_version.lower()
        raise _error('Invalid middleware version provided. Should be either "EMI1" or "EMI2", but you entered:"' + middleware_version + '"')

    print "Executing on CE the command : " + com

    myout, myerr = get_remote_command_result(com)
    print "Command output : " + myout
    print "Command error  : " + myerr

    return myout, myerr

#############################################################################################################################
##############################################################################################################################
def job_db_admin_purger_script_check(db_user_name, db_user_password, conf_f):

    '''
        | Description: | Cheks if the JobDBAdminPurger.sh in the given cream endpoint works correctly|
        | Arguments:   | cream endpoint, admin_name, admin_password, db_user_name, db_user_password  |
        | Returns:     | The result of the check                                                     |
        | Exceptions:  |                                                                             |
    '''

    # Gets the cream configuration file and stores it locally
    # Gets cream database username and password from ce-cream.xml configuration file 
    # Runs the command "export CATALINA_HOME=" + catalina_home + " ; JobDBAdminPurger.sh -c /etc/glite-ce-cream/cream-config.xml -u cremino -p creamtest -s DONE-FAILED,0"
    # Parse the output

    ret_val = ['SUCCESS', 'FAILED']

    options = " -s DONE-FAILED,0"
        
    myout, myerr = exec_jobDBAdminPurger_sh(db_user_name, db_user_password, conf_f, options)
        
    # Commented because the script has a not empty error string also when it is correctly running
    #if myerr != "":
    #        raise _error("job_db_admin_purger_script_check Failed\n" + " Reported: " +  myerr)               
    if re.search('START jobAdminPurger', myout) and re.search('STOP jobAdminPurger', myout):
        return ret_val[0]
    else:
        return ret_val[1]

#############################################################################################################################
##############################################################################################################################
def delete_job_from_batch_system(cream_job_id, batch_sys):
    '''
        | Description: | Manually delete  a job from the declared batch system.                     |
        | Arguments:   | cream_job_id (cream job identifier),                                       |
        | Returns:     | Nothing                                                                    |
        | Exceptions:  | batch_sys_mng.BatchCmdError, batch_sys_mng.JobNotFoundError                |
    '''

    batchSysFactory = batch_sys_mng.BatchSystemFactory(batch_sys)
    my_batch_sys_mng = batchSysFactory.getBatchSystemMng()

    batch_jid = "not_set"
    start = datetime.datetime.now()
    stop = datetime.datetime.now()
    elapsed = stop - start
    while elapsed < datetime.timedelta(minutes=2):
        print "(re-)try"
        try:
            time.sleep(30)
            print "Try to get batch_jid from cream jobid"
            print "--- cream_job_id = " + cream_job_id
            batch_jid = my_batch_sys_mng.get_batch_jid_from_cream_jid(cream_job_id)
            print "--- batch_jid = " + batch_jid
            break
        except Exception as exc:
            print "Exception trying to get batch_jid from cream jobid"
            print exc
            stop = datetime.datetime.now()
            elapsed = stop - start

    if batch_jid is "not_set":
        raise _error("CREAM job " + cream_job_id + " not found in batch system 5 minutes after submission")

    my_batch_sys_mng.del_job_from_batch_id(batch_jid)
###############################################################################
###############################################################################
def change_conf_param_in_file(conf_file, param_name, param_value):

    '''
       | Description: | Add or change, if already present, the provided parameter param_name        |
       |              | in the configuration file 'conf_file' with the 'param_value'                |
       |              | Call cream_configurator_server.CreamConfigurator remote object              |
       | Arguments:   | conf_file full name of file                                                 |
       |              | param_name name of parameter to add/change                                  |
       |              | param_value value to assign to param_name                                   |
       | Returns:     | nothing                                                                     |
       | Exceptions:  |                                                                             |
    '''

    cream_conf_layout_mng = cream_config_layout_mng.CreamConfigLayoutMng()

    param_value = cream_conf_layout_mng.chenge_conf_param_in_file(conf_file, param_name, param_value)


###############################################################################
###############################################################################
def run_yaim_func(site_info_file, func_to_run):

    '''
        | Description: | Run yaim function func_to_run using site_info_file as site-ifo.def file    |
        | Arguments:   | site_info_file | complete file path name of site-info.def file on ce       |
        |              |                | under test                                                |
        |              | func_to_run    | yaim function to be run                                   |
        | Returns:     | Nothing        |                                                           |
        | Exception:   | Throws exception on error.                                                 |
    '''

    command = "/opt/glite/yaim/bin/yaim -r -s " + site_info_file + " -n creamCE -f " + func_to_run
    print "Exec remote command: " + command

    my_utility = testsuite_utils.CommandMng()

    out, err = my_utility.exec_remote_command(command)
    print "Output:"
    print out
    print "Error:"
    print err

###############################################################################
###############################################################################
def configure_ce_by_yaim(site_info_file):
    '''
        | Description: | Run yaim using site_info_file as site-ifo.def file to configure the ce.    |
        |              | Check in testsuite configuration file which batch system is used and if    |
        |              | ce is also batch master to set configurations node types                   |
        | Arguments:   | site_info_file | complete file path name of site-info.def file on ce       |
        |              |                | under test                                                |
        | Returns:     | configuration command output and error as strings                          |
        | Exception:   | Throws exception on error.                                                 |
    '''
    my_conf = cream_testsuite_conf.CreamTestsuiteConfSingleton()
    batch_sys = my_conf.getParam('batch_system','batch_sys')
    batch_master_host = my_conf.getParam('batch_system','batch_master_host')
    ce_host = my_conf.getParam('submission_info','ce_host')

    command = "/opt/glite/yaim/bin/yaim -c -s " + site_info_file + " -n creamCE" 

    print "Batch sys is " + batch_sys
    print "Batch master is: " + batch_master_host
    print "ce_host is: " + ce_host

    if batch_sys == "pbs":
        if ce_host == batch_master_host:
            command = command + " -n TORQUE_server -n TORQUE_utils"
        else:
            command = command + " -n TORQUE_utils"

    if batch_sys == "lsf":
        command = command + " -n LSF_utils"

    if (batch_sys != "pbs") and (batch_sys != "lsf"):
        raise  _error("Batch system %s is NOT supported" % batch_sys)
    
    print "Exec remote command: " + command

    my_utility = testsuite_utils.CommandMng()

    out, err = my_utility.exec_remote_command(command)

    return out, err

###############################################################################
###############################################################################
def check_if_job_purged(cream_job_id, cream_sandbox):

    '''
        | Description: | Verify two things:                                                         |
        |              | 1) The glite-ce-job-status operation does not find the job anymore         |
        |              | 2) Input and Output sandbox dirs are correctly deleted on the cream-ce     |
        | Arguments:   | cream_job_id  | job that must be purged                                    |
        |              | cream_sandbox | directory where verify that files relative to the job      |
        |              |               | have need cleaned                                          |
        | Returns:     | a string containing JOB PURGED o JOB NOT PURGED                            |
        | Exception:   |                                                                            |
    '''

    ret_val = ['JOB PURGED', 'JOB NOT PURGED']
    my_utility = testsuite_utils.CommandMng()

    # Verify that glite-ce-job-status not find the job anymore
    curr_status = ""
    try:
        print "Trying to get job status ... "
        curr_status = cream_testing.get_current_status(cream_job_id)
    except Exception as exc:
        print "get_current_status throws exception: "
        print exc

    first_part, separator, second_part = cream_job_id.partition("CREAM")
    cream_job_name = separator + second_part

    # Verify if sandbox directory has been cleaned
    com = "find " + cream_sandbox + " -name " + cream_job_name
    print "trying to exec command : " + com
    cmd_out, cmd_err = my_utility.exec_remote_command(com)
    
    if len(curr_status) == 0 and len(cmd_out) == 0 :
        return ret_val[0]
    else :
        return ret_val[1]



#############################################################################################################################
##############################################################################################################################
def job_status_should_be_in(cream_job_id, statuses_list):
    '''
        | Description: | Verify if the given job status is in the provided status list.             |
        |              | Waits for a right status for 5 minutes                                     |
        | Arguments:   | cream_job_id  | (cream job identifier),                                    |
        |              | statuses_list | (Admitted as correct statuses list)                        |
        | Returns:     | Nothing                                                                    |
        | Exceptions:  | _error if the status does not reach an admitted status in five minutes     |

    '''
    final_states = ['DONE-OK', 'DONE-FAILED', 'ABORTED', 'CANCELLED']

    start = datetime.datetime.now()
    time.sleep(5)
    stop = datetime.datetime.now()
    elapsed = stop - start
    while elapsed < datetime.timedelta(minutes=5):
        status = cream_testing.get_current_status(cream_job_id)
        if (status in statuses_list) or (status in final_states):
            break
        else:
            time.sleep(20)
            elapsed = datetime.datetime.now() - start

    print "Detected Status = " + status
    right_otput_str_list = "".join(statuses_list)
    if status not in statuses_list:
        raise _error("Expected status should be in " + right_otput_str_list + " for job " + cream_job_id + " was actually " + status)


#############################################################################################################################
##############################################################################################################################
def append_string_to_file_on_ce(file_to_which_append, string_to_be_appended, output_location):
    '''
        | Description: | Append a string, received in input to the end of a local file received     |
        |              | also as input                                                              |
        | Arguments:   | string | file to which append                                              |
        |              | string | string to be appended                                             |
        |              | string | full path of the output location                                  |
        | Returns:     | Nothing (raises exception uppon non-validation)                            |
        | Exceptions:  |                                                                            |
    '''
    my_utility = testsuite_utils.Utils()
    print "file_to_which_append = " + file_to_which_append
    print "string_to_be_appended = " + string_to_be_appended
    print "output_location = " + output_location
    return my_utility.append_string_to_file_on_ce(file_to_which_append, string_to_be_appended, output_location)


#############################################################################################################################
##############################################################################################################################
def check_ce_GlueForeignKey_GlueCEUniqueID(ce_host):
    '''
        | Description: | Execute an ldapsearch on vs. the ce under test and verify if the result    |
        |              | contains foreignkey and glueceuniqueid                                     |
        | Arguments:   | string | ce host under test                                                |
        | Returns:     | Nothing (raises exception uppon non-validation)                            |
        | Exceptions:  |                                                                            |
    '''
 
    ret_val = ['CHECK SUCCESSFUL', 'CHECK FAILED']

    com = "ldapsearch -h " + ce_host + " -x -p 2170 -b o=grid | grep -i foreignkey | grep -i glueceuniqueid"
   
    my_utility = testsuite_utils.CommandMng()

    output, ret_code = my_utility.exec_command_os(com)

    if ret_code == 0:

        if len(output) == 0:
            print "Match for \"GlueForeignKey: GlueCEUniqueID=" + ce_host + "\" not found in \"\n" + "`" + com + "`" + "\nBug not fixed."
            return ret_val[1]
            
        else:
            exp = re.compile("GlueForeignKey: GlueCEUniqueID=" + ce_host)
            res = exp.match(output)
            if res:
                print 'Match found: ', res.group()
                return ret_val[0]
            else:
                print 'No match found'
                print "Match for \"GlueForeignKey: GlueCEUniqueID=" + ce_host + "\" not found in \"\n" + "`" + com + "`" + "\nBug not fixed."
                return ret_val[1]

    elif ret_code == 1:
        print "Match for \"GlueForeignKey: GlueCEUniqueID=" + ce_host + "\" not found in \"\n" + "`" + com + "`" + "\nBug not fixed."
        return ret_val[1]

    else: 
        print "Error executing command " + com
        print "error code = " + str(ret_code)
        return ret_val[1]


#############################################################################################################################
##############################################################################################################################
def check_cream_dynamic_info(ce_host):
    '''
        | Description: | Execute an ldapsearch on vs. the ce under test and verify if the result    |
        |              | contains 'GlueCEStateWaitingJobs 444444'                                   |
        | Arguments:   | string | ce host under test                                                |   
        | Returns:     | Nothing (raises exception uppon non-validation)                            |
        | Exceptions:  |                                                                            |
  
    '''

    ret_val = ['CHECK SUCCESSFUL', 'CHECK FAILED']

    #com = "ldapsearch -h " + ce_host + " -x -p 2170 -b o=grid | grep -i GlueCEStateWaitingJobs | grep -i 444444"
    com = "ldapsearch -h " + ce_host + " -x -p 2170 -b o=grid | grep -i GlueCEStateWaitingJobs "

    my_utility = testsuite_utils.CommandMng()

    output, ret_code = my_utility.exec_command_os(com)

    if ret_code == 0:

        if len(output) == 0:
            print "Match for GlueCEStateWaitingJobs not found in ldapsearch. Something goes wrong"
            return ret_val[1]

        else:
            exp = re.compile("444444")
            res = exp.match(output)
            if res:
                print 'Match FOUND: ', res.group()
                return ret_val[1]
            else:
                print "444444 NOT FOUND in " + com + " output"
                return ret_val[0]

#############################################################################################################################
##############################################################################################################################
def get_cream_db_access_params():
    '''
        | Description: | Search cream database name, host, username and password in cream       |
        |              | configuration file defined in cream_testsuite_conf.ini.                |
        | Arguments:   | None                                                                   |
        | Returns:     | db_host, db_name, db_user, db_password                                 |
        | Exceptions:  |                                                                        |
    '''

    cream_conf_layout_mng = cream_config_layout_mng.CreamConfigLayoutMng()

    db_user, db_password = cream_conf_layout_mng.get_cream_db_user_password()
    db_host = cream_conf_layout_mng.get_cream_db_host()
    db_name = cream_conf_layout_mng.get_cream_db_name()

    return db_host, db_name, db_user, db_password


#############################################################################################################################
#############################################################################################################################
def get_creamdb_startUpTime_and_creationTime(db_host, db_name, db_user, db_password):
    '''
    '''

    my_mysql_mng = mysql_mng.MysqlMng(db_name, db_user, db_password, db_host)
    db_connection = my_mysql_mng.db_connect(db_host, db_user, db_password, db_name)
    
    col_list = []
    col_list.append("startUpTime")
    col_list.append("creationTime")
    db_connection = my_mysql_mng.db_connect(db_host, db_user, db_password, db_name)
    selected_rows = my_mysql_mng.exec_select("db_info", col_list, db_connection)
    
    print selected_rows

    my_startUpTime = selected_rows[0][0]
    my_creationTime = selected_rows[0][1]

    return my_startUpTime, my_creationTime

#############################################################################################################################
##############################################################################################################################
def check_cream_dynamic_info(ce_host):
    '''
        | Description: | Execute an ldapsearch on vs. the ce under test and verify if the result    |
        |              | contains 'GlueCEStateWaitingJobs 444444'                                   |
        | Arguments:   | string | ce host under test                                                |   
        | Returns:     | Nothing (raises exception uppon non-validation)                            |
        | Exceptions:  |                                                                            |
    
    '''

    ret_val

#############################################################################################################################
##############################################################################################################################
def check_bug_83338(use_cemon_val):
    '''
       | Description: | Perform the following query on the resource bdii of the CREAM CE:           |
       |              | ldapsearch -h <ce_host> -p 2170 -b "o=glue" | grep -i endpointtype          |
       |              | endpointtype should be 3 if CEMon is deployed (USE_CEMON is true).          |
       |              | 2 otherwise.                                                                |   
       | Arguments:   | string | USE_CEMON value set in yaim configuration files                    |
       | Returns:     | check result                                                                |
       | Exceptions:  |                                                                             |
    '''
    ret_val = ['CHECK SUCCESSFUL', 'CHECK FAILED']
   
    my_conf = cream_testsuite_conf.CreamTestsuiteConfSingleton()
    ce_host = my_conf.getParam('submission_info','ce_host')

    com = "ldapsearch -h " + ce_host + " -x -p 2170 -b \"o=glue\" | grep -i endpointtype"

    p1 = subprocess.Popen(["ldapsearch", "-h", ce_host, "-x", "-p", "2170", "-b", "o=glue"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p1.wait()
    p2 = subprocess.Popen(["grep", "-i", "endpointtype"], stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()

    p2.wait()

    fPtr2 = p2.stdout
    output = fPtr2.readlines()
    output="".join(output)

    fPtrErr1 = p1.stderr 
    error=fPtrErr1.readlines()
    error = "".join(error)

    if len(error) != 0:
        raise _error(com + "\ncommand failed. \nCommand reported: " +  error)

    if len(output) == 0:
        print "endpointtype NOT FOUND in `" + com + "`"
        raise _error("endpointtype NOT FOUND in `" + com + "`")
    else:

        ex = re.compile('(?<=endpointType=).', re.IGNORECASE)
        endpoint_type = ex.search(output)

        if endpoint_type is None:
            raise _error("endpointType NOT found in output of %s" % com)

        endpoint_type = endpoint_type.group()
        print "endpoint_type = %s" % endpoint_type

        if (use_cemon_val == "true"):
            if endpoint_type == '3':
                print " use_cemon=%s endpointtype=%s ret_val=%s" % (use_cemon_val, endpoint_type, ret_val[0])
                return ret_val[0]
            else:
                print " use_cemon=%s endpointtype=%s ret_val=%s" % (use_cemon_val, endpoint_type, ret_val[1])
                return ret_val[1]
        else:
            if (use_cemon_val == "false"):
                if endpoint_type == '2':
                    print " use_cemon=%s endpointtype=%s ret_val=%s" % (use_cemon_val, endpoint_type, ret_val[0])
                    return ret_val[0]
                else:
                    print " use_cemon=%s endpointtype=%s ret_val=%s" % (use_cemon_val, endpoint_type, ret_val[1])
                    return ret_val[1]
            else:
                raise _error("Unknown value use_cemon=%s" % use_cemon_val)

    print " use_cemon=%s endpointtype=%s " % (use_cemon_val, endpoint_type)

    return ret_val[1]

#############################################################################################################################
##############################################################################################################################
def check_bug_95552(ce_host):
    '''
       | Description: | Run the command                                                             |
       |              | /usr/libexec/glite-ce-glue2-endpoint-static \                               |
       |              | /etc/glite-ce-glue2/glite-ce-glue2.conf | grep GLUE2EndpointURL             |
       |              | and verify that the URL is correctly defined (contains ":")                 |
       |              | Example of the error:                                                       |
       |              | GLUE2EndpointURL: https://cream-48.pd.infn.it8443/ce-cream/services         |  
       | Arguments:   | string | ce host under test                                                 |  
       | Returns:     | Nothing (raises exception uppon non-validation)                             |
       | Exceptions:  |                                                                             |
    '''

    com = "/usr/libexec/glite-ce-glue2-endpoint-static /etc/glite-ce-glue2/glite-ce-glue2.conf"

    print "Exec remote command: " + com

    my_utility = testsuite_utils.CommandMng()

    out, err = my_utility.exec_remote_command(com)
    print "Output:"
    print out
    print "Error:"
    print err

    if len(err) != 0:
        raise _error("Command " + com + " Returned error: " + err)

    exp = re.compile("GLUE2EndpointURL: https://" + ce_host + ":8443/ce-cream/services")
    res = exp.search(out)
    if res:
        print 'Match found: ', res.group()
    else:
        print 'No match found'
        raise _error("Match for \"GLUE2EndpointURL: https://" + ce_host +  ":8443/ce-cream/services \" not found in \"\n" + "`" + com + "` output" + "\nBug not fixed.")


#############################################################################################################################
##############################################################################################################################
def check_bug_95356(local_copy_of_ComputingShare_ldif):
    '''
       | Description: | Receive as input a local copy of /var/lib/bdii/gip/ldif/ComputingShare.ldif |
       |              | Append an empty GLUE2PolicyRule: to the file; put the modified file on ce;  |
       |              | run '/var/lib/bdii/gip/plugin/glite-info-dynamic-scheduler-wrapper' on ce   |
       |              | and verify that no exceptions are raised.                                   |  
       | Arguments:   | string | local copy of /var/lib/bdii/gip/ldif/ComputingShare.ldif           |
       | Returns:     | the result of the check                                                     |
       | Exceptions:  |                                                                             |
    '''

    ret_val = ['SUCCESS', 'FAILED']

    my_utility = testsuite_utils.Utils()
    cmd_mng = testsuite_utils.CommandMng()

    print "++++++++ Modify the file"
    with open(local_copy_of_ComputingShare_ldif, "a") as myfile:
        myfile.write("GLUE2PolicyRule:\n")

    myfile.close()

    print "++++++++ Put modified file on ce"
    my_utility.put_file_on_ce(local_copy_of_ComputingShare_ldif, "/var/lib/bdii/gip/ldif/ComputingShare.ldif")

    print "++++++++ Exec the test"

    cmd = "/var/lib/bdii/gip/plugin/glite-info-dynamic-scheduler-wrapper"
    try:
        out, err = cmd_mng.exec_remote_command(cmd)
        print "Output:"
        print out
        print "Error:"
        print err
        print "Test SUCCESSFULL"
        return ret_val[0]
    except Exception as e:
        print "Test FAILED with exception:"
        print e
        return ret_val[1]


#############################################################################################################################
##############################################################################################################################
def check_bug_59871():
    '''
       | Description: | Execute an ldapsearch vs. the ce resource,                                  |
       |              | search GlueHostApplicationSoftwareRunTimeEnvironment                        |
       |              | and verify that  are present tree rows:                                     |
       |              | GlueHostApplicationSoftwareRunTimeEnvironment: tag1                         |
       |              | GlueHostApplicationSoftwareRunTimeEnvironment: tag2                         | 
       |              | GlueHostApplicationSoftwareRunTimeEnvironment: tag3                         |            
       | Arguments:   | none                                                                        |  
       | Returns:     | The result of the check                                                     |
       | Exceptions:  |                                                                             | 
    '''

    my_conf = cream_testsuite_conf.CreamTestsuiteConfSingleton()
    ce_host = my_conf.getParam('submission_info','ce_host')

    com = "ldapsearch -h " + ce_host + " -x -p 2170 -b mds-vo-name=resource,o=grid | grep -i GlueHostApplicationSoftwareRunTimeEnvironment"

    p1 = subprocess.Popen(["ldapsearch", "-h", ce_host, "-x", "-p", "2170", "-b", "mds-vo-name=resource,o=grid"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p1.wait()
    p2 = subprocess.Popen(["grep", "-i", "GlueHostApplicationSoftwareRunTimeEnvironment"], stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()

    p2.wait()

    fPtr=p2.stdout
    output=fPtr.readlines()
    output=" ".join(output)

    fPtrErr1=p1.stderr
    error=fPtrErr1.readlines()
    error=" ".join(error)

    if len(error) != 0:
        raise _error("`" + com + "`" + "\ncommand failed \nCommand reported: " +  error)

    if len(output) == 0:
        raise _error("'" + com  + "'" + "Failed: output empty")

    print "Risultato di ldapsearch:"
    print output

    check_result = "OK"
    res = re.search("GlueHostApplicationSoftwareRunTimeEnvironment: tag1", output)
    if res:
        print 'Match found: ', res.group()
    else:
        print 'No match found for GlueHostApplicationSoftwareRunTimeEnvironment: tag1'
        check_result = "KO"

    res = re.search("GlueHostApplicationSoftwareRunTimeEnvironment: tag2", output)
    if res:
        print 'Match found: ', res.group()
    else:
        print 'No match found for GlueHostApplicationSoftwareRunTimeEnvironment: tag2'
        check_result = "KO"

    res = re.search("GlueHostApplicationSoftwareRunTimeEnvironment: tag3", output)
    if res:
        print 'Match found: ', res.group()
    else:
        print 'No match found for GlueHostApplicationSoftwareRunTimeEnvironment: tag3'
        check_result = "KO"

    print "check_bug_59871 result = " + check_result
    return check_result

#############################################################################################################################
##############################################################################################################################
def check_bug_96306():
    '''
       | Description: | Execute an ldapsearch vs. the ce resource,                                  |
       |              | search GLUE2ApplicationEnvironmentID                                        |
       |              | and verify that is present TESTTAG uppercased. Then search                  |
       |              | GLUE2ApplicationEnvironmentAppName and verify that is present TESTTAG       |
       |              | uppercased.                                                                 |
       | Arguments:   | none                                                                        |  
       | Returns:     | The result of the check                                                     |
       | Exceptions:  |                                                                             | 
    '''

    ret_val = ['CHECK SUCCESSFUL', 'CHECK FAILED']

    my_conf = cream_testsuite_conf.CreamTestsuiteConfSingleton()
    ce_host = my_conf.getParam('submission_info','ce_host')

    com = "ldapsearch -h " + ce_host + " -x -p 2170 -b o=glue"

    p1 = subprocess.Popen(["ldapsearch", "-h", ce_host, "-x", "-p", "2170", "-b", "o=glue"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p1.wait()

    fPtr=p1.stdout
    output=fPtr.readlines()
    output=" ".join(output)

    fPtrErr1=p1.stderr
    error=fPtrErr1.readlines()
    error=" ".join(error)

    if error != None and len(error) != 0:
        raise _error("`" + com + "`" + "\ncommand failed \nCommand reported: " +  error)

    if output == None or len(output) == 0:
        raise _error("'" + com  + "'" + "Failed: output empty")

    print "Result of ldapsearch:"
    print output

    test_res = ret_val[1]

    # First search
    ex = re.compile("GLUE2ApplicationEnvironmentID: TESTTAG")
    search_res = ex.search(output)

    if search_res is None:
        print "GLUE2ApplicationEnvironmentID: TESTTAG NOT found in output of " + com
        test_res = ret_val[1]
    else:
        print "GLUE2ApplicationEnvironmentID: TESTTAG found in output of " + com
        test_res = ret_val[0]

        search_res = search_res.group()
        print "case sensitive search of GLUE2ApplicationEnvironmentID: TESTTAG result = %s" % search_res

    # Second search
    ex = re.compile("GLUE2ApplicationEnvironmentAppName: TESTTAG")
    search_res = ex.search(output)

    if search_res is None:
        print "GLUE2ApplicationEnvironmentAppName: TESTTAG NOT found in output of " + com
        test_res = ret_val[1]
    else:
        print "GLUE2ApplicationEnvironmentAppName: TESTTAG found in output of " + com
        test_res = ret_val[0]

        search_res = search_res.group()
        print "case sensitive search of GLUE2ApplicationEnvironmentAppName: TESTTAG result = %s" % search_res

    return test_res


#############################################################################################################################
##############################################################################################################################
def check_bug_87361(config_file, cream_concurrency_level_val):
    '''
       | Description: | check that in the local copy of /etc/glite-ce-cream/cream-config.xml        |
       |              | it is the right configuration of cream_concurrency_level (called            |
       |              | with the right name - depending on EMI version)                             |
       | Arguments:   | string | local copy of /etc/glite-ce-cream/cream-config.xml                 |
       |              | string | cream_concurrency_level value present in yaim configuration        |  
       | Returns:     | The result of the check                                                     |
       | Exceptions:  |                                                                             |
    '''

    ret_val = ['SUCCESS', 'FAILED']

    print "Configuration file name = " + config_file

    # Open configuration file
    try:
        in_file = open(config_file,"r")
    except Exception as exc:
        print "Error opening file " + config_file
        self.my_log.error(exc)
        raise cream_testsuite_exception.CreamTestsuiteError("Error opening file " + config_file)

    # Configure the xml tag (tag_to_search) to search depending on EMI version
    str_to_search = regression_vars.cream_concurrency_level + "=\"" + str(cream_concurrency_level_val) +"\""
    print "String to search = " + str_to_search
    tag_to_search = ""
    if regression_vars.middleware_version.lower() == "emi1":
        print "middleware_version = %s" % regression_vars.middleware_version.lower()
        tag_to_search = '<service id=\"CREAM service '
    elif regression_vars.middleware_version.lower() == "emi2":
        print "middleware_version = %s" % regression_vars.middleware_version.lower()
        tag_to_search = '<commandexecutor id=\"BLAH executor\"'
    else:
        print "middleware_version = %s" % regression_vars.middleware_version.lower()
        raise _error('Invalid middleware version provided. Should be either "EMI1" or "EMI2", but you entered:"' + regression_vars.middleware_version + '"')

    # Select the piece of the file where search the parameter
    str_where_search = ""
    found = False
    while True :
        in_line = in_file.readline()
        if not in_line: break
        print "Tag to search: " + tag_to_search
        if re.search(tag_to_search, in_line):
            found = True
            while re.search('>', in_line) == None :
                str_where_search = str_where_search + in_line + " "
                in_line = in_file.readline()
            break
    print "str_where_search = " + str_where_search

    in_file.close()

    if found is False:
        raise _error(tag_to_search + " not found in " + config_file)

    # Search the parameter
    if re.search(str_to_search, str_where_search):
        print "TEST SUCCESSFUL"
        return ret_val[0]
    else:
        print "TEST FAILED"
        return ret_val[1]



