import requests
import json


def handle_get_events(headers):
    response = get_events(headers)
    if response.status_code == 200:
        return json.loads(response.text)


def get_events(headers):
    return requests.get('https://smp.eu-west-1.service.3ddigitalvenue.com/friends-family/events/', headers=headers)
