import PySimpleGUI as sg


def configuration_window():
    layout = [
        [sg.Text('Select number of checkouts:')],
        [sg.Spin(values=[i for i in range(1, 101)], initial_value=1, size=(8, 0))],
        [sg.Text('Enter Time (hh:mm:ss):')],
        [sg.InputText(size=(8, 0))],
        [sg.Button('Start at inputted time', key="-SUBMIT-"), sg.Button('Start now', key="-STARTNOW-")]
    ]

    window = sg.Window('Chelsea ticket bot', layout)

    while True:
        event, values = window.read()

        if event == '-SUBMIT-':
            num_checkouts = values[0]
            time_input = values[1]
            try:
                hours, minutes, seconds = time_input.split(':')
                hours = int(hours)
                minutes = int(minutes)
                seconds = int(seconds)
                if hours < 0 or hours > 23 or minutes < 0 or minutes > 59 or seconds < 0 or seconds > 59:
                    raise ValueError
                else:
                    window.close()
                    return num_checkouts, time_input
            except ValueError:
                sg.Popup('Invalid input. Please enter time in the format hh:mm:ss.')

        if event == '-STARTNOW-':
            num_checkouts = values[0]
            window.close()
            return num_checkouts, "00:00:00"
        if event == sg.WIN_CLOSED:
            break
