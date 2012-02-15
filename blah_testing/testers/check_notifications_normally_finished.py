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

    time.sleep(200)

    job_num = blah_testing.get_job_num_from_jid(cream_job_id)
    
    blah_parser_log_file_name = blah_testing.get_blah_parser_log_file_name()
    local_blah_parser_log_file = cream_regression.get_file_from_ce(blah_parser_log_file_name, "/tmp")
    
    notifications_list = blah_testing.get_notifications_in_blah_parser_log(local_blah_parser_log_file, job_num)    

    print notifications_list

    print blah_testing.check_notifications_for_normally_finished(notifications_list)


test_notifications_for_normally_finished_jobs()

