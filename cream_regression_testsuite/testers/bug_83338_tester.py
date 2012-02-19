
#!/usr/bin/python

import cream_regression

use_cemon_val = cream_regression.get_yaim_param("USE_CEMON")

print cream_regression.check_bug_83338(use_cemon_val) #Errore ldap
