'''
Job Handling
--

Proxy Handling
--

Data Manipulation
--

JDL Creation
--

Utils
--

CREAM Utils
--


Implemented methods enumeration:
1)  Exec Remote Command
2)  get_remote_command_result
3)  exec_cream_cli_command  
4)  enable_submission
5)  check_allowed_submission
6)  create_rfc_proxy
7)  get_file_from_ce
8)  get_cream_db_user_password_from_config
9)  job_db_admin_purger_script_check
10)  check_parameter
11) delete_job_from_batch_system
12) job_status_should_be_in
13) check_ce_GlueForeignKey_GlueCEUniqueID
14) check_cream_dynamic_info


'''

import subprocess , shlex , os , sys , time , datetime , re , string , paramiko
from string import Template
import batch_sys_mng, cream_testing, testsuite_utils, cream_config_layout_mng, cream_testsuite_conf

class _error(Exception):

        def __init__(self,string):
                self.string = string
        def __str__(self):
                return str(self.string)

##############################################################################################################################
##############################################################################################################################

def exec_remote_command(command):

        '''
                Description:    Executes a generic unix command on the indicated host with provided admin name and password.
                Arguments:      remote cream host, command to execute, administrator name and administrator password. 
                Returns:        nothing.
        '''

        my_utility = testsuite_utils.CommandMng()

        print "Exec remote command: " + command

        my_utility.exec_remote_command(command)

##############################################################################################################################
##############################################################################################################################
def get_remote_command_result(command):

        '''
                Description: Executes a generic unix command on the indicated host with provided admin name and password.   
                Arguments:   remote cream host, command to execute, administrator name and administrator password. 
                Returns:     command output an command error as strings.
        '''

        my_utility = testsuite_utils.CommandMng()

        print "Exec remote command: " + command

        outStr, errStr = my_utility.exec_remote_command(command)

        return outStr, errStr 

##############################################################################################################################
##############################################################################################################################
def exec_cream_cli_command(command):

    '''
        Description:    Executes a generic cream client command.
        Arguments:      cream-cli command.
        Returns:        nothing.
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
def enable_submission(ce_endpoint):

        '''
                Description:    Enables the job submission in the given cream endpoint.
                Arguments:      cream endpoint.
                Returns:        glite-ce-enable-submission command output.
        '''

        com="/usr/bin/glite-ce-enable-submission %s" % ce_endpoint
        ret=exec_cream_cli_command(com)
        out = " ".join(ret)
        out = out.strip()
        out = out.replace (" ", "_")

        return out


##############################################################################################################################
##############################################################################################################################
def get_job_output(target_dir_path, job_id):

    '''
       | Description: | Retrieve the job output saving it in the provided directory |
       | Arguments:   | 
       | Returns:     |
       | Exception:   |
    '''

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
                Description:    Cheks if the job submission in the given cream endpoint is enabled.
                Arguments:      cream endpoint.
                Returns:        glite-ce-allowed-submission command output.
        '''
        time.sleep(20)
        com="/usr/bin/glite-ce-allowed-submission %s" % ce_endpoint
        ret=exec_cream_cli_command(com)
        out = "".join(ret)
        out = out.strip()
        out = out.replace (" ", "_")

        return out

##############################################################################################################################
##############################################################################################################################
def create_rfc_proxy(password, vo, cert=None, key=None, time=None):
        '''
                |  Description:  |  Create a user proxy.                                        |\n
                |  Arguments:    |  password  |  the user's proxy password                      |
                |                |  vo        |  for the voms extention.                        |
                |                |  cert      |  non standard certificate path                  |
                |                |  key       |  non standard key path                          |
                |                |  time      |  the validity period of the proxy. Form: HH:MM  |\n
                |  Returns:      |  nothing.                                                    |
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

#############################################################################################################################
##############################################################################################################################
def create_jdl_87492(vo, output_dir):
    '''
        | Description:    | Create a jdl specific to test bug #87492              |
        | Arguments:      |   vo           |   virtual organisation               |
        |                 |   output_dir   |   the directory to put the file in   | 
        | Returns:        | The created jdl path                                  |
        | Exceptions:     |                                                       |
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

    ret_val = ['CHECK SUCCESSFUL', 'CHECK FAILED']

    result = re.search("INFO: Executing function: config_cream_gip_scheduler_plugin_check", job_output)

    if result is None:
        return ret_val[1]
    else:
        return ret_val[0]


