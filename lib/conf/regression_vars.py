# Copyright 2011 Dimosthenes Fioretos dfiore -at- noc -dot- edunet -dot- gr
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import cream_testsuite_conf

my_conf = cream_testsuite_conf.CreamTestsuiteConfSingleton()

# ce cream host
ce_host = my_conf.getParam('submission_info', 'ce_host')
print " ce_host = " + ce_host
my_conf.checkIfParamIsNull('ce_host', ce_host)

# Distinguish name of the user performing the tests (e.g.: /C=IT/O=INFN/OU=Personal Certificate/L=Padova/CN=Firstname Secondname")
dn = my_conf.getParam('submission_info', 'dn')
print " dn = " + dn
my_conf.checkIfParamIsNull('dn', dn)

# The cream endpoint to be used (e.g.: ctb04.gridctb.uoa.gr:8443 )
ce_endpoint = my_conf.getParam('submission_info', 'ce_endpoint')
print " ce_endpoint = " + ce_endpoint
my_conf.checkIfParamIsNull('ce_endpoint', ce_endpoint)

# The cream queue to be used (e.g.: cream-pbs-see )
cream_queue = my_conf.getParam('submission_info', 'cream_queue')
print " cream_queue = " + cream_queue
my_conf.checkIfParamIsNull('cream_queue', cream_queue)

# The CREAM endpoint in use for delegation (e.g.: https://ctb04.gridctb.uoa.gr:8443//ce-cream/services/gridsite-delegation )
deleg_endpoint = my_conf.getParam('submission_info', 'deleg_endpoint')
print " deleg_endpoint = " + deleg_endpoint
my_conf.checkIfParamIsNull('deleg_endpoint', deleg_endpoint)

# The user's submitting the jobs virtual organisation (e.g.: see )
vo = my_conf.getParam('submission_info', 'vo')
print " vo = " + vo
my_conf.checkIfParamIsNull('vo', vo)

# The user's submitting the jobs proxy password (e.g.: p4sSw0rD )
proxy_pass = my_conf.getParam('submission_info', 'proxy_pass')
print " proxy_pass = " + proxy_pass
my_conf.checkIfParamIsNull('proxy_pass', proxy_pass)

# Gridftp server used for data transfers (e.g.: se01.isabella.grnet.gr )
gridftp_server = my_conf.getParam('submission_info', 'gridftp_server')
print " gridftp_server = " + gridftp_server
my_conf.checkIfParamIsNull('gridftp_server', gridftp_server)

# LFC directory for data transfers. This directory will be created, it doesn't have to allready exist. Example: /grid/dteam/cream_testing
lfn_dir = my_conf.getParam('submission_info', 'lfn_dir')
print " lfn_dir = " + lfn_dir
my_conf.checkIfParamIsNull('lfn_dir', lfn_dir)

# A directory in the gridftp server.This directory has to allready exist and your vo have write access to it. Used for OSB file storage. Example: /tmp
gridftp_dir = my_conf.getParam('submission_info', 'gridftp_dir')
print " gridftp_dir = " + gridftp_dir
my_conf.checkIfParamIsNull('gridftp_dir', gridftp_dir)

# A delegation id string (e.g.: me_deleg_id )
deleg_id = my_conf.getParam('submission_info', 'deleg_id')
print " deleg_id = " + deleg_id
my_conf.checkIfParamIsNull('deleg_id', deleg_id)

# The log level used during the test.Default is INFO.For extra output,set to DEBUG or TRACE.
# (possible values: NONE FAIL WARN INFO DEBUG TRACE)
log_level = my_conf.getParam('logger', 'robot_framework_log_level')
print " log_level = " + log_level
my_conf.checkIfParamIsNull('log_level', log_level)

#The underlying batch system of the CREAM endpoint.Either pbs or lsf.
batch_system = my_conf.getParam('batch_system', 'batch_sys')
print " batch_system = " + batch_system
my_conf.checkIfParamIsNull('batch_system', batch_system)

# The hostname where TORQUE is running. Example: ctb07.gridctb.uoa.gr
torque_host = my_conf.getParam('batch_system', 'torque_host')
print " torque_host = " + torque_host
my_conf.checkIfParamIsNull('torque_host', torque_host)

