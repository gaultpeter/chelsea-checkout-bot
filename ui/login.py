import json
import PySimpleGUI as sg
from backend.login import post_login


def login_window():
    email_input = [sg.Text("Email: ", size=(8, 0)),
                   sg.InputText(key="-EMAIL-", focus=True, default_text="")]

    password_input = [sg.Text("Password: ", size=(8, 0)),
                      sg.InputText(password_char='*', key="-PASSWORD-", default_text="")]

    login_button = [sg.Button(button_text='Login', key="-LOGIN-", bind_return_key=True)]

    login_form_column = [email_input, password_input, login_button]

    layout = [[sg.Text("Please enter your Chelsea login details")],
              [sg.Column(login_form_column, element_justification="right")]]

    # Create the window
    window = sg.Window("Chelsea ticket bot", layout, icon="../resources/icon.ico")

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "-LOGIN-":
            email = values.get("-EMAIL-")
            password = values.get("-PASSWORD-")
            with open("../resources/headers.json", "r") as headers_file:
                headers = json.load(headers_file)
            login_details = json.dumps({"username": email, "password": password})
            login_response = handle_login(login_details, headers, 0)
            if login_response == "Error":
                return "Error"
            if login_response:
                csrf = login_response[0].get("csrf")
                session_id = login_response[1].get("set-cookie")
                headers['X-CSRFTOKEN'] = csrf
                headers['Cookie'] = session_id
                window.close()
                return csrf, session_id, headers, login_response
        if event == sg.WIN_CLOSED:
            break
    window.close()


def handle_login(login_details, headers, error_count):
    response = post_login(login_details, headers)
    status_code = response.status_code
    if error_count < 100:
        if status_code == 200:
            return json.loads(response.text), response.headers
        else:
            if status_code == 401:
                sg.Popup('Incorrect login details provided')
            else:
                error_count = error_count + 1
                return handle_login(login_details, headers, error_count)
    else:
        return "Error"
