import Pyro4, sys

print "############### BEGIN ###############"

Pyro4.config.DETAILED_TRACEBACK = True

nameserver=Pyro4.locateNS(host="cream-06.pd.infn.it", port=22352)
#uri=nameserver.lookup("cream_configurator")
uri=nameserver.lookup("proviamo")

#print "Ready. Object uri =", uri

#print "\n*** installing Pyro's excepthook"
#sys.excepthook=Pyro4.util.excepthook

cream_config_mng=Pyro4.Proxy(uri)

# Try to change services/glite-creamce file on CE

try:
    cream_config_mng.chenge_service_param("/root/sarab_devel/siteinfo/services/glite-creamce", "CREAM_SANDBOX_PATH", "/tmp/cream_sanbox_new")
except Exception:
    print ">>>>>>>>>>>>>> Printing Pyro traceback"
    print('PyRO remote exception:' + (''.join(Pyro4.util.getPyroTraceback())))
    print "<<<<<<<<<<<<<< end of Pyro traceback"

print "                              "    
print "                              "    
print "                              "    
print "                              "    
print "\n*** installing Pyro's excepthook"
sys.excepthook=Pyro4.util.excepthook
#cream_config_mng.chenge_service_param("/root/sarab_devel/siteinfo/services/faulty/glite-creamce", "CREAM_SANDBOX_PATH", "/tmp/cream_sanbox_new")
cream_config_mng.chenge_service_param("/root/sarab_devel/siteinfo/services/glite-creamce", "CREAM_SANDBOX_PATH", "/tmp/cream_sanbox_new")

#try:
#cream_config_mng.run_function("/root/sarab_devel/siteinfo/site-info.def", "config_cream_ce")

print "Done"

#except Exception:
#    print ">>>>>>>>>>>>>> Printing Pyro traceback"
#    print('PyRO remote exception:' + (''.join(Pyro4.util.getPyroTraceback())))
#    print "<<<<<<<<<<<<<< end of Pyro traceback"

