import json
from flask import Blueprint, request, Response, jsonify
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
  full_path = f'{api}/{path}'
  headers = {'Content-Type': 'application/json'}
  if full_path != "security/login" and full_path != "security/register":
    # authorize user
    print(f'{SECURITY_URL}authorize', { 'destination': full_path }, {'Authorization': request.headers.get('Authorization'), 'Content-Type': 'application/json'})
    security_response = post(f'{SECURITY_URL}authorize', json={ 'destination': full_path }, headers={'Authorization': request.headers.get('Authorization'), 'Content-Type': 'application/json'})
    status_code = security_response.status_code
    if status_code == 403:
      return Response('Access Denied', 403)
    if status_code == 401 or status_code >= 300 or status_code < 200:
      return Response('Not Authenticated', 401)
    user = security_response.json()
    headers['USER_NAME'] = user['userName']
    headers['USER_SESSION_ID'] = user['sessionId']
    headers['USER_FULL_NAME'] = user['fullName']
    headers['USER_EMAIL']= user['email']

  # forward to internal service
  if api == "security":
    site_path = f'{SECURITY_URL}{path}'
  else:
    getSites()
    site_path = f'{sites[api]}{path}'
  if request.method == 'GET':
    return get(url=site_path).content
  if request.method == 'PUT':
    return put(url=site_path, json=request.json, headers=headers).content
  if request.method == 'POST':
    return post(url=site_path, json=request.json, headers=headers).content
  if request.method == 'DELETE':
    return delete(url=site_path, headers=headers).content
  else:
    return "<p>unknown request</p>"

def getSites():
  global sites
  if sites is None:
    site_configuration = get(f'{CONFIGURATION_URL}configuration/sites').json()
    sites = site_configuration['configurationValue']
  return sites