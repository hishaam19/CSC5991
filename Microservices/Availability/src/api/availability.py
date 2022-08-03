import json
from flask import Blueprint, request, jsonify, Response

from models import Availability, db

bp = Blueprint('availability', __name__, url_prefix='/availability')

@bp.route('/', methods=['POST'])
def addAvailability():
    body = request.get_json()
    if request.headers.get('USER_ROLE') != body['username']:
        return Response('Access Denied', 403)
    availability  = None
    if 'userName' not in body or 'date' not in body or 'startTime' not in body or 'endTime' not in body:
        return Response('Invalid Request', 400)
    if 'id' in body:
        availability = Availability.query.filter(Availability.id == body['id']).first()
    if Availability is None:
        availability = Availability(
            username = body['userName'],
            date = body['date'],
            starttime = body['startTime'],
            endtime = body['endTime']
        )
        db.session.add(availability)
    else:
        availability.username = body['userName'],
        availability.date = body['date'],
        availability.starttime = body['startTime'],
        availability.endtime = body['endTime']
    db.session.commit()
    return jsonify(availability.serialize())


@bp.route('/<path:username>', methods=['GET'])
def getAvailability(username):
    if request.headers.get('USER_NAME') != username:
        return Response('Access Denied', 403)
    availability = Availability.query.filter(Availability.username == username)
    if availability is None:
        return jsonify({})
    return jsonify(availability.serialize())
