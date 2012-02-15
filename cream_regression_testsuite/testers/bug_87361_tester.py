
#!/usr/bin/python

import cream_regression

config_file = cream_regression.get_file_from_ce("cream-48.pd.infn.it", "root", "cmsgrid", "/etc/blah.config", "/tmp")
print "Conf file = " + config_file
res = cream_regression.check_parameter(config_file, "cream_concurrency_level")

print res