# A user on the TORQUE host, who has job admin priviledges and ssh access to the machine. Example: root
torque_admin_user = my_conf.getParam('batch_system', 'torque_admin_user')
print " torque_admin_user = " + torque_admin_user
my_conf.checkIfParamIsNull('torque_admin_user', torque_admin_user)

# The aforementioned user's ssh password. Example: p4sSw0rD
torque_admin_pass = my_conf.getParam('batch_system', 'torque_admin_pass')
my_conf.checkIfParamIsNull('torque_admin_pass', torque_admin_pass)
batch_master_host = my_conf.getParam('batch_system', 'batch_master_host')
my_conf.checkIfParamIsNull('batch_master_host', batch_master_host)
batch_master_admin  = my_conf.getParam('batch_system', 'batch_master_admin')
my_conf.checkIfParamIsNull('batch_master_admin', batch_master_admin)
batch_master_admin_password = my_conf.getParam('batch_system', 'batch_master_admin_password')
my_conf.checkIfParamIsNull('batch_master_admin_password', batch_master_admin_password)

# The hostname where the lrms is running. Example: ctb07.gridctb.uoa.gr
lrms_host=batch_master_host

# A user on the lrms host, who has job admin priviledges and ssh access to the machine. Example: root
lrms_admin_user=batch_master_admin

# The aforementioned user's ssh password. Example: p4sSw0rD
lrms_admin_pass=batch_master_admin_password

# The path in which temporary files will reside.
# They will be automatically cleaned up unless you set the variable delete_files to "False" or explicitely don't run the cleanup test case.
# The path will be created -with its parents-, it doesn't have to exist. You can leave it empty and a temporary directory will be created for you.
# In order to know which temp random directory is used, it is printed in standard output and in the final test suite report.
# Warning: any parent directories created, are not removed! 
# All in all, unless needed for specific reasons, you should leave this variable empty.
tmp_dir = my_conf.getParam('testsuite_behaviour', 'tmp_dir')
print " tmp_dir = " + tmp_dir
my_conf.checkIfParamIsNull('tmp_dir', tmp_dir)

# Delete temporary files (jdl and script files created during the test) or not. Possible values: True False. Defaults to "True"
delete_files = my_conf.getParam('testsuite_behaviour', 'delete_files')
print " delete_files = " + delete_files
my_conf.checkIfParamIsNull('delete_files', delete_files)

# The cream host's root user's ssh password. Example: p4sSw0rD
cream_root_pass = "cmsgrid"
my_conf.checkIfParamIsNull('cream_root_pass', cream_root_pass)

# Path to a second certificate
sec_cert = my_conf.getParam('submission_info', 'sec_cert')
print " sec_cert = " + sec_cert

# Path to a second key
sec_key = my_conf.getParam('submission_info', 'sec_key')
print " sec_key = " + sec_key

# Password for the second certificate
sec_proxy_pass = my_conf.getParam('submission_info', 'sec_proxy_pass')
print " sec_proxy_pass = " + sec_proxy_pass

# CREAM CE configuration files
ce_cream_xml = my_conf.getParam('cream-ce_conf_files', 'ce-cream.xml')
cream_config_xml = my_conf.getParam('cream-ce_conf_files', 'cream-config.xml')
print " ce_cream_xml = " + ce_cream_xml
print " cream_config_xml = " + cream_config_xml
my_conf.checkIfParamIsNull('ce_cream_xml', ce_cream_xml)
my_conf.checkIfParamIsNull('cream_config_xml', cream_config_xml)

# BLAH configuration file 
blah_config = my_conf.getParam('cream-ce_conf_files', 'blah.config')
print " blah_config = " + blah_config
my_conf.checkIfParamIsNull('blah_config', blah_config)

# Yaim-cream configuration files
site_info = my_conf.getParam('cream_yaim_conf_files', 'site-info.def')
services_glite_creamce = my_conf.getParam('cream_yaim_conf_files', 'services-glite-creamce')
print " site_info = " + site_info
print " services_glite_creamce = " + services_glite_creamce
my_conf.checkIfParamIsNull('site-info.def', site_info)
my_conf.checkIfParamIsNull('services_glite_creamce', services_glite_creamce)

