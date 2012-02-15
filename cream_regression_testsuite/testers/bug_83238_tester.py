import cream_regression, cream_testing, batch_sys_mng, time, datetime, sys

# create_proxy(password,vo)
cream_testing.create_proxy("sarabINFN","dteam")

# sleep_jdl(vo,secs, output_dir)
jdl_fname = cream_testing.sleep_jdl("dteam","300", "/tmp")

#  submit_job(jdl_path,ce_endpoint,delegId=None)
#cream_job_id = cream_testing.submit_job(jdl_fname, "cream-06.pd.infn.it:8443/cream-pbs-cert" )
cream_job_id = cream_testing.submit_job(jdl_fname, "cream-06.pd.infn.it:8443/cream-pbs-cert" )

cream_regression.delete_job_from_batch_system(cream_job_id, "pbs", "cream-06.pd.infn.it", "root", "cmsgrid")
#cream_regression.delete_job_from_batch_system(cream_job_id, "pbs", "cream-06.pd.infn.it", "root", "cmsgrid")

cream_regression.job_status_should_be_in(cream_job_id, ['DONE-FAILED', 'CANCELLED'])
