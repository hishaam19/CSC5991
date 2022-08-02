from flask import Blueprint, jsonify, request
from models import Interview, UserInterview
from app import application
import datetime

bp = Blueprint('interview', __name__, url_prefix='/interview')
      
@bp.route('/', methods=['GET'])
def getInterviews():
    items = Interview.query.all()
    result = []
    for item in items:
        result.append(item.serialize())
    return jsonify(result)

@bp.route('/<path:interviewId>', methods=['GET'])
def getInterview(interviewId):
    interview = Interview.query.filter(Interview.id == interviewId).first()
    if interview is None:
        return jsonify({})
    return jsonify(interview.serialize())

@bp.route('/', methods=['POST'])
def addUpdateInterview():
    body = request.get_json()
    interview = None
    if 'id' in body:
        interview = Interview.query.filter(Interview.id == body['id']).first()
    if interview is None:
        if 'startDateTime' in body:
            interview = Interview(
                durationinminutes=body['durationInMinutes'],
                recruiterusername=body['recruiterUsername'],
                candidateusername=body['candidateUsername'],
                startdatetime=body['startDateTime'],
                cancelled=body['cancelled']
            )
        else:
             interview = Interview(
                durationinminutes=body['durationInMinutes'],
                recruiterusername=body['recruiterUsername'],
                candidateusername=body['candidateUsername'],
                cancelled=body['cancelled']
            )           
        db.session.add(interview)
    else:
        interview.durationinminutes=body['yearsOfExperience']
        interview.recruiterusername=body['workLocation']
        interview.candidateusername=body['willingToRelocate']
        interview.cancelled=body['userName']
        if 'startDateTime' not in body:
            interview.startdatetime=body['startDateTime']
    db.session.commit()
    return jsonify(interview.serialize())

@bp.route('/<path:interviewId>', methods=['PUT'])
def cancelInterview(interviewId):
    interview = Interview.query.filter(Interview.id == interviewId).first()
    interview.cancelled=True
    db.session.commit()
    return jsonify(interview)