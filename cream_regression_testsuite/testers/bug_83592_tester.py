import cream_regression, cream_testing
import time

print "Create proxy ..."
# create_proxy(password,vo)
cream_regression.create_rfc_proxy("sarabINFN","dteam")

print "Create JDL file ..."
# sleep_jdl(vo,secs, output_dir)
jdl_fname, script_name = cream_testing.isb_client_to_ce_jdl("dteam", "/tmp")

print "Submitting job ..."
cream_job_id = cream_testing.submit_job(jdl_fname, "cream-06.pd.infn.it:8443/cream-pbs-cert" )

time.sleep(120)
print "Getting  and checking final status ..."

cream_regression.job_status_should_be_in(cream_job_id, ['DONE-OK'])
