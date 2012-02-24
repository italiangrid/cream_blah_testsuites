#!/usr/bin/python

import cream_regression, cream_testing
import time
import datetime
import shutil
import os

# create_proxy(password,vo)
cream_testing.create_proxy("sarabINFN","dteam")

# sleep_jdl(vo,secs, output_dir)
jdl_fname = cream_testing.sleep_jdl("dteam","5", "/tmp")

cream_job_id = cream_testing.submit_job(jdl_fname, "cream-06.pd.infn.it:8443/cream-pbs-cert" )
print cream_job_id
time.sleep(5)

# Get yaim_conf_param CREAM_SANDBOX_PATH_old
sandbox_path_value_old = cream_regression.get_cream_sandbox_from_yaim_conf()
print "sandbox_path_value_old = " + sandbox_path_value_old

# Verify that the job is finished (it should be in a terminal state)
print "Getting final job status ... "
final_job_status = cream_testing.get_final_status(cream_job_id)
print "Final job status = " + final_job_status

cream_regression.exec_remote_command("service tomcat5 stop")

now = datetime.datetime.now()
suffix = now.strftime("%Y%m%d_%M%S")
os.mkdir("/tmp/tmp_" + suffix)
local_copy_of_services = cream_regression.get_file_from_ce("/root/sarab_devel/siteinfo/services/glite-creamce", "/tmp/tmp_" + suffix)

print "Saving services file on a local copy _save"
cream_regression.exec_local_command("cp " + local_copy_of_services +  " " + local_copy_of_services + "_save")

# Reconfigure the CE with a different value of CREAM_SANDBOX_PATH
print "Changing configuration parameter ... "
cream_regression.change_conf_param_in_file("/root/sarab_devel/siteinfo/services/glite-creamce", "CREAM_SANDBOX_PATH", "/tmp/cream_sanbox_x")


print "Reconfiguring cream ce ... "
cream_regression.run_yaim_func("/root/sarab_devel/siteinfo/site-info.def", "config_cream_ce")

# Get db username and password
print "Get db username and password from CE"
db_usr_name, db_usr_pass = cream_regression.get_cream_db_user_password_from_config()

# Try, with the JobDBAdminPurger.sh script, to purge the submitted job
print "Running jobDBAdminPurger.sh ... "
cream_job_name =  cream_regression.get_job_label_from_jid(cream_job_id)
print cream_job_name
options =  " --jobIds " + cream_job_name + " -s " + final_job_status

print "Try purge job ..."
cream_regression.exec_jobDBAdminPurger_sh(db_usr_name, db_usr_pass, "/etc/glite-ce-cream/cream-config.xml", " --jobIds " + cream_job_name + " -s " + final_job_status)

# Verify that glite-ce-job-status not find the job anymore
# and that the CREAM sandbox directory for the job has been deleted
print "Verify if job is purged"
final_res = cream_regression.check_if_job_purged(cream_job_id, sandbox_path_value_old)
print final_res

# Test teardown: restore old sandboxdir
print "restore default sandbox deleting the new from services/glite-creamce"
cream_regression.put_file_on_ce(local_copy_of_services + "_save", "/root/sarab_devel/siteinfo/services/glite-creamce")

print "Re-configure running yaim"
cream_regression.configure_ce_by_yaim("/root/sarab_devel/siteinfo/site-info.def")

shutil.rmtree("/tmp/tmp_" + suffix)
