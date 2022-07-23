from flask import Blueprint, request, jsonify

from models import Configuration, db

bp = Blueprint('configuration', __name__, url_prefix='/configuration')

@bp.route('/', methods=['GET'])
def getAllConfiguration():
    items = Configuration.query.all()
    result = []
    for item in items:
        result.append(item.serialize())
    return jsonify(result)

@bp.route('/', methods=['POST'])
def addConfiguration():
    body = request.get_json()
    new_configuration = Configuration(
        configurationKey=body.configurationKey,
        configurationValue=body.configurationValue
    )
    db.session.add(new_configuration)
    db.session.commit()
    return jsonify(new_configuration)

@bp.route('/<path:configurationKey>', methods=['GET'])
def getConfiguration(configurationKey):
    return jsonify(Configuration.query.filter(Configuration.configurationKey == configurationKey).first())

@bp.route('/<path:configurationKey>', methods=['PUT'])
def updateConfiguration(configurationKey):
    body = request.get_json()
    configuration = Configuration.query.filter(Configuration.configurationKey == configurationKey).first()
    configuration.configurationValue = body.configurationValue
    db.session.commit()
    return jsonify(configuration)

@bp.route('/<path:configurationItem>', methods=['DELETE'])
def deleteConfiguration(configurationKey):
    configuration = Configuration.query.filter(Configuration.configurationKey == configurationKey).delete()
    return jsonify(configuration)
