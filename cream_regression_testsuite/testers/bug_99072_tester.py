#!/usr/bin/python

import cream_regression, testsuite_utils
import re

cmd_mng = testsuite_utils.CommandMng()
cmd = "/usr/bin/glite_cream_load_monitor /etc/glite-ce-cream-utils/glite_cream_load_monitor.conf --show"
out, err = cmd_mng.exec_remote_command(cmd)

m = re.search('(?<=Detected value for Tomcat FD:).*', out)
res = m.group(0).strip()
print "res = "+res

