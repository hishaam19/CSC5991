from flask import Blueprint, request, Response
from requests import get, put, post, delete

CONFIGURATION_URL = "https://configuration-service-jmackie80.cloud.okteto.net/"
SECURITY_URL = "https://security-service-jmackie80.cloud.okteto.net/"

sites = None

bp = Blueprint('apiproxy', __name__, url_prefix='/api')

@bp.route("/", methods=['GET'])
def proxyRoot():
    return "<p>api proxy</p>"

@bp.route('/<path:api>/', defaults={'path': ''}, methods=['GET', 'PUT', 'POST', 'DELETE'])
@bp.route('/<path:api>/<path:path>', methods=['GET', 'PUT', 'POST', 'DELETE'])
def proxy(api, path):
  # authorize user
  security_response = get(f'{CONFIGURATION_URL}authorize', headers= {'Authorization': request.headers.get('Authorization')})
  status_code = security_response.status_code
  if status_code == 403:
    return Response('Access Denied', 403)
  if status_code == 401 or status_code >= 300 or status_code < 200:
    return Response('Not Authenticated', 401)
  user = security_response.json()
  headers = {'USER_NAME': user['userName'], 'USER_SESSION_ID': user['sessionId'], 'USER_FULL_NAME': user['fullName'], 'USER_EMAIL': user['email']}

  # forward to internal service
  getSites()
  if request.method == 'GET':
    return get(f'{sites[api]}{path}', headers=headers).content
  if request.method == 'PUT':
    return put(f'{sites[api]}{path}', data=request.get_json(), headers=headers).content
  if request.method == 'POST':
    return post(f'{sites[api]}{path}', data=request.get_json(), headers=headers).content
  if request.method == 'DELETE':
    return delete(f'{sites[api]}{path}', headers=headers).content
  else:
    return "<p>unknown request</p>"

def getSites():
  global sites
  if sites is None:
    site_configuration = get(f'{CONFIGURATION_URL}configuration/sites').json()
    sites = site_configuration['configurationValue']
  return sites