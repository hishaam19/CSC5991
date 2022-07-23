from flask import Blueprint, request
from requests import get, put, post, delete

CONFIGURATION_URL = "https://configuration-service-jmackie80.cloud.okteto.net/"

sites = None

bp = Blueprint('apiproxy', __name__, url_prefix='/api')

@bp.route("/", methods=['GET'])
def proxyRoot():
    return "<p>api proxy</p>"

@bp.route('/<path:api>/', defaults={'path': ''}, methods=['GET', 'PUT', 'POST', 'DELETE'])
@bp.route('/<path:api>/<path:path>', methods=['GET', 'PUT', 'POST', 'DELETE'])
def proxy(api, path):
  getSites()
  if request.method == 'GET':
    return get(f'{sites[api]}{path}').content
  if request.method == 'PUT':
    return put(f'{sites[api]}{path}', data=request.get_json()).content
  if request.method == 'POST':
    return post(f'{sites[api]}{path}', data=request.get_json()).content
  if request.method == 'DELETE':
    return delete(f'{sites[api]}{path}').content
  else:
    return "<p>unknown request</p>"

def getSites():
  global sites
  if sites is None:
    site_configuration = get(f'{CONFIGURATION_URL}configuration/sites').json()
    sites = site_configuration['configurationValue']
  return sites