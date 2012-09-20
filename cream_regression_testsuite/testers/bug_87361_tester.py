#!/usr/bin/python

import cream_regression, regression_vars
import datetime, os, shutil, re

print "Get yaim_conf_param CREAM_CONCURRENCY_LEVEL value"
cream_concurrency_level_old = cream_regression.get_cream_concurrency_level_from_yaim_conf()
print "CREAM_CONCURRENCY_LEVEL = " + cream_concurrency_level_old

#cream_concurrency_level_old = 50

 Save a local copy of services
now = datetime.datetime.now()
suffix = now.strftime("%Y%m%d_%M%S")
os.mkdir("/tmp/tmp_" + suffix)
local_copy_of_services = cream_regression.get_file_from_ce("/root/siteinfo/services/glite-creamce", "/tmp/tmp_" + suffix)

print "Saving services file on a local copy _save"
cream_regression.exec_local_command("cp " + local_copy_of_services +  " " + local_copy_of_services + "_save")

# Reconfigure the CE with a different value of CREAM_CONCURRENCY_LEVEL
print "Changing configuration parameter ... "
cream_concurrency_level_new = int(cream_concurrency_level_old) + 50
cream_regression.change_conf_param_in_file("/root/siteinfo/services/glite-creamce", "CREAM_CONCURRENCY_LEVEL", str(cream_concurrency_level_new))

print "Re-configure running yaim"
cream_regression.configure_ce_by_yaim("/root/siteinfo/site-info.def")

#cream_concurrency_level_new = 100
print "Check CREAM_CONCURRENCY_LEVEL in configuration file"
local_copy_config_file = cream_regression.get_file_from_ce("/etc/glite-ce-cream/cream-config.xml", "/tmp")
#local_copy_config_file = "/tmp/local_copy_of_a_cream_file"
print "Conf file = " + local_copy_config_file

print "Check if parameter " + regression_vars.cream_concurrency_level + " is correctly set in conf file"


config_file_name = regression_vars.ce_cream_xml
print "Configuration file where search : " + config_file_name
config_file = local_copy_config_file
print "Configuration file where search : " + config_file
if len(config_file) == 0:
    print "File " + config_file + " NOT FOUND "
    raise cream_testsuite_exception.CreamTestsuiteError("File " + config_file + " NOT FOUND ")

print cream_regression.check_bug_87361(config_file, cream_concurrency_level_new)


# Test teardown: restore old sandboxdir
print "restore default CREAM_CONCURRENCY_LEVEL deleting the new from services/glite-creamce"
cream_regression.put_file_on_ce(local_copy_of_services + "_save", "/root/siteinfo/services/glite-creamce")

print "Re-configure running yaim"
cream_regression.configure_ce_by_yaim("/root/siteinfo/site-info.def")

shutil.rmtree("/tmp/tmp_" + suffix)



