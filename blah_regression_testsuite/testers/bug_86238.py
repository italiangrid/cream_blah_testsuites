# To test the fix configure a CREAM CE with the new blparser.
# Don't use it (i.e. do not submit jobs nor issue any other commands).
# kill the budater and bnotifier processes.
# Wait for 1 minute: you should see that the bupdater and bnotifier have been restarted. 

import cream_regression, blah_regression, cream_testing
import re, time, sys


blparser_with_updater_and_notifier = cream_regression.get_yaim_param("BLPARSER_WITH_UPDATER_NOTIFIER")

print "blparser_with_updater_and_notifier = " + blparser_with_updater_and_notifier

if not blparser_with_updater_and_notifier:
    print "Changing configuration parameter ... "
    cream_regression.change_conf_param_in_file("/root/sarab_devel/siteinfo/services/glite-creamce", "BLPARSER_WITH_UPDATER_NOTIFIER", "true")
 
config_file = cream_regression.get_file_from_ce("/etc/blah.config", "/tmp")
is_initialized = cream_regression.check_parameter(config_file, "blah_check_children_interval")
if is_initialized != "INITIALIZED":
    print "KO - parameter blah_check_children_interval not initialized in /etc/blah.config"
    sys.exit()

print "Create proxy"
cream_testing.create_proxy("sarabINFN","dteam")

print "Clear the ce deleting al jobs"
cream_testing.cancel_all_jobs("cream-06.pd.infn.it:8443")

print "Re-configure the ce"
cream_regression.configure_ce_by_yaim("/root/sarab_devel/siteinfo/site-info.def")

print "Find bupdater and bnotifier pids in `cat /var/blah/blah_bupdater.pid` and `cat /var/blah/blah_bnotifier.pid`"

blah_regression.kill_remote_process_with_pid_file("/var/blah/blah_bupdater.pid")
blah_regression.kill_remote_process_with_pid_file("/var/blah/blah_bnotifier.pid")

time.sleep(61)

if blah_regression.remote_process_is_alive("/usr/bin/BUpdater"):
    print "/usr/bin/BUpdater OK"
else:
    print "/usr/bin/BUpdater KO"

if blah_regression.remote_process_is_alive("/usr/bin/BNotifier"):
    print "/usr/bin/BNotifier OK"
else:
    print "/usr/bin/BNotifier KO"




