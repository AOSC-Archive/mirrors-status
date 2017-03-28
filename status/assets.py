from flask_assets import Bundle
import requests, httplib
from datetime import datetime

common_css = Bundle(
    'css/vendor/bootstrap.min.css',
    'css/vendor/helper.css',
    'css/vendor/footable.bootstrap.min.css',
    'css/master.css',
    'css/main.css'
)

common_js = Bundle(
        'js/vendor/footable.min.js',
        'js/main.js'
)

def fetch_last_update(url):
    request = requests.get(url)
    data = request.text.strip()
    code = request.status_code
    if code == requests.codes.ok:
        if data.isdigit():
            return datetime.utcfromtimestamp(int(data)), code
        else:
            return 0, 502
    else:
        return 0, code


def update_mirror_status(mirror):
    time, code = fetch_last_update(mirror.last_update_url)
    mirror.last_fetch_status_code = code
    mirror.last_fetch_status = httplib.responses[code]
    mirror.last_fetch = datetime.utcnow()
    if code == requests.codes.ok:
        mirror.repo_last_update = time
    else:
        mirror.repo_last_update = datetime.fromtimestamp(0)

    return mirror