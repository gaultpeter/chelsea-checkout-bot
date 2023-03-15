import PySimpleGUI as sg

def friends_and_family_selection_window(accounts):
    account_checkboxes = [[sg.Checkbox(account['name'], key=f"-{account['account_id']}-", enable_events=True)] for
                          account in accounts]

    # Determine the height of the column based on the number of accounts
    num_accounts = len(accounts)
    col_height = min(num_accounts * 30, 200)

    layout = [[sg.Text('Please select the accounts to purchase for:')],
              [sg.Column(account_checkboxes, size=(400, col_height))]]

    # Add row for each account with dropdown for ticket type selection
    for account in accounts:
        layout.append([sg.Text('Select ticket type for this account:', visible=False, key=f"-{account['account_id']}_text-")])
        layout.append([sg.Frame(title=account['name'], layout=[
                        [sg.Combo(['ADULT', 'JUNIOR', 'SENIOR'], default_value='ADULT', size=(15,1), key=f"-{account['account_id']}_ticket_type-")]],
                        key=f"-{account['account_id']}_frame-", visible=False)])

    layout.append([sg.Button('Submit', disabled=True, key="-SUBMIT-")])

    window = sg.Window('Chelsea ticket bot', layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        # Show/hide the ticket type frames and text based on checkbox status
        for account in accounts:
            if values.get(f"-{account['account_id']}-"):
                window[f"-{account['account_id']}_frame-"].update(visible=True)
                window[f"-{account['account_id']}_text-"].update(visible=True)
            else:
                window[f"-{account['account_id']}_frame-"].update(visible=False)
                window[f"-{account['account_id']}_text-"].update(visible=False)

        # Extract the selected account IDs and ticket types
        selected_accounts = []
        for account in accounts:
            if values.get(f"-{account['account_id']}-"):
                selected_accounts.append({'account_id': account['account_id'], 'ticket_type': values.get(f"-{account['account_id']}_ticket_type-")})

        if len(selected_accounts) > 0:
            window["-SUBMIT-"].update(disabled=False)

        if event == '-SUBMIT-':
            # Check that at least one account was selected
            if selected_accounts:
                window.close()
                return selected_accounts
        if event == sg.WIN_CLOSED:
            break

    window.close()
