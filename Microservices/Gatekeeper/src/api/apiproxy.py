from flask import Blueprint
from requests import get

sites = {
    "availability": "https://availability-service-jmackie80.cloud.okteto.net/",
    "configuration": "https://configuration-service-jmackie80.cloud.okteto.net/",
    "employee": "https://employee-service-jmackie80.cloud.okteto.net/",
    "scheduling": "https://scheduling-service-jmackie80.cloud.okteto.net/",
    "calendar": "https://calendar-service-jmackie80.cloud.okteto.net/",
    "communications": "https://communications-service-jmackie80.cloud.okteto.net/"
}

bp = Blueprint('apiproxy', __name__, url_prefix='/api')

@bp.route("/", methods=['GET'])
def proxyRoot():
    return "<p>api proxy</p>"

@bp.route('/<path:api>/', defaults={'path': ''})
@bp.route('/<path:api>/<path:path>')
def proxy(api, path):
  return get(f'{sites[api]}{path}').content
