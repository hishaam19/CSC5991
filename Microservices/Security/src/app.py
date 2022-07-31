from flask import Flask, request, redirect, url_for, render_template, jsonify, Response
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2  
import psycopg2.extras
import re 
import jwt
import datetime
import uuid

application = Flask(__name__)
application.secret_key = 'okteto'
 
conn=psycopg2.connect(dbname='Security', user='okteto', host='10.152.137.106', password='okteto', port='5432')
conn.autocommit=True
cur=conn.cursor() 

@application.route('/login', methods=['GET', 'POST'])
def login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    loginUser = request.get_json()
    if request.method == 'POST' and 'username' in loginUser and 'password' in loginUser:
        username = loginUser['username']
        password = loginUser['password']
        cursor.execute("SELECT * FROM users WHERE username='{0}'".format(username))
        user = cursor.fetchone()
        if user:
            password_rs = user['password']
            if check_password_hash(password_rs, password):
                session_id = str(uuid.uuid1())
                token = str(jwt.encode({
                    'sessionId' : session_id,
                    'userName' : username, 
                    'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)
                }, application.secret_key, "HS256"), 'utf-8')
                cursor.execute("UPDATE users SET sessionId='{0}' WHERE username='{1}'".format(session_id, username))
                conn.commit()
                return jsonify({ 'token' : token })
            else:
                return Response('Incorrect username/password', 400)
        else:
            return Response('Incorrect username/password', 400)
 
    return render_template('login.html')
  
@application.route('/register', methods=['GET', 'POST'])
def register():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    user = request.get_json()
    if request.method == 'POST' and 'username' in user and 'password' in user and 'email' in user and 'role' in user:  
        fullname = user['fullname']
        username = user['username']
        password = user['password']
        role = user['role']
        email = user['email']
        _hashed_password = generate_password_hash(password)
        cursor.execute("SELECT * FROM users WHERE username ='{0}'".format(username,))
        account = cursor.fetchone()
        if account:
            return Response('Account already exists!', 400)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            return Response('Invalid email address', 400)
        elif not re.match(r'[A-Za-z0-9]+', username):
            return Response('Username must contain only characters and numbers!', 400)
        elif not username or not password or not email:
            return Response('Please fill out the form!', 400)
        else:
            cursor.execute("INSERT INTO users (fullname, username, password, email, role) VALUES ('{0}','{1}','{2}','{3}','{4}')".format(fullname, username, _hashed_password, email, role))
            conn.commit()
            return jsonify(user)
   
   
@application.route('/logout')
def logout():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    user_name = request.headers.get('USER_NAME')
    cursor.execute("UPDATE users SET sessionId=NULL WHERE username='{0}'".format(user_name))
    conn.commit()
    return redirect(url_for('login'))
  
@application.route('/profile')
def profile(): 
    user_name = request.headers.get('USER_NAME')
    user = getUser(user_name)
    return jsonify(user)
 
@application.route('/authorize', methods=['POST'])
def authorize():
    token = None
    if 'Authorization' in request.headers:
        token = request.headers.get('Authorization')
    user = authenticate(token)
    if not user:
        return Response('Not Authenticated', 401)
    role = user['role']
    data = request.get_json()
    destination = data['destination']
    if role == 'admin' or destination.startswith("availability") or destination.startswith("scheduling"):
        return jsonify(user)
    if destination.startswith("candidate") and (role == 'candidate' or role == 'recruiter'):
        return jsonify(user)
    if destination.startswith("employee") and (role == 'recruiter' or role == 'interviewer' or role == 'manager'):
        return jsonify(user)
    if destination.startswith("security/profile"):
        return jsonify(user)
    if destination.startswith("security/logout"):
        return jsonify(user)
    return Response('Access Denied', 403)

def authenticate(token):
    if not token:
        return None
    #try:
    updatedToken = token.replace('Bearer ', '', 1)
    data = jwt.decode(updatedToken, application.secret_key, algorithms=["HS256"])
    user = getUser(data['userName'])
    if not user or user['sessionId'] != data['sessionId']:
        return None
    return user
    #except:
    #    return None

def getUser(user_name):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT * FROM users WHERE username='{0}'".format(user_name))
    account = cursor.fetchone()
    return { 'fullName' : account['fullname'], 'userName' : account['username'], 'email' : account['email'], 'sessionId': account['sessionid'], 'password': account['password'], 'role': account['role'] }