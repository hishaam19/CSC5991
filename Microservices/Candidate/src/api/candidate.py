from flask import Blueprint, request, jsonify, Response

from models import Candidate, db

bp = Blueprint('candidate', __name__, url_prefix='/candidate')

@bp.route('/', methods=['POST'])
def addCandidate():
    body = request.get_json()
    if request.headers.get('USER_ROLE') != 'recruiter' and body['username'] != request.headers.get('USER_NAME'):
        return Response('Access Denied', 403)
    candidate = None
    if 'yearsOfExperience' not in body or 'workLocation' not in body or 'willingToRelocate' not in body or 'phoneNumber' not in body or 'userName' not in body:
        return Response('Invalid Request', 400)
    if 'id' in body:
        candidate = Candidate.query.filter(Candidate.id == body['id']).first()
    if candidate is None:
        candidate = Candidate(
            yearsofexperience=body['yearsOfExperience'],
            worklocation=body['workLocation'],
            willingtorelocate=body['willingToRelocate'],
            phonenumber=body['phoneNumber'],
            username=body['userName']
        )
        db.session.add(candidate)
    else:
        candidate.yearsofexperience=body['yearsOfExperience']
        candidate.worklocation=body['workLocation']
        candidate.willingtorelocate=body['willingToRelocate']
        candidate.phonenumber=body['phoneNumber']
        candidate.username=body['userName']
    db.session.commit()
    return jsonify(candidate.serialize())

@bp.route('/<path:username>', methods=['GET'])
def getCandidate(username):
    if request.headers.get('USER_ROLE') != 'recruiter' and username != request.headers.get('USER_NAME'):
        return Response('Access Denied', 403)
    candidate = Candidate.query.filter(Candidate.username == username).first()
    if candidate is None:
        return jsonify({})
    return jsonify(candidate.serialize())
