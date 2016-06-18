
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'models'))

#print(sys.path)

from mysql_python import MysqlPython
from models.User import User

import MySQLdb
from DBUtils.PooledDB import PooledDB

def get_all_users() :
    myDB = MysqlPython('thinkman-wang.com', 'thinkman', 'Ab123456', 'db_thinknews')

    szSql = 'select * from user'
    result = myDB.select_advanced(szSql)

    lstUser = []
    for obj in result :
        user = User()
        user.id, user.user_name, user.password = obj
        lstUser.append(user)

    return lstUser

g_dbPool = PooledDB(MySQLdb, 5, host='thinkman-wang.com', user='thinkman', passwd='Ab123456', db='db_thinknews', port=3306);

def get_all_user_from_pool():
    conn = g_dbPool.connection()
    cur=conn.cursor()
    SQL="select * from user"
    cur.execute(SQL)

    rows=cur.fetchall()

    lstUser = []
    for row in rows:
        user = User()
        user.id = row[0]
        user.user_name = row[1]
        user.password = row[2]
        lstUser.append(user)

    cur.close()
    return lstUser

def user_login(user_name, password):
    conn = g_dbPool.connection()
    cur=conn.cursor()    
    cur.execute("select * from view_user where user_name=%s AND password=%s" , (user_name, password))
    #cur.execute("select * from view_user where user_name=\"18621675203\" AND password=\"a0a475cf454cf9a06979034098167b\"")
    
    rows=cur.fetchall()
    lstUser = []
    for row in rows:
        user = User()
        user.id = row[0]
        user.user_name = row[1]
        user.password = row[2]
        user.token = row[3]
        user.create_time = row[4]
        user.expire_time = row[5]
        lstUser.append(user)    
        
    cur.close()
    
    if (lstUser != None and len(lstUser) >= 1):
        return lstUser[0]
    else:
        return None
    
    


