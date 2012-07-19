
import cream_testing, blah_testing, blah_regression, cream_regression
import time
import datetime

print "Creating proxy ..."
cream_testing.create_proxy("sarabINFN","dteam")

print "Creating jdl"
jdl_fname = cream_testing.sleep_jdl("dteam","150", "/tmp")


# With PBS and SGE it is possible to suspend only IDLE (i.e. not yet running) jobs.
# To perform the test, first saturate the batch system, second submit the job which
# will be under test.
# At the end of the test cancel all submitted job to free the batch system
#print "Saturating batch system"
job_ids_list = blah_testing.saturate_batch_system(jdl_fname)

print "send other 10 jobs"
cream_job_ids = list()
cream_job_ids = blah_testing.submit_n_jobs(10, jdl_fname)

submitted_jobs = cream_job_ids + job_ids_list 

cream_regression.suspend_n_jobs(submitted_jobs)
print "sleep 90"
time.sleep(90)

cream_regression.resume_n_jobs(submitted_jobs)
print "sleep 360"
time.sleep(360)


print "Getting final jobs status ... "
jobs_final_states, failed_jobs = cream_regression.get_n_job_status(submitted_jobs, "DONE-OK", 200)

#jobs_final_states = {'https://cream-48.pd.infn.it:8443/CREAM343000020': 'DONE-OK', 'https://cream-48.pd.infn.it:8443/CREAM860080984': 'DONE-OK', 'https://cream-48.pd.infn.it:8443/CREAM165998598': 'DONE-OK', 'https://cream-48.pd.infn.it:8443/CREAM272504930': 'DONE-OK', 'https://cream-48.pd.infn.it:8443/CREAM028643262': 'DONE-OK', 'https://cream-48.pd.infn.it:8443/CREAM031420087': 'DONE-OK', 'https://cream-48.pd.infn.it:8443/CREAM175340630': 'DONE-OK', 'https://cream-48.pd.infn.it:8443/CREAM860441571': 'DONE-OK', 'https://cream-48.pd.infn.it:8443/CREAM314754532': 'DONE-OK', 'https://cream-48.pd.infn.it:8443/CREAM900734086': 'DONE-OK', 'https://cream-48.pd.infn.it:8443/CREAM925052464': 'DONE-OK', 'https://cream-48.pd.infn.it:8443/CREAM583028808': 'DONE-OK', 'https://cream-48.pd.infn.it:8443/CREAM796407022': 'DONE-OK', 'https://cream-48.pd.infn.it:8443/CREAM346998990': 'DONE-OK', 'https://cream-48.pd.infn.it:8443/CREAM381465963': 'DONE-OK', 'https://cream-48.pd.infn.it:8443/CREAM909432116': 'DONE-OK', 'https://cream-48.pd.infn.it:8443/CREAM070883268': 'DONE-OK', 'https://cream-48.pd.infn.it:8443/CREAM096224245': 'DONE-OK', 'https://cream-48.pd.infn.it:8443/CREAM579038454': 'DONE-OK', 'https://cream-48.pd.infn.it:8443/CREAM500294263': 'DONE-OK', 'https://cream-48.pd.infn.it:8443/CREAM380152351': 'DONE-OK', 'https://cream-48.pd.infn.it:8443/CREAM272710161': 'DONE-OK', 'https://cream-48.pd.infn.it:8443/CREAM751432700': 'DONE-OK', 'https://cream-48.pd.infn.it:8443/CREAM709859316': 'DONE-OK', 'https://cream-48.pd.infn.it:8443/CREAM327028920': 'DONE-OK', 'https://cream-48.pd.infn.it:8443/CREAM972118020': 'DONE-OK', 'https://cream-48.pd.infn.it:8443/CREAM916207691': 'DONE-OK', 'https://cream-48.pd.infn.it:8443/CREAM076071699': 'DONE-OK', 'https://cream-48.pd.infn.it:8443/CREAM610050083': 'DONE-OK', 'https://cream-48.pd.infn.it:8443/CREAM428607805': 'DONE-OK', 'https://cream-48.pd.infn.it:8443/CREAM932934778': 'DONE-OK'}

res = blah_regression.check_for_bug_94414(jobs_final_states)

print res

print "Cancelling all jobs..."
cream_testing.cancel_all_jobs("cream-48.pd.infn.it:8443")

