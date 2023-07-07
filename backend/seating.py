import json
import requests

from backend import error_handler


def get_seating(session_id, event_id, headers):
    print("Getting stands available...")
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
        print("Error in getting stands, retrying...")
        error_handler.print_response(response)
        get_seating(session_id, event_id, headers)
