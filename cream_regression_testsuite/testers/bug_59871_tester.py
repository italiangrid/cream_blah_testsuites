#!/usr/bin/python

import cream_regression, testsuite_utils, testsuite_utils
import shutil, re, time, subprocess

my_utility = testsuite_utils.Utils()

ce_host = "cream-48.pd.infn.it"
vo = "dteam"
file_name = "/opt/glite/var/info/" + ce_host + "/" + vo + "/" + vo + ".list"

myfile, local_copy_of_file_saved = my_utility.append_string_to_file_on_ce(file_name, "tag1 tag2\ntag3", "/tmp")

#print "file_to_get_and_modify: " + file_name
#local_copy_of_file = cream_regression.get_file_from_ce(file_name, "/tmp")
#print "Conf file = " + local_copy_of_file
#local_copy_of_file_saved = local_copy_of_file + ".save"

#shutil.copyfile(local_copy_of_file, local_copy_of_file_saved)


#with open(local_copy_of_file, "a") as myfile:
#    myfile.write("tag1 tag2\ntag3")

#my_utility.put_file_on_ce(local_copy_of_file, file_name)

time.sleep(200)

print cream_regression.check_bug_59871()

#com = "ldapsearch -h " + ce_host + " -x -p 2170 -b mds-vo-name=resource,o=grid | grep -i GlueHostApplicationSoftwareRunTimeEnvironment"
#
#p1 = subprocess.Popen(["ldapsearch", "-h", ce_host, "-x", "-p", "2170", "-b", "mds-vo-name=resource,o=grid"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#p2 = subprocess.Popen(["grep", "-i", "GlueHostApplicationSoftwareRunTimeEnvironment"], stdin=p1.stdout, stdout=subprocess.PIPE)
#
#p2.wait()
#
#fPtr=p2.stdout
#output=fPtr.readlines()
#output=" ".join(output)
#
#fPtrErr1=p1.stderr
#error=fPtrErr1.readlines()
#error=" ".join(error)
#
#if len(error) != 0:
#    raise _error("`" + com + "`" + "\ncommand failed \nCommand reported: " +  error)
#
#if len(output) == 0:
#    raise _error("'" + com  + "'" + "Failed: output empty")
#
#print "Risultato di ldapsearch:"
#print output
#
#check_result = "OK"
#res = re.search("GlueHostApplicationSoftwareRunTimeEnvironment: tag1", output)
#if res:
#    print 'Match found: ', res.group()
#else:
#    print 'No match found for GlueHostApplicationSoftwareRunTimeEnvironment: tag1'
#    check_result = "KO"
#    #raise _error("Match for \"GlueForeignKey: GlueCEUniqueID=" + ce_host + "\" not found in \"\n" + "`" + com + "`" + "\nBug not fixed.")
#
#res = re.search("GlueHostApplicationSoftwareRunTimeEnvironment: tag2", output)
#if res:
#    print 'Match found: ', res.group()
#else:
#    print 'No match found for GlueHostApplicationSoftwareRunTimeEnvironment: tag2'
#    check_result = "KO"
#    #raise _error("Match for \"GlueForeignKey: GlueCEUniqueID=" + ce_host + "\" not found in \"\n" + "`" + com + "`" + "\nBug not fixed.")
#
#res = re.search("GlueHostApplicationSoftwareRunTimeEnvironment: tag3", output)
#if res:
#    print 'Match found: ', res.group()
#else:
#    print 'No match found for GlueHostApplicationSoftwareRunTimeEnvironment: tag3'
#    check_result = "KO"
#    #raise _error("Match for \"GlueForeignKey: GlueCEUniqueID=" + ce_host + "\" not found in \"\n" + "`" + com + "`" + "\nBug not fixed.")
#
#print check_result

my_utility.put_file_on_ce(local_copy_of_file_saved, file_name)