#############################################################################################################################
##############################################################################################################################
def get_job_label_from_jid(cream_job_id):

    ''' | Description: | gets the job label (string "CREAM" followed by 9 digits) from job ID |
        | Arguments:   | cream_job_id (cream job identifier)                                  |
        | Returns:     | the job label (string "CREAM" followed by 9 digits)                  |
        | Exceptions:  |                                                                      |
    '''

    first_part, separator, second_part = cream_job_id.partition("CREAM")
    return separator + second_part

#############################################################################################################################
##############################################################################################################################
def get_file_from_ce(file_to_get, output_dir):

        '''
                Description:    Gets the file_to_get from the cream endpoint provided.
                Arguments:      cream endpoint, 
                                admin_name,
                                admin_pass,
                                file to get (full path name).
                Returns:        local full path of retrieved file.
        '''

        my_utility = testsuite_utils.Utils()

        return my_utility.get_file_from_ce(file_to_get, output_dir) 

#############################################################################################################################
##############################################################################################################################
def check_parameter(conf_f, param_to_check):

        '''
            | Description: | This function searches if the parameter param_to_check is present |
            |              | in the provided configuration file                                |    
            | Arguments:   | param_to_check: name of the parameter to search                   |
            |              | conf_f: file where search the parameter.                          |
            | Returns:     | INITIALIZED, NOT_PRESENT, or NOT_INITIALIZED                      |
        '''

        my_utility = testsuite_utils.Utils()
        ret_val, param_value = my_utility.check_param_in_conf_file(conf_f, param_to_check)

        return ret_val

    
