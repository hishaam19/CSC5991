import json
from flask import Blueprint, request, jsonify, Response

from models import Availability, db

bp = Blueprint('reporting', __name__, url_prefix='/reporting')

@bp.route('/', methods=['GET'])
def getReport(username):
    if request.headers.get('USER_NAME') != username:
        return Response('Access Denied', 403)
    reporting = Availability.query.filter(Availability.username == username)
    if reporting is None:
        return jsonify({})
    return jsonify(reporting.serialize())
