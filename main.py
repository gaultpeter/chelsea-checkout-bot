import json
import time
import concurrent.futures

from events import handle_get_events
from login import handle_login
from checkout import start_checkout


def get_events():
    with open("./resources/headers.json", "r") as headers_file:
        headers = json.load(headers_file)
    with open("resources/login_details.json", "r") as login_details_file:
        data = json.load(login_details_file)
        login_details = json.dumps(data)
    login_response = handle_login(login_details, headers)
    csrf = login_response[0].get("csrf")
    session_id = login_response[1].get("set-cookie")
    headers['X-CSRFTOKEN'] = csrf
    headers['Cookie'] = session_id
    events = handle_get_events(headers)
    for event in events:
        print(event['id'], event['name'])


def start_script():
    with open("./resources/headers.json", "r") as headers_file:
        headers = json.load(headers_file)
    with open("resources/login_details.json", "r") as login_details_file:
        data = json.load(login_details_file)
        login_details = json.dumps(data)
    login_response = handle_login(login_details, headers)
    csrf = login_response[0].get("csrf")
    session_id = login_response[1].get("set-cookie")
    headers['X-CSRFTOKEN'] = csrf
    headers['Cookie'] = session_id

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(start_checkout, session_id, event_id, headers, supporter_numbers,
                                   csrf, login_response)
                   for _ in
                   range(num_of_attempts)]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result == "success":
                break


if __name__ == '__main__':

    get_events()

    on_sale_time = "09:59:59"
    supporter_numbers = []
    event_id = ""
    num_of_attempts = 1

    print("Waiting for start time: " + on_sale_time)
    while time.strftime("%H:%M:%S") < on_sale_time:
        print("Current time: " + time.strftime("%H:%M:%S"))
        time.sleep(0.5)

    start_script()