# BLAH configuration parameters names 
blah_cream_concurrency_level = my_conf.getParam('blah_parameters', 'blah_cream_concurrency_level')
blah_bupdater_loop_interval = my_conf.getParam('blah_parameters', 'blah_bupdater_loop_interval')
print " blah_cream_concurrency_level = " + blah_cream_concurrency_level
print " blah_bupdater_loop_interval = " + blah_bupdater_loop_interval
my_conf.checkIfParamIsNull('blah_cream_concurrency_level', blah_cream_concurrency_level)
my_conf.checkIfParamIsNull('blah_bupdater_loop_interval', blah_bupdater_loop_interval)

# CREAM configuration parameters names
cream_sandbox_path = my_conf.getParam('cream_parameters', 'cream_sandbox_path')
print " cream_sandbox_path = " + cream_sandbox_path
my_conf.checkIfParamIsNull('cream_sandbox_path', cream_sandbox_path)

# do not change this variable
ce=ce_endpoint + "/" + cream_queue
print " ce = " + ce

# CE specific
ce_admin_user = my_conf.getParam('ce_specific','cream_root_usr')
print " ce_admin_user = " + ce_admin_user
my_conf.checkIfParamIsNull('ce_admin_user', ce_admin_user)

ce_admin_pass =  my_conf.getParam('ce_specific','cream_root_pass')
print " ce_admin_pass = " + ce_admin_pass
my_conf.checkIfParamIsNull('ce_admin_pass', ce_admin_pass)

# The cream db host
creamdb_host = my_conf.getParam('cream_db_params','creamdb_host')
print " creamdb_host = " + creamdb_host
my_conf.checkIfParamIsNull('creamdb_host', creamdb_host)

#The cream db port
creamdb_port = my_conf.getParam('cream_db_params','creamdb_port')
print " creamdb_port = " + creamdb_port
my_conf.checkIfParamIsNull('creamdb_port', creamdb_port)

# The user to read the cream db
creamdb_user = my_conf.getParam('cream_db_params','creamdb_user')
print " creamdb_user = " + creamdb_user
my_conf.checkIfParamIsNull('creamdb_user', creamdb_user)

# The aforementioned user's db pass
creamdb_pass = my_conf.getParam('cream_db_params','creamdb_pass')
print " creamdb_pass = " + creamdb_pass
my_conf.checkIfParamIsNull('creamdb_pass', creamdb_pass)

# The authorization model in use. Either gjaf or argus
authz_model = my_conf.getParam('cream_authorization','authz_model')
print " authz_model = " + authz_model

# The host of the argus service, if applicable
argus_host = my_conf.getParam('cream_authorization','argus_host')
print " argus_host = " + argus_host

# Root user password for ssh access on argus host
argus_root_pass = my_conf.getParam('cream_authorization','argus_root_pass')
print " argus_root_pass = " + argus_root_pass 
 
if authz_model == "argus":
    my_conf.checkIfParamIsNull('argus_host', argus_host)
    my_conf.checkIfParamIsNull('argus_root_pass', argus_root_pass)

#########################################
#
# Variable checking/setting code follows.
# Do not edit. (unless you know what and why you are doing it!)
#
#########################################
import os as _os       # underscored libs aren't included into rf when the module itself is loaded
import tempfile as _tf # same as above

class _error(Exception):
        def __init__(self,string):
                self.string = string
        def __str__(self):
                return str(self.string)

if batch_system != "pbs" and batch_system != "lsf":
        raise _error('Batch system must be either "pbs" or "lsf". You entered: ' + batch_system)

if log_level != "NONE" and log_level != "FAIL" and log_level != "WARN" and log_level != "INFO" and log_level != "DEBUG" and log_level != "TRACE":
        raise _error('Log level must be one of: NONE FAIL WARN INFO DEBUG TRACE. You entered: ' + log_level)

if tmp_dir == "" or tmp_dir[0] != '/' or tmp_dir == "/tmp" or tmp_dir == "/tmp/":
        tmp_dir = _tf.mkdtemp(suffix=".cream_testing", dir="/tmp/") + '/'
else:
        if tmp_dir[-1] != '/':
                tmp_dir += '/'
        _os.system("mkdir -p " + tmp_dir) #this should work under normal circumstances, the code here is kept minimal after all.
print "The files of this testsuite will be stored under: " + tmp_dir

if delete_files != "True" and delete_files != "False":
        delete_files = "True"

