import logging
import cream_testsuite_conf
import testsuite_utils
import cream_testsuite_exception
import shlex
import re
import os
import subprocess
import paramiko
import datetime
import os
import regression_vars

class CreamConfigLayoutMng():

    def __init__(self):
        
        '''
              | Description:    | Constructor.                                                        |
              | Arguments:      | None.                                                               |
              | Returns:        |                                                                     |
              |Exceptions:      |                                                                     |
        '''

        self.my_log = logging.getLogger('CreamConfigLayoutMng')
        self.my_log.info("Creating CreamConfigLayoutMng object")
        self.my_conf = cream_testsuite_conf.CreamTestsuiteConfSingleton()
        self.ce_host = self.my_conf.getParam('submission_info','ce_host')
        self.admin_name = self.my_conf.getParam('ce_specific','cream_root_usr')
        self.admin_pass = self.my_conf.getParam('ce_specific','cream_root_pass')
        #self.output_dir = self.my_conf.getParam('testsuite_behaviour','tmp_dir')
        self.output_dir = regression_vars.tmp_dir   # The output dir must be always the same in all the testsuite,
                                                    # to allow cleaning procedure
        self.my_utils = testsuite_utils.Utils()

        if len(self.ce_host) == 0:
            raise cream_testsuite_exception.TestsuiteError("Mandatory parameter ce_host is empty. Check testsuite configuration")
        if len(self.admin_name) == 0:
            raise cream_testsuite_exception.TestsuiteError("Mandatory parameter cream_root_usr is empty. Check testsuite configuration")
        if len(self.admin_pass) == 0:
            raise cream_testsuite_exception.TestsuiteError("Mandatory parameter cream_root_pass is empty. Check testsuite configuration")

    def get_cream_db_user_password(self):

        '''
              | Description:    | Search cream database username and password in cream configuration  |
              |                 | file defined in cream_testsuite_conf.ini.                           |
              | Arguments:      | None.                                                               |
              | Returns:        | dbuser, dbpassword.                                                 |
              | Exceptions:     |                                                                     |
        '''

        config_file_name = self.my_conf.getParam('cream-ce_conf_files', 'ce-cream.xml')
        print "Configuration file where search : " + config_file_name
        config_file = self.my_utils.get_file_from_ce(config_file_name, self.output_dir)
        if len(config_file) == 0:
            print "File " + config_file + " NOT FOUND on " + self.ce_host
            raise cream_testsuite_exception.CreamTestsuiteError("File " + config_file + " NOT FOUND on " + self.ce_host)

        print "Configuration file name = " + config_file
        self.my_log.debug("Configuration file name = " + config_file)
        try:
            in_file = open(config_file,"r")
        except Exception as exc:
            self.my_log.error("Error opening file " + config_file)
            print "Error opening file " + config_file
            self.my_log.error(exc)
            raise cream_testsuite_exception.CreamTestsuiteError("Error opening file " + config_file)

        str_where_search = ""
        found = False
        
        while True :
            in_line = in_file.readline()       
            if not in_line: break
            if re.search('<Resource name=\"jdbc/creamdb\"', in_line) or re.search('<dataSource name=\"datasource_creamdb\"', in_line):
                found = True
                while re.search('/>', in_line) == None :
                    str_where_search = str_where_search + in_line + " "
                    in_line = in_file.readline()
                break

        in_file.close()
      
        if found is False:
                self.my_log.critical("<Resource name=\"jdbc/creamdb\" or <dataSource name=\"datasource_creamdb\" not found in " + config_file)
                raise cream_testsuite_exception.CreamTestsuiteError("<Resource name=\"jdbc/creamdb\" or <dataSource name=\"datasource_creamdb\" not found in " + config_file)

        m = re.search('(?<=username=\").*\" ', str_where_search)
        db_u_name = m.group(0)
        db_u_name = db_u_name.replace('\"','')

        m = re.search('(?<=password=\").*\"', str_where_search)
        db_u_pwd = m.group(0)
        db_u_pwd = db_u_pwd.replace('\"','')

        self.my_log.debug("db_user_name = " + db_u_name + "; db_user_password = " + db_u_pwd)

        return db_u_name, db_u_pwd
     

    def check_yaim_param(self, param_name):
    
        ''' | Description: | This function explores all the yaim configuration files following |
            |              | the yaim configuration flow, i.e.                                 |
            |              |   1. /opt/glite/yaim/defaults/site-info.pre                       |
            |              |   2. /opt/glite/yaim/defaults/glite-node-type.pre                 |
            |              |   3. /root/siteinfo/site-info.def                                 |
            |              |   4. /root/siteinfo/services/glite-node-type                      |
            |              |   5. /opt/glite/yaim/defaults/site-info.post                      |
            |              |   6. /opt/glite/yaim/defaults/glite-node-type.post                |
            |              |   7. /root/siteinfo/nodes/machine.domain                          |
            | Arguments:   | param_name is the name of the parameter to search                 | 
            | Returns:     | The value of the parameter "param_name" or an empty string if     |
            |              | parameter not found.                                              |
            | Exceptions:  |                                                                   |

        '''

        yaim_conf_files = []
        param_value = ""

        site_info_pre = self.my_conf.getParam('cream_yaim_conf_files', 'site-info.pre') 
        yaim_conf_files.append(site_info_pre)

        services_glite_creamce_pre = self.my_conf.getParam('cream_yaim_conf_files', 'services-glite-creamce.pre') 
        yaim_conf_files.append(services_glite_creamce_pre)

        site_info = self.my_conf.getParam('cream_yaim_conf_files', 'site-info.def')
        yaim_conf_files.append(site_info) 

        services_glite_creamce = self.my_conf.getParam('cream_yaim_conf_files', 'services-glite-creamce') 
        yaim_conf_files.append(services_glite_creamce)

        site_info_post = self.my_conf.getParam('cream_yaim_conf_files', 'site-info.post') 
        yaim_conf_files.append(site_info_post)

        services_glite_creamce_post = self.my_conf.getParam('cream_yaim_conf_files', 'services-glite-creamce.post')
        yaim_conf_files.append(services_glite_creamce_post)

        node_file = self.my_conf.getParam('cream_yaim_conf_files', 'node-file') 
        yaim_conf_files.append(node_file)

        for file in yaim_conf_files:

            try:
                self.my_log.debug("Getting file " + file + " from ce ")
                print "Getting file " + file + " from ce "
                local_file = self.my_utils.get_file_from_ce(file, self.output_dir)
            except Exception as exc:
                print "File " + file + " does not exists or other error - Skip "
                print str(exc)
                self.my_log.debug("File " + file + " does not exists - Skip or other error")
                continue

            try:
                self.my_log.debug("Searching " + param_name + " in " + local_file)
                print "Searching " + param_name + " in " + local_file
                is_initialized, tmp_param_value = self.my_utils.check_param_in_conf_file(local_file, param_name) 
                print "is_initialized = " + is_initialized
                print "tmp_param_value = " + tmp_param_value 
            except Exception as exc:
                print "Error searching param " + param_name + " in file " + file + " - Skip "
                print str(exc)
                continue

            if is_initialized is "INITIALIZED":
                param_value = tmp_param_value
                print "Param " + param_name + " found in " + file + " with value " + param_value
                self.my_log.debug("Param " + param_name + " found in " + file + " with value " + param_value)

        print "Fine for, param_value = " + param_value

        if len(param_value) == 0:
            print "Param " + param_name + " NOT found in yaim configuration files"
            self.my_log.debug("Param " + param_name + " NOT found in yaim configuration files")

        return param_value

    def chenge_conf_param_in_file(self, file_name, param_name, param_value):

        '''
           | Description: | Add or change, if already present, the provided parameter param_name  |
           |              | in the configuration file 'service_name' with the 'param_value'       |
           | Arguments:   | service_name full name of <site_info_dir>/services/glite-creamce file |
           |              | param_name name of parameter to add/change                            |
           |              | param_value value to assign to param_name                             |
           | Returns:     | nothing                                                               |
        '''

        service_name = self.my_utils.get_file_from_ce(file_name, self.output_dir)

        temp_file =  self.output_dir + "/serv_glite_creamce.tmp"

        print "File get from ce = " + service_name
        print "tmp file = " + temp_file

        com1="egrep -ve \"" + param_name + "\" " + service_name
        com1_print = "egrep -ve \"" + param_name + "\" " + service_name + " > " + temp_file
        com2="echo " +  param_name + "=" + param_value
        com2_print = "echo " +  param_name + "=" + param_value + " >> " + temp_file

        fout1 = open(temp_file, 'w')
        args = shlex.split(com1.encode('ascii'))
        p = subprocess.Popen(args , shell=False , stderr=subprocess.STDOUT , stdout=fout1, stdin=subprocess.PIPE)
        p.communicate()
        retVal=p.wait()
        fout1.close()

        #GNU grep returns 0 on success, 1 if no matches were found, and 2 for other errors (syntax errors, nonexistant input files, etc)
        if retVal != 0 :
            if retVal == 1 :
                self.my_log.debug("Failed executing : `" + com1 + "` - No matches were found. PASS.")
            elif retVal == 2 :
                fout1 = open(temp_file, 'r')
                com1_out = fout1.readlines()
                fout1.close()
                self.my_log.debug("Failed executing : `" + com1 + "`\n" + "".join(com1_out) + " Raise cream_configurator_exceptions.CreamConfiguratorError")
                print "Failed executing : `" + com1 + "`\n" + "".join(com1_out) + " Raise cream_configurator_exceptions.CreamConfiguratorError"
                raise cream_testsuite_exception.CreamTestsuiteError("Failed executing : `" + com1 + "`\n" + "".join(com1_out))
            else :
                self.my_log.debug("Failed executing : `" + com1 + "` - Reason unknown. Raise cream_configurator_exceptions.CreamConfiguratorError.")
                print "Failed executing : `" + com1 + "` - Reason unknown. Raise cream_configurator_exceptions.CreamConfiguratorError."
                raise cream_testsuite_exception.CreamTestsuiteError("Failed executing : `" + com1 + "` - Reason unknown")

        fout2 = open(temp_file, 'a')
        args = shlex.split(com2.encode('ascii'))
        p = subprocess.Popen( args , shell=False , stderr=subprocess.STDOUT , stdout=fout2 , stdin=subprocess.PIPE)
        (outdata, errdata) = p.communicate()
        retVal=p.wait()
        fout2.close()
        if retVal != 0 :
            fout2 = open(temp_file, 'r')
            com2_out = fout2.readlines()
            fout2.close()
            self.my_log.debug("Failed executing : `" + com2 +  "`\n" + "".join(com2_out) + " Raise cream_configurator_exceptions.CreamConfiguratorError")
            print "Failed executing : `" + com2 +  "`\n" + "".join(com2_out) + " Raise cream_configurator_exceptions.CreamConfiguratorError"
            raise cream_configurator_exceptions.CreamConfiguratorError("Failed executing : `" + com2 +  "`\n" + "".join(com2_out))

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        ssh.connect(self.ce_host, username = self.admin_name, password = self.admin_pass)
        sftp = ssh.open_sftp()
        sftp.put(temp_file, file_name)
        sftp.close()

