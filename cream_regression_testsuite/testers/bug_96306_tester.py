#!/usr/bin/python

import cream_regression, testsuite_utils, testsuite_utils
import shutil, re, time, subprocess

my_utility = testsuite_utils.Utils()
my_cmdmng = testsuite_utils.CommandMng()

ce_host = "cert-41.pd.infn.it"
vo = "dteam"
file_name = "/opt/glite/var/info/" + ce_host + "/" + vo + "/" + vo + ".list"

myfile, local_copy_of_file_saved = my_utility.append_string_to_file_on_ce(file_name, "TESTTAG", "/tmp")


time.sleep(20)

#out, err = my_cmdmng.exec_command("ldapsearch -h cert-41.pd.infn.it -x -p 2170 -b o=grid")
out, err = my_cmdmng.exec_command("ldapsearch -x -H ldap://cert-41.pd.infn.it:2170  -b o=glue")
#out, err = my_cmdmng.exec_remote_command("ldapsearch -x -H ldap://cert-41.pd.infn.it:2170  -b o=glue")
#print "out"
#print out
#print "err"
#print err
#print cream_regression.check_bug_96306()

#my_utility.put_file_on_ce(local_copy_of_file_saved, file_name)
