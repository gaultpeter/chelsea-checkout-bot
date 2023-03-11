from backend.events import get_events
from backend.friends_and_family import get_friends_and_family
from backend.login import get_logged
from ui.event_selection import event_selection_window
from ui.login import login_window

csrf = ""
session_id = ""
headers = ""
friends_and_family = []
logged = []
account_ids_and_name = []
events = []


def set_login_credentials(login_response):
    global csrf
    global session_id
    global headers
    csrf = login_response[0]
    session_id = login_response[1]
    headers = login_response[2]


def populate_accounts():
    global friends_and_family
    global logged
    global account_ids_and_name
    friends_and_family = get_friends_and_family(session_id, headers)
    logged = get_logged(session_id, headers)
    account_ids_and_name.append(create_account_ids_and_name_object(True,
                                                                   logged['tdc_info']['first_name']
                                                                   + " " + logged['tdc_info']['last_name'],
                                                                   logged['tdc_info']['id']))
    for account in friends_and_family:
        account_ids_and_name.append(create_account_ids_and_name_object(False, account['name'], account['associate_id']))


def populate_events():
    global events
    events = get_events(session_id, headers)


def create_account_ids_and_name_object(main_account, name, account_id):
    return {"main_account": main_account, "name": name, "account_id": account_id}


def main():
    set_login_credentials(login_window())
    populate_accounts()
    populate_events()
    event_selection_window(events)


if __name__ == "__main__":
    main()
    print(account_ids_and_name)
    print(events)
