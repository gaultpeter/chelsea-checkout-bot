import json
import requests

from backend.error_handler import print_response


def get_seating(event_id, session_id, headers):
    cookies = {
        'sessionid': session_id,
    }
    response = requests.get(
        'https://smp.eu-west-1.service.3ddigitalvenue.com/friends-family/events/'+event_id+'/availability/',
        cookies=cookies,
        headers=headers,
    )
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        print_response(response)
        get_seating(event_id, session_id, headers)
