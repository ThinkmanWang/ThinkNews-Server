#!/usr/bin/python
#coding=utf-8

import sys
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入 
sys.setdefaultencoding('utf-8')

import os

import MySQLdb
from utils.mysql_python import MysqlPython
from models.User import User
from models.RetModel import RetModel
from utils.user_db_utils import *  
from utils.favorite_db_utils import *
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

dict_err_code = { 
    0 : "success" 
    , 1 : "Server support post only" 
    , 10 : "Upload failed" 
    , 20 : "user_name or password is incorrect"
    , 21 : "Token incorrect"
    , 30 : "Add favorite failed"
    , 31 : "Get favorite failed"
}

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

@app.route("/api/login", methods=['POST', 'GET'])
def login():
    if (request.method != 'POST'):
        return obj2json(RetModel(1, dict_err_code[1], {}) )
    
    if (request.form['user_name'] is None or request.form['password'] is None):
        return obj2json(RetModel(20, dict_err_code[20]))
    
    user = user_login(request.form['user_name'], request.form['password'])
    
    szRet = ""
    if (user == None):
        szRet = obj2json(RetModel(1, "user_name or password is incorrect", {}) )
    else:
        retModel = RetModel(0, "success", user)
        szRet = obj2json(retModel)
            
    return szRet

@app.route('/api/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return obj2json(RetModel(2, dict_err_code[2], {}) )
    
    uid = request.form['uid']
    token = request.form["token"]    
    file = request.files['avatar']
    
    if (uid is None or token is None):
        return obj2json(RetModel(21, dict_err_code[21], {}) )     

    if (False == verify_user_token(uid, token)):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        savedFileName = hashlib.md5(filename).hexdigest() + "." + get_file_ext(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], savedFileName ) )
        return obj2json(RetModel(0, dict_err_code[0], {}) )
    else:
        return obj2json(RetModel(2, dict_err_code[2], {}) )    
        
    
@app.route('/api/add_favorite', methods=['GET', 'POST'])
def add_favorite():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )
    
    uid = request.form['uid']
    token = request.form["token"]
    ctime = request.form["ctime"]
    title = request.form["title"]
    description = request.form["description"]
    picUrl = request.form["picUrl"]
    url = request.form["url"]
    
    if (uid is None or token is None):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    
    
    if (False == verify_user_token(uid, token)):
        return obj2json(RetModel(21, dict_err_code[21], {}) )
    
    favorite = Favorite()
    favorite.ctime = ctime
    favorite.title = title
    favorite.description = description
    favorite.picUrl = picUrl
    favorite.url = url
    nRet = insert_favorite_for_user(uid, favorite)
    
    if (None == nRet):
        return obj2json(RetModel(30, dict_err_code[30], {}) )
    
    retModel = RetModel(0, "success", nRet)
    szRet = obj2json(retModel)    
    return szRet

@app.route('/api/get_favorite', methods=['GET', 'POST'])
def get_user_favorite_list():
    if request.method == 'GET':
        return obj2json(RetModel(1, dict_err_code[1], {}) )    
    
    uid = request.form['uid']
    token = request.form["token"]    
    nStart = int(request.form["start"])
    nCount = int(request.form["count"])
    
    if (uid is None or token is None):
        return obj2json(RetModel(21, dict_err_code[21], {}) )     
    
    if (False == verify_user_token(uid, token)):
        return obj2json(RetModel(21, dict_err_code[21], {}) )    
    
    lstFavorite = get_favorite_of_user(uid, nStart, nCount)
    if (None == lstFavorite):
        return obj2json(RetModel(31, dict_err_code[31], {}) )    
    
    retModel = RetModel(0, "success", lstFavorite)
    szRet = obj2json(retModel)    
    return szRet    
        
if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=8000)