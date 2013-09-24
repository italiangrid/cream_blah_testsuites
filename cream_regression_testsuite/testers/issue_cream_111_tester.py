import cream_regression, cream_testing, batch_sys_mng, time, datetime, sys

print "Creating proxy"
cream_testing.create_proxy("sarabINFN","dteam")
print "proxy created"

print "Creating jdl"
jdl_fname = cream_regression.create_jdl_CREAM_111("/tmp")
print "jdl created"

print "Submitting job"
#  submit_job(jdl_path,ce_endpoint,delegId=None)
#cream_job_id = cream_testing.submit_job(jdl_fname, "cream-06.pd.infn.it:8443/cream-pbs-cert" )
cream_job_id = cream_testing.submit_job(jdl_fname, "cream-23.pd.infn.it:8443/cream-lsf-cert" )
print "Job submitted"


print "waiting until job is finished"
final_job_status = cream_testing.get_final_status(cream_job_id)

print "Job finished. Job final status = " + final_job_status

print "Getting job output"
output_path = cream_regression.get_job_output("/tmp", cream_job_id)

print "Checking job output"
result = cream_regression.check_job_out_CREAM_111(output_path)

print result
