from backend.events import get_events
from backend.friends_and_family import get_friends_and_family
from backend.login import get_logged
from backend.main import start_script
from ui.checkout_options import configuration_window
from ui.display_results import display_results_window
from ui.error import display_error
from ui.event_selection import event_selection_window
from ui.friends_and_family import friends_and_family_selection_window
from ui.login import login_window
from ui.waiting import wait_for_tickets_release

csrf = ""
session_id = ""
headers = ""
friends_and_family = []
logged = []
account_ids_and_name = []
events = []
selected_event = ""
selected_accounts = []
num_of_checkouts = 0
start_time = ""
login_response = ""
results = []
error = ""


def set_results(results_):
    global results
    results = results_


def set_selected_event(event_id):
    global selected_event
    selected_event = event_id


def set_num_of_checkouts(num):
    global num_of_checkouts
    num_of_checkouts = num


def set_selected_accounts(account_numbers):
    global selected_accounts
    selected_accounts = account_numbers


def set_login_credentials(login):
    global csrf
    global session_id
    global headers
    global login_response
    global error
    if login:
        if login == "Error":
            error = "Timed out, try again in a few minutes"
        elif len(login) > 1:
            csrf = login[0]
            session_id = login[1]
            headers = login[2]
            login_response = login[3]


def populate_accounts():
    global friends_and_family
    global logged
    global account_ids_and_name
    friends_and_family = get_friends_and_family(session_id, headers)
    logged = get_logged(session_id, headers)
    account_ids_and_name = [create_account_ids_and_name_object(True,
                                                               logged['tdc_info']['first_name']
                                                               + " " + logged['tdc_info']['last_name'],
                                                               logged['tdc_info']['id'])]
    for account in friends_and_family:
        account_ids_and_name.append(create_account_ids_and_name_object(False, account['name'], account['associate_id']))


def populate_events():
    global events
    events = get_events(session_id, headers)


def create_account_ids_and_name_object(main_account, name, account_id):
    return {"main_account": main_account, "name": name, "account_id": account_id}


def set_configuration(config):
    global num_of_checkouts
    global start_time
    if config:
        num_of_checkouts = config[0]
        start_time = config[1]


def main():
    global error
    set_login_credentials(login_window())
    if len(error) > 1:
        display_error(error)
        restart()
    else:
        populate_accounts()
        populate_events()
        if friends_and_family and logged and account_ids_and_name and events:
            set_selected_accounts(friends_and_family_selection_window(account_ids_and_name))
        else:
            restart()
        if selected_accounts:
            set_selected_event(event_selection_window(events))
        else:
            restart()
        if selected_event:
            set_configuration(configuration_window())
        else:
            restart()
        if num_of_checkouts and start_time:
            wait_for_tickets_release(start_time)
        else:
            restart()
        if session_id and selected_event and headers and selected_accounts and csrf \
                and login_response and num_of_checkouts:
            display_results_window(start_script(session_id, selected_event, headers, selected_accounts, csrf,
                                                login_response, num_of_checkouts))
        else:
            restart()


def restart():
    global error
    error = ""
    main()


if __name__ == "__main__":
    main()
    print(results)