#############################################################################################################################
##############################################################################################################################
def get_yaim_param(param_name):

    '''
        | Description: | Call remote object cream_config_layout_mng.CreamConfigLayoutMng      |
        |              | to obtain the value of the parameter param_name                      |
        | Arguments:   | param_name | the parameter name                                      |
        | Returns:     | the parameter value                                                  |
        | Exception:   |                                                                      |
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
        | Description: | Uses the get_yaim_param to get the CREAM_SANDBOX_PATH from yaim     |
        |              | configuration on ce and then parses the result to manage the case   |
        |              | of default value                                                    |
        |              | CREAM_SANDBOX_PATH=${GLITE_CREAM_LOCATION_VAR}/cream_sandbox        |
        | Arguments:   | None                                                                |
        | Returns:     | CREAM_SANDBOX_PATH value configured in yaim                         |
        | Exception:   |                                                                     |
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
def get_cream_db_user_password_from_config():

        '''
           | Description: | Search cream database username and password in cream configuration file. |
           | Arguments:   | None                                                                     |
           | Returns:     | dbuser, dbpassword.                                                      |
        '''
        
        cream_conf_layout_mng = cream_config_layout_mng.CreamConfigLayoutMng()

        return cream_conf_layout_mng.get_cream_db_user_password()

#############################################################################################################################
##############################################################################################################################
def exec_jobDBAdminPurger_sh(db_usr_name, db_usr_pass, conf_f, options):

    '''
        | Description: | Call  remote object cream_config_layout_mng.CreamConfigLayoutMng to      |
        |              | obtain cream database username and object and then call                  |
        |              | Call cream_testsuite_mng.CommandMng remote object ito exec job purging   |
        |              | operation                                                                |
        | Argument:    | options string to add to the jobDBAdminPurger command                    |
        | Returns:     | output and error of the command execution                                |
        | Exception:   |                                                                          |
    '''
    my_conf = cream_testsuite_conf.CreamTestsuiteConfSingleton()
    catalina_home = my_conf.getParam('srv_environment','CATALINA_HOME')
    com = "export CATALINA_HOME=%s; /usr/sbin/JobDBAdminPurger.sh -c %s -u %s -p %s %s" % (catalina_home, conf_f, db_usr_name, db_usr_pass, options)
    print "Executing on CE the command : " + com

    myout, myerr = get_remote_command_result(com)
    print "Command output : " + myout
    print "Command error  : " + myerr

    return myout, myerr

#############################################################################################################################
##############################################################################################################################
def job_db_admin_purger_script_check(db_user_name, db_user_password, conf_f):

        '''
                Description:    Cheks if the JobDBAdminPurger.sh in the given cream endpoint works correctly.
                Arguments:      cream endpoint, admin_name, admin_password, db_user_name, db_user_password.
                Returns:        ??.
        '''

        # Gets the cream configuration file and stores it locally
        # Gets cream database username and password from ce-cream.xml configuration file 
        # Runs the command "export CATALINA_HOME=/var/lib/tomcat5 ; JobDBAdminPurger.sh -c /etc/glite-ce-cream/cream-config.xml -u cremino -p creamtest -s DONE-FAILED,0"
        # Parse the output

        ret_val = ['SUCCESS', 'FAILED']

        options = " -s DONE-FAILED,0"
        
        myout, myerr = exec_jobDBAdminPurger_sh(db_user_name, db_user_password, conf_f, options)
        
        if myerr != "":
                raise _error("Command " + com + " Failed\n" + "Command reported: " +  myerr)               
        if re.search('START jobAdminPurger', myout) and re.search('STOP jobAdminPurger', myout):
                return ret_val[0]
        else:
                return ret_val[1]

#############################################################################################################################
##############################################################################################################################
def delete_job_from_batch_system(cream_job_id, batch_sys):
        '''
                Description:    Manually delete  a job from the declared batch system.
                Arguments:      cream_job_id (cream job identifier), 
                Returns:        Nothing
                Exceptions:     batch_sys_mng.BatchCmdError, batch_sys_mng.JobNotFoundError
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
       | Description: | Add or change, if already present, the provided parameter param_name  |
       |              | in the configuration file 'conf_file' with the 'param_value'          |
       |              | Call cream_configurator_server.CreamConfigurator remote object        |
       | Arguments:   | conf_file full name of file                                           |
       |              | param_name name of parameter to add/change                            |
       |              | param_value value to assign to param_name                             |
       | Returns:     | nothing                                                               |
       | Exceptions:  |                                                                       |
    '''

    cream_conf_layout_mng = cream_config_layout_mng.CreamConfigLayoutMng()

    param_value = cream_conf_layout_mng.chenge_conf_param_in_file(conf_file, param_name, param_value)


###############################################################################
###############################################################################
def run_yaim_func(site_info_file, func_to_run):

    '''
        | Description: | Run yaim function func_to_run using site_info_file as site-ifo.def file |
        | Arguments:   | site_info_file | complete file path name of site-info.def file on ce    |
        |              |                | under test                                             |
        |              | func_to_run    | yaim function to be run                                |
        | Returns:     | Nothing        |                                                        |
        | Exception:   | Throws exception on error.                                              |
    '''

    command = "/opt/glite/yaim/bin/yaim -r -s " + site_info_file + " -n creamCE -f " + func_to_run
    print "Exec remote command: " + command

    my_utility = testsuite_utils.CommandMng()

    my_utility.exec_remote_command(command)

###############################################################################
###############################################################################
def configure_ce_by_yaim(site_info_file):
    '''
        | Description: | Run yaim using site_info_file as site-ifo.def file to configure the ce. |
        |              | Check in testsuite configuration file which batch system is used and if |
        |              | ce is also batch master to set configurations node types                |
        | Arguments:   | site_info_file | complete file path name of site-info.def file on ce    |
        |              |                | under test                                             |
        | Returns:     | configuration command output and error as strings                       |
        | Exception:   | Throws exception on error.                                              |
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
        | Description: | Verify two things:                                                     |
        |              | 1) The glite-ce-job-status operation does not find the job anymore     |
        |              | 2) Input and Output sandbox dirs are correctly deleted on the cream-ce |
        | Arguments:   | cream_job_id  | job that must be purged                                |
        |              | cream_sandbox | directory where verify that files relative to the job  |
        |              |               | have need cleaned                                      |
        | Returns:     | a string containing JOB PURGED o JOB NOT PURGED                        |
        | Exception:   |                                                                        |
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
                   Description:    Verify if the given job status is in the provided status list. 
                                   Waits for a right status for 5 minutes
                   Arguments:      cream_job_id (cream job identifier), 
                                   statuses_list (Admitted as correct statuses list)
                   Returns:        Nothing
                   Exceptions:     _error if the status does not reach an admitted status in five minutes

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
def check_ce_GlueForeignKey_GlueCEUniqueID(ce_host):

        '''
                | Description: |
                | Arguments:   |
                | Returns:     | Nothing (raises exception uppon non-validation)
        '''

        com = "ldapsearch -h " + ce_host + " -x -p 2170 -b o=grid | grep -i foreignkey | grep -i glueceuniqueid"

        p1 = subprocess.Popen(["ldapsearch", "-h", ce_host, "-x", "-p", "2170", "-b", "o=grid"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p2 = subprocess.Popen(["grep", "-i", "foreignkey"], stdin=p1.stdout, stdout=subprocess.PIPE)
        p3 = subprocess.Popen(["grep", "-i", "glueceuniqueid"], stdin=p2.stdout, stdout=subprocess.PIPE)

        p3.wait()

        fPtr=p3.stdout
        output=fPtr.readlines()
        output=" ".join(output)

        fPtrErr1=p1.stderr
        error=fPtrErr1.readlines()
        error=" ".join(error)

        if len(error) != 0:
                raise _error("`" + com + "`" + "\ncommand failed \nCommand reported: " +  error)

        if len(output) == 0:
                raise _error("'" + com  + "'" + "Failed: output empty")

        exp = re.compile("GlueForeignKey: GlueCEUniqueID=" + ce_host)
        res = exp.match(output)
        if res:
                print 'Match found: ', res.group()
        else:
                print 'No match found'
                raise _error("Match for \"GlueForeignKey: GlueCEUniqueID=" + ce_host + "\" not found in \"\n" + "`" + com + "`" + "\nBug not fixed.")
     
#############################################################################################################################
##############################################################################################################################
def check_cream_dynamic_info(ce_host):
        '''
                | Description: |    
                | Arguments:   |   
                | Returns:     |   
        '''

        com = "ldapsearch -h " + ce_host + " -x -p 2170 -b o=grid | grep -i GlueCEStateWaitingJobs | grep -i 444444"
        p1 = subprocess.Popen(["ldapsearch", "-h", ce_host, "-x", "-p", "2170", "-b", "o=grid"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p2 = subprocess.Popen(["grep", "-i", "GlueCEStateWaitingJobs"], stdin=p1.stdout, stdout=subprocess.PIPE)
        p3 = subprocess.Popen(["grep", "-i", "444444"], stdin=p2.stdout, stdout=subprocess.PIPE)

        p3.wait()

        fPtr3=p3.stdout
        output=fPtr3.readlines()
        output="".join(output)

        fPtrErr1=p1.stderr
        error=fPtrErr1.readlines()
        error=" ".join(error)

        if len(error) != 0:
                raise _error(com + "\ncommand failed. \nCommand reported: " +  error)

        if len(output) == 0:
                print "4444444  NOT FOUND in `" + com + "`"
                print "Bug Fixed"
        else:
                raise _error("444444 FOUND in `" + com + "`\nBug not fixed")

#############################################################################################################################
##############################################################################################################################
def check_bug_83338(use_cemon_val):
    '''
       | Description: |    
       | Arguments:   |   
       | Returns:     |   
    '''
    ret_val = ['CHECK SUCCESSFUL', 'CHECK FAILED']
   
    my_conf = cream_testsuite_conf.CreamTestsuiteConfSingleton()
    ce_host = my_conf.getParam('submission_info','ce_host')

    com = "ldapsearch -h " + ce_host + " -x -p 2170 -b \"o=glue\" | grep -i endpointtype"

    p1 = subprocess.Popen(["ldapsearch", "-h", ce_host, "-x", "-p", "2170", "-b", "o=glue"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p2 = subprocess.Popen(["grep", "-i", "endpointtype"], stdin=p1.stdout, stdout=subprocess.PIPE)

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
            if endpoint_type == 3:
                print " use_cemon=%s endpointtype=%s " % (use_cemon_val, endpoint_type)
                return ret_val[0]
            else:
                print " use_cemon=%s endpointtype=%s " % (use_cemon_val, endpoint_type)
                return ret_val[1]
        else:
            if (use_cemon_val == "false"):
                if endpoint_type == 2:
                    print " use_cemon=%s endpointtype=%s " % (use_cemon_val, endpoint_type)
                    return ret_val[0]
                else:
                    print " use_cemon=%s endpointtype=%s " % (use_cemon_val, endpoint_type)
                    return ret_val[1]
            else:
                raise _error("Unknown value use_cemon=%s" % use_cemon_val)

    print " use_cemon=%s endpointtype=%s " % (use_cemon_val, endpoint_type)

    return ret_val[1]







