import cream_regression
#import testsuite_utils
import cream_config_layout_mng
import mysql_mng
import MySQLdb as mdb
import datetime
import sys

#def db_connect(db_host, db_user, db_user_password, db_name):
#    con = None
#
#    try:
#
#        con = mdb.connect(db_host, db_user, db_user_password, db_name) 
#
#        cur = con.cursor()
#        #cur.execute("SELECT VERSION()")
#        #data = cur.fetchone()
#        #print "Database version : %s " % data
#    
#    except mdb.Error, e:
#  
#        print "Error %d: %s" % (e.args[0],e.args[1])
#        sys.exit(1)
#    
#    return con
#
#
#def exec_select(table_name, column_to_select, con):
#
#    #con = mdb.connect('localhost', 'testuser', 'test623', 'testdb');
#
#    clause = column_to_select[0]
#    for i in range(1, len(column_to_select)):
#        clause = clause + ", " + column_to_select[i] 
#
#    rows = None
#    with con: 
#
#        cur = con.cursor()
#        select_cmd = "SELECT " + clause + " FROM " + table_name 
#        print "select command:"
#        print select_cmd
#        #cur.execute("SELECT " + clause + " FROM " + table_name)
#        cur.execute(select_cmd)
#
#        rows = cur.fetchall()
#
#        print "Selected ROWS"
#        #for row in rows:
#        #    print row
#        for row in rows:
#            for col in row:
#                print "%s," % col
#                #print "\n"
#        print "Selected ROWS end"
#
#    return rows
#
#cmd_mng = testsuite_utils.CommandMng()
#utils = testsuite_utils.Utils()

db_host, db_name, db_user, db_password = cream_regression.get_cream_db_access_params()
print  "db_name, db_user, db_password, db_host = " + db_name  + ", " + db_user + ", " + db_password + ", " + db_host

#
## Eseguire sul ce:
## mysql -h cert-41 -u root --password="H1C14dfh"  -e "GRANT SELECT (startUpTime, creationTime) on creamdb.db_info to cremino@'cream-12.pd.infn.it' IDENTIFIED BY 'Hellas' WITH GRANT OPTION";
## per garantirmi i permessi
####cmd = " mysql -h " + ce_host + " -u root --password=\"" + mysql_password + "\" -e \"GRANT SELECT (startUpTime, creationTime) on creamdb.db_info to cremino@\'cream-12.pd.infn.it\' IDENTIFIED BY \'Hellas\' WITH GRANT OPTION\";"
#
#
## Eseguire dalla UI (usando mysqldb)
## mysql -h cert-41 -u cremino --password="Hellas"  -e "SELECT startUpTime,creationTime from creamdb.db_info ";

my_startUpTime_before, my_creationTime_before = cream_regression.get_creamdb_startUpTime_and_creationTime(db_host, db_name, db_user, db_password)

## Riconfigurare usando yaim
cream_regression.configure_ce_by_yaim("/root/siteinfo/site-info.def")

# Eseguire nuovamente dalla UI (usando mysqldb)
# mysql -h cert-41 -u cremino --password="Hellas"  -e "SELECT startUpTime,creationTime from creamdb.db_info ";

my_startUpTime_after, my_creationTime_after = cream_regression.get_creamdb_startUpTime_and_creationTime(db_host, db_name, db_user, db_password)

# Verificare che "creationTime_before" = "creationTime_after" e "startUpTime_before" != "startUpTime_after" 

if (my_creationTime_before == my_creationTime_after) and (my_startUpTime_before != my_startUpTime_after):
    print "SUCCESS"
else:  
    print "FAIL"

