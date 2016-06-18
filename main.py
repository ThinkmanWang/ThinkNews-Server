#!/usr/bin/python
#coding=utf-8

import sys
import os

import MySQLdb
from utils.mysql_python import MysqlPython
from models.User import User
from models.RetModel import RetModel
from utils.user_db_utils import *  
import json
from utils.object2json import obj2json
import hashlib
import time

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask import render_template
from werkzeug import secure_filename

#app = Flask(__name__) 
app = Flask(__name__, static_url_path = "/pic", static_folder = "upload")
app.config['UPLOAD_FOLDER'] = 'upload/'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'TXT', 'PDF', 'PNG', 'JPG', 'JPEG', 'GIF'])


'''
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
'''

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def get_file_ext(filename):
    if ('.' in filename):
        return filename.rsplit('.', 1)[1]
    else:
        return ""
    
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

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['avatar']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            savedFileName = hashlib.md5(filename).hexdigest() + "." + get_file_ext(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], savedFileName ) )
            return obj2json(RetModel(0, "Success", {}) )
        else:
            return obj2json(RetModel(2, "Upload failed", {}) )
    else:
        return obj2json(RetModel(2, "Upload failed", {}) )
        
if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=8000)