import json
import requests


def get_friends_and_family(session_id, headers):
    cookies = {
        'sessionid': session_id,
    }
    response = requests.get(
        'https://smp.eu-west-1.service.3ddigitalvenue.com/friends-family/customer/associations/',
        cookies=cookies,
        headers=headers,
    )
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        get_friends_and_family(session_id, headers)
