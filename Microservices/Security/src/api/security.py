from flask import Blueprint, request, redirect, jsonify, Response
from werkzeug.security import generate_password_hash, check_password_hash
import re 
import jwt
import datetime
import uuid

from models import User, db

secret_key = 'okteto'
bp = Blueprint('security', __name__, url_prefix='/')

@bp.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    if 'username' in body and 'password' in body:
        username = body['username']
        password = body['password']
        user = User.query.filter(User.username == username).first()
        if user:
            password_rs = user.password
            if check_password_hash(password_rs, password):
                session_id = str(uuid.uuid1())
                token = str(jwt.encode({
                    'sessionId' : session_id,
                    'userName' : username, 
                    'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)
                }, secret_key, "HS256"), 'utf-8')
                db.session.commit()
                return jsonify({ 'token' : token })
            else:
                return Response('Incorrect username/password', 400)
        else:
            return Response('Incorrect username/password', 400)
    else:
        return Response('Incorrect username/password', 400)

@bp.route('/register', methods=['POST'])
def register():
    body = request.get_json()
    if 'username' in body and 'password' in body and 'email' in body and 'role' in body:  
        username = body['username']
        password = body['password']
        email = body['email']
        _hashed_password = generate_password_hash(password)
        user = User.query.filter(User.username == username).first()
        if user:
            return Response('Account already exists!', 400)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            return Response('Invalid email address', 400)
        elif not re.match(r'[A-Za-z0-9]+', username):
            return Response('Username must contain only characters and numbers!', 400)
        elif not username or not password or not email:
            return Response('Please fill out the form!', 400)
        else:
            user = User(
                fullname=body['fullname'],
                username=username,
                password=_hashed_password,
                email=email,
                role=body['role']
            )
            db.session.add(user)
            db.session.commit()
            return jsonify(user.serialize())
    else:
        return Response('Invalid request', 400)

@bp.route('/logout', methods=['GET'])
def logout():
    user_name = request.headers.get('USER_NAME')
    user = User.query.filter(User.username == user_name).first()
    if user:
        user.sessionid = None
        db.session.commit()
        return jsonify(user.serialize())
    return jsonify({})

@bp.route('/profile', methods=['GET'])
def profile(): 
    user_name = request.headers.get('USER_NAME')
    user = getUser(user_name)
    return jsonify(user)

@bp.route('/authorize', methods=['POST'])
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
    try:
        updatedToken = token.replace('Bearer ', '', 1)
        data = jwt.decode(updatedToken, secret_key, algorithms=["HS256"])
        user = getUser(data['userName'])
        if not user or user['sessionId'] != data['sessionId']:
            return None
        return user
    except:
        return None

def getUser(user_name):
    user = User.query.filter(User.username == user_name).first()
    if user:
        return user.serialize()
    return ({})