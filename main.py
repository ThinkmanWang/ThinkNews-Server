#!/usr/bin/python
#coding=utf-8

import MySQLdb
from utils.mysql_python import MysqlPython
from models.User import User
from models.RetModel import RetModel
from utils.user_db_utils import *  
import json
from utils.object2json import obj2json
import hashlib
import time

from flask import Flask
from flask import request

app = Flask(__name__)

def main():
    print 'Hello World'  
    myDB = MysqlPython('thinkman-wang.com', 'thinkman', 'Ab123456', 'db_thinknews')
    
    szSql = 'select * from user'
    result = myDB.select_advanced(szSql)

    for obj in result :
        user = User()
        user.id, user.user_name, user.password = obj
        
        print("%d | %s | %s" % (user.id, user.user_name, user.password))
    
    lstUser = get_all_users()
    for user in lstUser :
        print("%d | %s | %s" % (user.id, user.user_name, user.password))
    
    lstUser = get_all_user_from_pool();
    for user in lstUser :
        print("%d | %s | %s" % (user.id, user.user_name, user.password))   
    
    print obj2json(lstUser)
    
    user = login("18621675203", "a0a475cf454cf9a06979034098167b9e")
    
    if (user != None):
        print obj2json(user)
    else:
        print("login failed")
        
    szToken = ("%s%d" % ("a0a475cf454cf9a06979034098167b9e", int(time.time())))
    print(hashlib.md5(szToken).hexdigest())
    
@app.route("/", methods=['POST', 'GET'])
def index():
    return "Server API for ThinkNews!"

@app.route("/login", methods=['POST', 'GET'])
def login():
    if (request.method != 'POST'):
        return obj2json(RetModel(1, "Server support post only", {}) )
    
    if (request.form['user_name'] is None or request.form['password'] is None):
        return obj2json(RetModel(1, "user_name or password is null"))
    
    user = user_login(request.form['user_name'], request.form['password'])
    
    szRet = ""
    if (user == None):
        szRet = obj2json(RetModel(1, "user_name or password is incorrect", {}) )
    else:
        retModel = RetModel(0, "success", user)
        szRet = obj2json(retModel)
            
    return szRet
    
if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=8000)