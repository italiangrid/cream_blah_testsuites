
#!/usr/bin/python

import cream_regression, subprocess, sys

# ldapsearch -h cream-35 -x -p 2170 -b "o=grid" | grep -i GlueCEStateWaitingJobs | grep -i 444444

cream_regression.check_cream_dynamic_info("cream-06.pd.infn.it") #Errore ldap
