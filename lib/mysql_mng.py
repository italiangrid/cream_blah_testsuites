import MySQLdb as mdb
import logging

class MysqlMngError(Exception):

    def __init__(self, msg):
        Exception.__init__(self,msg)
        self.msg = msg

    def __str__(self):
        return str(self.msg)


class MysqlMng():

    db_name = ""
    db_user = ""
    db_password = ""
    db_host = ""

    def __init__(self, dbname, dbuser, dbpass, dbhost):
        MysqlMng.db_name
        MysqlMng.db_user
        MysqlMng.db_password
        MysqlMng.db_host
        self.my_log = logging.getLogger('MysqlMng')

    def db_connect(self, db_host, db_user, db_user_password, db_name):
        con = None

        try:
            con = mdb.connect(db_host, db_user, db_user_password, db_name)
            cur = con.cursor()
        except mdb.Error, e:
            print "Error %d: %s" % (e.args[0],e.args[1])
            raise MysqlMngError("Error %d: %s" % (e.args[0],e.args[1]))

        return con

    def exec_select(self, table_name, column_to_select, con):

        clause = column_to_select[0]
        for i in range(1, len(column_to_select)):
            clause = clause + ", " + column_to_select[i]

        rows = None
        with con:

            cur = con.cursor()
            select_cmd = "SELECT " + clause + " FROM " + table_name
            print "select command:"
            print select_cmd
            cur.execute(select_cmd)
            rows = cur.fetchall()
            print "Selected ROWS begin"
            for row in rows:
                for col in row:
                    print "%s," % col
            print "Selected ROWS end"

        return rows

