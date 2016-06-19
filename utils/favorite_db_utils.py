import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'models'))

#print(sys.path)

from mysql_python import MysqlPython
from models.User import User
from models.Favorite import Favorite
import MySQLdb
from DBUtils.PooledDB import PooledDB
import hashlib
import time

g_dbPool = PooledDB(MySQLdb, 5, host='thinkman-wang.com', user='thinkman', passwd='Ab123456', db='db_thinknews', port=3306, charset = "utf8", use_unicode = True);

def get_favorite_of_user(uid, nStart, nPageSize):
    conn = g_dbPool.connection()
    cur=conn.cursor()
    cur.execute("select id, uid, ctime, title, description, picUrl, url from favorite where uid=%s order by id limit %s,%s", \
                (uid, nStart, nPageSize))

    rows=cur.fetchall()

    lstFavorite = []
    for row in rows:
        favorite = Favorite()
        favorite.id = row[0]
        favorite.uid = row[1]
        favorite.ctime = row[2]
        favorite.title = row[3]
        favorite.description = row[4]
        favorite.picUrl = row[5]
        favorite.url = row[6]
        lstFavorite.append(favorite)

    cur.close()
    return lstFavorite

def check_if_favorite_exist():
    conn = g_dbPool.connection(uid, favorite)
    cur=conn.cursor()
    cur.execute("select * from favorite where uid=%s and ctime=%s and title=%s and description=%s and picUrl=%s and url=%s", \
                (uid, favorite.ctime, favorite.title, favorite.description, favorite.picUrl, favorite.url))

    rows=cur.fetchall()
    rows.close()
    
    if (len(rows) > 0):
        return True
    else:
        return False


def insert_favorite_for_user(uid, favorite):
    
    if (check_if_favorite_exist(uid, favorite)):
        favorite.uid = uid
        return favorite 
    
    conn = g_dbPool.connection()
    cur=conn.cursor()
    
    try:
        nRet = cur.execute("insert into favorite(uid, ctime, title, description, picUrl, url) values(%s, %s, %s, %s, %s, %s)", \
                    (uid, favorite.ctime, favorite.title, favorite.description, favorite.picUrl, favorite.url))
    
        nRet=conn.commit()
        
        favorite.uid = uid
        return favorite
    except MySQLdb.Error, e:
        print e
        return None
    finally:
        cur.close()