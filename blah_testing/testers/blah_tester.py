import cream_testing, blah_testing, cream_regression
import time

def test_notifications_for_normally_finished_jobs():

    # Create_proxy
    cream_testing.create_proxy("sarabINFN","dteam")

    # sleep_jdl(100)
    jdl_fname = cream_testing.sleep_jdl("dteam","100", "/tmp")

    #submit()
    cream_job_id = cream_testing.submit_job(jdl_fname, "cream-06.pd.infn.it:8443/cream-pbs-cert" )
    print cream_job_id
    time.sleep(5)

    #get_final_status()
    print "Getting final job status ... "
    final_job_status = cream_testing.get_final_status(cream_job_id)
    print "Final job status = " + final_job_status

    job_num = blah_testing.get_job_num_from_jid(cream_job_id)
    
    blah_parser_log_file_name = blah_testing.get_blah_parser_log_file_name()
    local_blah_parser_log_file = cream_regression.get_file_from_ce(blah_parser_log_file_name, "/tmp")
    
    time.sleep(200)

    notifications_list = blah_testing.get_notifications_in_blah_parser_log(local_blah_parser_log_file, job_num)    

    print notifications_list

    print blah_testing.check_notifications_for_normally_finished(notifications_list)


def test_notifications_for_cancelled_jobs():

    print "Creating proxy ..."
    cream_testing.create_proxy("sarabINFN","dteam")

    print "Creating jdl"
    jdl_fname = cream_testing.sleep_jdl("dteam","300", "/tmp")

    print "Submitting job " + jdl_fname
    cream_job_id = cream_testing.submit_job(jdl_fname, "cream-06.pd.infn.it:8443/cream-pbs-cert" )
    print cream_job_id
    time.sleep(60)

    print "Verifying status of job " + cream_job_id
    cream_regression.job_status_should_be_in(cream_job_id, ['PENDING', 'RUNNING', 'REALLY-RUNNING'])

    print "Cancelling job " + cream_job_id
    cream_testing.cancel_job(cream_job_id)

    print "Sleeping 200sec"
    time.sleep(200)

    job_num = blah_testing.get_job_num_from_jid(cream_job_id)
    
    blah_parser_log_file_name = blah_testing.get_blah_parser_log_file_name()
    local_blah_parser_log_file = cream_regression.get_file_from_ce(blah_parser_log_file_name, "/tmp")
    
    time.sleep(200)

    notifications_list = blah_testing.get_notifications_in_blah_parser_log(local_blah_parser_log_file, job_num)

    print notifications_list

    print blah_testing.check_notifications_for_cancelled(notifications_list)


def test_notifications_for_suspended_resumed_jobs():

    print "Creating proxy ..."
    cream_testing.create_proxy("sarabINFN","dteam")

    print "Creating jdl"
    jdl_fname = cream_testing.sleep_jdl("dteam","300", "/tmp")


    # With PBS and SGE it is possible to suspend only IDLE (i.e. not yet running) jobs.
    # To perform the test, first saturate the batch system, second submit the job which
    # willbe under test.
    # At the end of the test cancel all submitted job to free the batch system
    print "Saturating batch system"
    job_ids_list = blah_testing.saturate_batch_system()

    print "Submitting job " + jdl_fname
    cream_job_id = cream_testing.submit_job(jdl_fname, "cream-06.pd.infn.it:8443/cream-pbs-cert" )
    print cream_job_id
    print "Sleeping 1min"
    time.sleep(60)

    print "Verifying status of job " + cream_job_id
    cream_regression.job_status_should_be_in(cream_job_id, ['IDLE'])

    print "Suspending job ..."
    cream_testing.suspend_job(cream_job_id)

    print "Sleeping 10sec"
    time.sleep(10)

    #check if job suspended on batch system. It is enough check status and verify it is 'HELD'
    print "Verifying status of job " + cream_job_id + ". Should be in 'HELD'"
    cream_regression.job_status_should_be_in(cream_job_id, ['HELD'])
  
    #count = int(len(job_ids_list)/4) 
    #print "Sleep " + str(count) + "sec"
    #time.sleep(count)
    
    print "Cancel job saturating batch system"
    blah_testing.cancel_list_of_jobs(job_ids_list)

    print "Sleeping 5 min ..."
    time.sleep(300)

    print "Resuming job ..."
    cream_testing.resume_job(cream_job_id)

    print "Getting final job status ... "
    final_job_status = cream_testing.get_final_status(cream_job_id)
    print "Final job status = " + final_job_status

    print "Sleeping 30sec"
    time.sleep(30)

    job_num = blah_testing.get_job_num_from_jid(cream_job_id)
    
    blah_parser_log_file_name = blah_testing.get_blah_parser_log_file_name()
    local_blah_parser_log_file = cream_regression.get_file_from_ce(blah_parser_log_file_name, "/tmp")
    
    print "Sleeping 6min."
    time.sleep(360)

    print "Get notifications list in blah parser log file local copy"
    notifications_list = blah_testing.get_notifications_in_blah_parser_log(local_blah_parser_log_file, job_num)

    print notifications_list

    print blah_testing.check_notifications_for_resumed(notifications_list)

    print "Cancelling all jobs..."
    cream_testing.cancel_all_jobs("cream-06.pd.infn.it:8443")

print "####################"
print "Test NORMAL"
test_notifications_for_normally_finished_jobs()

print "####################"
print "Test CANCELLED"
test_notifications_for_cancelled_jobs()

print "####################"
print "Test SUSPENDED"
test_notifications_for_suspended_resumed_jobs()
