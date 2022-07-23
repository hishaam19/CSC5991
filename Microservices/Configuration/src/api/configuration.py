from flask import Blueprint, request

from models import Configuration, db

bp = Blueprint('configuration', __name__, url_prefix='/configuration')

@bp.route('/', methods=['GET'])
def getAllConfiguration():
    return Configuration.query.filter()

@bp.route('/', methods=['POST'])
def addConfiguration():
    body = request.get_json()
    new_configuration = Configuration(
        configurationKey=body.configurationKey,
        configurationValue=body.configurationValue
    )
    db.session.add(new_configuration)
    db.session.commit()
    return new_configuration

@bp.route('/<path:configurationKey>', methods=['GET'])
def getConfiguration(configurationKey):
    return Configuration.query.filter(Configuration.configurationKey == configurationKey).first()

@bp.route('/<path:configurationKey>', methods=['PUT'])
def updateConfiguration(configurationKey):
    body = request.get_json()
    configuration = Configuration.query.filter(Configuration.configurationKey == configurationKey).first()
    configuration.configurationValue = body.configurationValue
    db.session.commit()
    return configuration

@bp.route('/<path:configurationItem>', methods=['DELETE'])
def deleteConfiguration(configurationKey):
    configuration = Configuration.query.filter(Configuration.configurationKey == configurationKey).delete()
    return configuration
