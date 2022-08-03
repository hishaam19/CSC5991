from flask import Blueprint, request, jsonify, Response

from models import Employee, db

bp = Blueprint('employee', __name__, url_prefix='/employee')

@bp.route('/', methods=['POST'])
def addEmployee():
    body = request.get_json()
    if request.headers.get('USER_ROLE') != 'admin' and body['username'] != request.headers.get('USER_NAME'):
        return Response('Access Denied', 403)
    employee = None
    if 'userName' not in body or 'role' not in body or 'hireDate' not in body or 'salary' not in body:
        return Response('Invalid Request', 400)
    if 'id' in body:
        employee = Employee.query.filter(Employee.id == body['id']).first()
    if employee is None:
        employee = Employee(
            username = body['userName'],
            role = body['role'],
            hiredate = body['hireDate'],
            salary = body['salary']
        )
        db.session.add(employee)
    else:
        employee.username = body['userName'],
        employee.role = body['role'],
        employee.hiredate = body['hireDate'],
        employee.salary = body['salary']
    db.session.commit()
    return jsonify(employee.serialize())

@bp.route('/<path:username>', methods=['GET'])
def getEmployee(username):
    if request.headers.get('USER_ROLE') != 'employee' and username != request.headers.get('USER_NAME'):
        return Response('Access Denied', 403)
    employee = Employee.query.filter(Employee.username == username).first()
    if employee is None:
        return jsonify({})
    return jsonify(employee.serialize())

@bp.route('/<path:username>', methods=['PUT'])
def updateRole(username):
    body = request.get_json()
    if request.headers.get('USER_ROLE') != 'admin' and username != request.headers.get('USER_NAME'):
        return Response('Access Denied', 403)
    employee = Employee.query.filter(Employee.username == username).first()
    if employee is None:
        return jsonify({})
    employee.role = body['role']
    db.session.commit()
    return jsonify(employee.serialize())


