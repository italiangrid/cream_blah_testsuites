#!/usr/bin/python

import cream_regression, re, testsuite_utils

class _error(Exception):

        def __init__(self,string):
                self.string = string
        def __str__(self):
                return str(self.string)

ce_host = "cream-48.pd.infn.it"

# /usr/libexec/glite-ce-glue2-endpoint-static /etc/glite-ce-glue2/glite-ce-glue2.conf | grep GLUE2EndpointURL

#com = "/usr/libexec/glite-ce-glue2-endpoint-static /etc/glite-ce-glue2/glite-ce-glue2.conf | grep GLUE2EndpointURL"
com = "/usr/libexec/glite-ce-glue2-endpoint-static /etc/glite-ce-glue2/glite-ce-glue2.conf"

print "Exec remote command: " + com

my_utility = testsuite_utils.CommandMng()

out, err = my_utility.exec_remote_command(com)
print "Output:"
print out
print "Error:"
print err

if len(err) != 0:
        raise _error("Command " + com + " Returned error: " + err)

exp = re.compile("GLUE2EndpointURL: https://" + ce_host + ":8443/ce-cream/services")
res = exp.match(out)
if res:
        print 'Match found: ', res.group()
else:
        print 'No match found'
        raise _error("Match for \"GLUE2EndpointURL: https://" + ce_host +  ":8443/ce-cream/services \" not found in \"\n" + "`" + com + "` output" + "\nBug not fixed.")

