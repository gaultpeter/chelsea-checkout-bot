import PySimpleGUI as sg
import datetime


def wait_for_tickets_release(time_str):
    layout = [[sg.Text(f'Waiting for tickets to release at {time_str}...')],
              [sg.Text('This window will automatically proceed at the given time')]]

    window = sg.Window('Chelsea ticket bot', layout, finalize=True, icon="../resources/icon.ico")

    target_time = datetime.datetime.strptime(time_str, '%H:%M:%S')

    while True:
        current_time = datetime.datetime.now().time()
        if current_time >= target_time.time():
            window.close()
            break
        event, values = window.read(timeout=100)
        if event == sg.WINDOW_CLOSED:
            break

    window.close()
