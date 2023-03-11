import json

import requests

from backend.error_handler import print_response





def post_login(login_details, headers):
    return requests.post("https://smp.eu-west-1.service.3ddigitalvenue.com/friends-family/auth/login/",
                         data=login_details, headers=headers)


def get_logged(session_id, headers):
    cookies = {
        'sessionid': session_id,
    }

    response = requests.get(
        'https://smp.eu-west-1.service.3ddigitalvenue.com/friends-family/auth/logged/',
        cookies=cookies,
        headers=headers,
    )

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        get_logged(session_id, headers)
