import paramiko, os, datetime
import testsuite_utils, cream_regression

ce_host = "cream-48.pd.infn.it"
admin_name = 'root'
tester_home = os.environ['HOME']
my_utils = testsuite_utils.Utils()
cmd_mng = testsuite_utils.CommandMng()

print "++++++++ Get local copy of file and save it"
now = datetime.datetime.now()
suffix = now.strftime("%Y%m%d_%M%S")
os.mkdir("/tmp/tmp_" + suffix)

local_copy_of_ComputingShare_ldif = cream_regression.get_file_from_ce("/var/lib/bdii/gip/ldif/ComputingShare.ldif", "/tmp/tmp_" + suffix)

print "++++++++ Saving services file on a local copy _save"
cream_regression.exec_local_command("cp " + local_copy_of_ComputingShare_ldif +  " " + local_copy_of_ComputingShare_ldif + "_save")

print "++++++++ Modify the file" 
with open(local_copy_of_ComputingShare_ldif, "a") as myfile:
    myfile.write("GLUE2PolicyRule:\n")

myfile.close()

print "++++++++ Put modified file on ce"
my_utils.put_file_on_ce(local_copy_of_ComputingShare_ldif, "/var/lib/bdii/gip/ldif/ComputingShare.ldif")

print "++++++++ Exec the test"

cmd = "/var/lib/bdii/gip/plugin/glite-info-dynamic-scheduler-wrapper"
try:
    out, err = cmd_mng.exec_remote_command(cmd)
    print "Output:"
    print out
    print "Error:"
    print err
    print "Test SUCCESSFULL"
except:
    #    #raise _error("Command " + cmd + " Returned error: " + err)
    print "Test FAILED"

print "++++++++ Restore the original file on ce"
my_utils.put_file_on_ce(local_copy_of_ComputingShare_ldif + "_save", "/var/lib/bdii/gip/ldif/ComputingShare.ldif")

# Verify all ok on ce executing the test

out, err = cmd_mng.exec_remote_command(cmd)
print "Output:"
print out
print "Error:"
print err







