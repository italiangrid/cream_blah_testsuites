#To test the fix, configure a CREAM CE using the new blparser.
#Then try a:
#service gLite restart
#It shouldn't report the error message:
#Starting BNotifier: /opt/glite/bin/BNotifier: Error creating and binding socket: Address already in use

import cream_regression, blah_regression
import re

blparser_with_updater_and_notifier = cream_regression.get_yaim_param("BLPARSER_WITH_UPDATER_NOTIFIER")

print "blparser_with_updater_and_notifier = " + blparser_with_updater_and_notifier

if not blparser_with_updater_and_notifier:
    print "Changing configuration parameter ... "
    cream_regression.change_conf_param_in_file("/root/sarab_devel/siteinfo/services/glite-creamce", "BLPARSER_WITH_UPDATER_NOTIFIER", "true")
    cream_regression.configure_ce_by_yaim("/root/sarab_devel/siteinfo/site-info.def")

output, error = cream_regression.get_remote_command_result('service gLite restart')

print "=============================================="
print "OUTPUT:"
print output
print "=============================================="
print "ERROR:"
print error
print "=============================================="

result = blah_regression.check_error_for_bug_84261(error)

print result

