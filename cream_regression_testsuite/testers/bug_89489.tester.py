import cream_regression
import re

output, error = cream_regression.configure_ce_by_yaim("/root/sarab_devel/siteinfo/site-info.def")

print "=============================================="
print "OUTPUT:"
print output
print "=============================================="
print "ERROR:"
print error
print "=============================================="


print cream_regression.check_job_out_89489(output)

