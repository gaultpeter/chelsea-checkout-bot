import requests

from error_handler import print_response


def handle_login(login_details, headers):
    print("Attempting login...")
    response = post_login(login_details, headers)
    if response.status_code == 200:
        print("Login success!")
        return response.json(), response.headers
    else:
        print("Retrying login...")
        print_response(response)
        return handle_login(login_details, headers)


def post_login(login_details, headers):
    return requests.post("https://smp.eu-west-1.service.3ddigitalvenue.com/friends-family/auth/login/",
                         data=login_details, headers=headers)


def get_logged(session_id, headers):
    cookies = {
        'sessionid': session_id,
    }

    return requests.get(
        'https://smp.eu-west-1.service.3ddigitalvenue.com/friends-family/auth/logged/',
        cookies=cookies,
        headers=headers,
    )
