
import cream_testing, blah_testing, cream_regression
import time

local_copy_of_blah_config = cream_regression.get_file_from_ce("/etc/blah.config", "/tmp")
#ret_val = INITIALIZED, NOT_PRESENT, or NOT_INITIALIZED
ret_val = cream_regression.check_parameter(local_copy_of_blah_config, "bupdater_use_bhist_for_killed")

print "bupdater_use_bhist_for_killed = " + ret_val + " Should be INITIALIZED"

print "Creating proxy ..."
cream_testing.create_proxy("sarabINFN","dteam")

print "Creating jdl"
jdl_fname = cream_testing.sleep_jdl("dteam","300", "/tmp")

print "Submitting job " + jdl_fname
cream_job_id = cream_testing.submit_job(jdl_fname, "cream-48.pd.infn.it:8443/cream-lsf-cert" )
print cream_job_id
time.sleep(60)

print "Verifying status of job " + cream_job_id
cream_regression.job_status_should_be_in(cream_job_id, ['PENDING', 'RUNNING', 'REALLY-RUNNING'])

print "Cancelling job " + cream_job_id
cream_testing.cancel_job(cream_job_id)

print "Sleeping 200sec"
time.sleep(200)

job_num = blah_testing.get_job_num_from_jid(cream_job_id)
#job_num = "985342878"
blah_parser_log_file_name = blah_testing.get_blah_parser_log_file_name()
local_blah_parser_log_file = cream_regression.get_file_from_ce(blah_parser_log_file_name, "/tmp")
#local_blah_parser_log_file = "/tmp/local_copy_of_a_cream_file"
time.sleep(200)

notifications_list = blah_testing.get_notifications_in_blah_parser_log(local_blah_parser_log_file, job_num)

print notifications_list

print blah_testing.check_notifications_for_cancelled(notifications_list)






