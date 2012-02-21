import cream_testing, blah_testing, cream_regression
import time

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

