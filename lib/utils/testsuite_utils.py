import sys, os, subprocess, shlex, re 
import logging
import paramiko
import cream_testsuite_exception
import cream_testsuite_conf

class CommandMng():

    my_log = None
    my_conf = None
    my_ce_host = ""
    my_admin_name = ""
    my_admin_pass = ""

    def __init__(self):
        self.my_log = logging.getLogger('CommandMng')
        CommandMng.my_conf = cream_testsuite_conf.CreamTestsuiteConfSingleton()
        CommandMng.my_ce_host = CommandMng.my_conf.getParam('submission_info','ce_host')
        CommandMng.my_admin_name = CommandMng.my_conf.getParam('ce_specific','cream_root_usr')
        CommandMng.my_admin_pass = CommandMng.my_conf.getParam('ce_specific','cream_root_pass')

        if len(CommandMng.my_ce_host) == 0:
            raise cream_testsuite_exception.TestsuiteError("Mandatory parameter ce_host is empty. Check testsuite configuration")
        if len(CommandMng.my_admin_name) == 0:
            raise cream_testsuite_exception.TestsuiteError("Mandatory parameter cream_root_usr is empty. Check testsuite configuration")
        if len(CommandMng.my_admin_pass) == 0:
            raise cream_testsuite_exception.TestsuiteError("Mandatory parameter cream_root_pass is empty. Check testsuite configuration")

    def exec_command(self, command):

            '''
                 |  Description:    | Executes a generic shell command.          |
                 |  Arguments:      | command, a generic shell command.          |
                 |  Returns:        | command output and error as strings.       |
                 |  Exceptions:     | throws an exception if something goes bad. |
            '''
          
            self.my_log.info("Executing command : " + command)
            print "Executing command : " + command
            args = shlex.split(command.encode('ascii'))
            p = subprocess.Popen( args , shell=False , stderr=subprocess.PIPE , stdout=subprocess.PIPE )

            retVal = p.wait()

            if p.stdout is not None:
                    out = p.stdout
                    #my_output = out.readlines()
                    my_output = out.read()
                    self.my_log.debug("".join(my_output))
            else:
                    my_output = ""

            if p.stderr is not None:
                    err = p.stderr
                    my_error = err.read()
                    self.my_log.debug("".join(my_error))
            else:
                    my_error = ""
            print "exec local command output: \n" + my_output
            print "exec local command error \n" + my_error

            if retVal != 0 and len(my_output) != 0: 
                if "error" in ','.join(my_output).lower() or "fatal" in ','.join(my_output).lower() or "fault" in ','.join(my_output).lower() or retVal != 0 :
                        raise cream_testsuite_exception.TestsuiteError("Command %s execution failed with return value: %s\nCommand reported: %s" % (command, str(p.returncode), ','.join(my_output)))

            return my_output, my_error


    def exec_remote_command(self, command):

        '''
                | Description:      | Executes a generic unix command on the cream ce under test |
                | Arguments:        | command to execute                                         |
                | Returns:          | command output and error as strings                        |
        '''

        ce_host = CommandMng.my_ce_host
        admin_name = CommandMng.my_admin_name
        admin_pass = CommandMng.my_admin_pass

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ce_host, username=admin_name, password=admin_pass, allow_agent=False)
 
        print "running '%s'" % command
        ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command(command)
    
        exit_status = ssh_stdout.channel.recv_exit_status()
        print "Command %s on ce %s exit status: %s" % (command, ce_host, exit_status)
        if exit_status != 0 :
                client.close()
                raise cream_testsuite_exception.TestsuiteError("Error on command %s execution on %s" % (command, ce_host))
        out = ""
        if ssh_stdout is not None:
            out = []
            for i in ssh_stdout.readlines():
                out.append(i)
        else:
            out = ['']
            print "output of " + command + " is empty"
        if ssh_stderr is not None:
            err = []
            for i in ssh_stderr:
                err.append(i)
        else:
            err =['']
            print "error  of " + command + " is empty"

        return "".join(out), "".join(err)

    
def exec_background_process(self, command):

            '''
                 | Description:    | Executes a command in background.          |
                 | Arguments:      | command, a command (to lauch a process).   |
                 | Returns:        | Nothing.                                   |
                 | Exceptions:     | throws an exception if something goes bad. |
            '''


            self.my_log.info("executing command : " + command)
            os.system(command + " &")



