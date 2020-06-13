# -*- coding: utf-8 -*-
import pymysql
import time

# DB settings
db_host = 'localhost'
db_port = 3306
db_name = 'gold_pro'
db_user = 'root'
db_pwd = '52971314'

activity_table = 'activity_info'

class MySQLConnection(object):
    def __init__(self, db_host, db_port, db_name, db_user, db_pwd):
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_pwd = db_pwd
        self._connect()

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    def _connect(self):
        conn = pymysql.connect( \
                        user=self.db_user, \
                        passwd=self.db_pwd, \
                        db=self.db_name, \
                        host=self.db_host, \
                        port=self.db_port, \
                        charset="utf8mb4", \
                        use_unicode=True)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        self.conn, self.cursor = conn, cursor

    def _try_connect(self):
        try:
            self.conn.ping()
        except Exception as e:
            self._connect()

    def execute_select(self, cmd):
        try:
            self._try_connect()
            self.cursor.execute(cmd)
            result = self.cursor.fetchall()
            # result = self.cursor.fetchone()
            return result
        except Exception as e:
            print(e)

    def execute(self, cmd):
        try:
            self._try_connect()
            self.cursor.execute(cmd)
            self.conn.commit()
        except Exception as e:
            print(e)

    def update_or_insert(self, data, table_name, bulk=False):
        if bulk:
            self.db_queue.put([table_name, data])
            return

        """If data exist, then update. else, insert"""
        keys = list(data.keys())
        values = list(data.values())
        
        keys_str = ','.join(['`' + k + '`' for k in keys])
        values_str = ','.join(['%s'] * len(keys))

        # on duplicate key update
        on_dup_update_str = ','.join([k + '=VALUES(' + k + ')' for k in keys])

        cmd = "INSERT INTO `" + table_name + "` (" + keys_str + ")" + " VALUES (" + values_str + ") ON DUPLICATE KEY UPDATE " + on_dup_update_str
        try:
            self._try_connect()
            self.cursor.execute(cmd, values)
            self.conn.commit()
        except Exception as e:
            print(e)

    def close(self):
        self.conn.close()
        
db_connection = MySQLConnection(
    db_host, 
    db_port, 
    db_name, 
    db_user, 
    db_pwd
)