class Utils():

    my_conf = None
    my_ce_host = ""
    my_admin_name = ""
    my_admin_pass = ""

    def __init__(self):
        self.my_log = logging.getLogger('Utils')
        Utils.my_conf = cream_testsuite_conf.CreamTestsuiteConfSingleton()
        Utils.my_ce_host = Utils.my_conf.getParam('submission_info','ce_host')
        Utils.my_admin_name = Utils.my_conf.getParam('ce_specific','cream_root_usr')
        Utils.my_admin_pass = Utils.my_conf.getParam('ce_specific','cream_root_pass')
       
        if len(Utils.my_ce_host) == 0:
            raise cream_testsuite_exception.TestsuiteError("Mandatory parameter ce_host is empty. Check testsuite configuration") 
        if len(Utils.my_admin_name) == 0:
            raise cream_testsuite_exception.TestsuiteError("Mandatory parameter cream_root_usr is empty. Check testsuite configuration")
        if len(Utils.my_admin_pass) == 0:
            raise cream_testsuite_exception.TestsuiteError("Mandatory parameter cream_root_pass is empty. Check testsuite configuration")


    def check_param_in_conf_file(self, conf_f, param_to_check):

        ''' | Description: | This function searches if the parameter param_to_check is present |
            |              | in the provided configuration file conf_f based on the ipothesys  |
            |              | that the configuration file is written as set of pairs            |
            |              | param_name = param_value. It jumps rows containing '#' character  |
            |              | before param_name, supposing they are comments.                   |
            | Arguments:   | conf_f: file where search the parameter.                          |
            |              | param_to_check: name of the parameter to search                   |
            | Returns:     | ret_val: with possible values INITIALIZED, NOT_PRESENT,           |
            |              |          or NOT_INITIALIZED                                       |
            |              | parameter_value may contain the param_to_check value or an empty  |
            |              | string                                                            |
            | Exceptions:  |                                                                   |
        '''

        ret_val = ['INITIALIZED', 'NOT_PRESENT', 'NOT_INITIALIZED']
        param_row = ""
        param_value = ""

        self.my_log.debug("Configuration file name = " + conf_f)
        try:
            in_file = open(conf_f,"r")
        except Exception as exc:
            print "Error opening file " + conf_f
            self.my_log.error("Error opening file " + conf_f)
            self.my_log.error(exc)
            raise cream_testsuite_exception.TestsuiteError("Error opening file " + conf_f)

        in_line = in_file.readline()
        while in_line:
            in_line = in_line.strip()
            if re.search('^#', in_line):
                in_line = in_file.readline()
                continue
            else:
                pass
            if re.search(param_to_check, in_line):
                param_row = in_line
                first_part, separator, second_part = param_row.partition("#")
                self.my_log.debug("first part = " + first_part)
                self.my_log.debug("second part = " + second_part)
                self.my_log.debug("separator = " + separator)
                if len(first_part) == 0:
                    continue
                else:
                    param_row = first_part
                    break
            in_line = in_file.readline()
        in_file.close()

        str_to_match = '(?<=' + param_to_check + '=).*'
        m = re.search(str_to_match, param_row)

        if param_row != "":

            if m == None:
                return ret_val[2], param_value.strip()  # NOT INITIALIZED
            else:
                m = m.group(0)
                self.my_log.debug("Parameter value = __" + m.strip() + "__")
                if m == "" or m == "\n" :
                    return ret_val[2], param_value.strip() # NOT INITIALIZED
                else:
                    param_value = m
                    return ret_val[0], param_value.strip()  # INITIALIZED
        else:
            return ret_val[1], param_value.strip() # NOT PRESENT


    def get_file_from_ce(self, file_to_get, output_dir):

        '''
            | Description: | Gets the file_to_get from the ce cream under test.     |
            | Arguments:   | file to get (full path name)                           |
            |              | output dir | local output path                         |
            | Returns:     | local full path of retrieved file.                     |
            | Exceptions:  |                                                        |
        '''
      
        ce_host = Utils.my_ce_host
        admin_name = Utils.my_admin_name
        admin_pass = Utils.my_admin_pass

        localpath = ""
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #In case the server's key is unknown,
        #we will be adding it automatically to the list of known hosts
        ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))

        ssh.connect(ce_host, username=admin_name, password=admin_pass, allow_agent=False)
        ftp = ssh.open_sftp()
        try:
            ftp.stat(file_to_get)
        except IOError, e:
            if e[0] == 2:
                print "File " + file_to_get + " does NOT exist on " + ce_host 
            raise    
        else:
            print "File " + file_to_get + " exists on " + ce_host 
            localpath = output_dir + "/" + 'local_copy_of_a_cream_file'
            ftp.get(file_to_get, localpath, None)

            print "Download of " + file_to_get + " from " + ce_host + " done."

        ftp.close()
        ssh.close() 

        return localpath


    def put_file_on_ce(self, local_file, remote_file):

        '''
            | Description: | Putss the local_file on the cream ce under test.       |
            | Arguments:   | local_file, remote_file                                |
            | Returns:     | Nothing                                                |
            | Exceptions:  |                                                        |
        '''

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        ssh.connect(self.my_ce_host, username = self.my_admin_name, password = self.my_admin_pass, allow_agent=False)
        sftp = ssh.open_sftp()
        sftp.put(local_file, remote_file)
        sftp.close()


    def check_if_remote_file_exist(self, remote_file):

        '''
            | Description: | Gets the file_to_get from the cream ce under test.     |
            | Arguments:   | file to get (full path name)                           |
            | Returns:     | True/False                                             |
            | Exceptions:  |                                                        |
        '''

        ce_host = Utils.my_ce_host
        admin_name = Utils.my_admin_name
        admin_pass = Utils.my_admin_pass

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #In case the server's key is unknown,
        #we will be adding it automatically to the list of known hosts
        ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))

        ssh.connect(ce_host, username=admin_name, password=admin_pass, allow_agent=False)
        ftp = ssh.open_sftp()
        try:
            ftp.stat(remote_file)
        except IOError, e:
            if e[0] == 2:
                print "File " + remote_file + " does NOT exist on " + ce_host
                ret_val = False
            raise    
        else:
            print "File " + remote_file + " exists on " + ce_host 
            ret_val = True

        ftp.close()
        ssh.close()

        return ret_val
