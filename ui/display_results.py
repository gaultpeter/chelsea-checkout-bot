import PySimpleGUI as sg
import webbrowser


def create_ticket_display(results):
    columns = []
    for result in results:
        result_ = result[0]
        if 'Error' in result_:
            columns.append([sg.Text(result_)])
        else:
            seat_info = []
            for seat in result_["seats"]:
                seat_info.append([sg.Text(f"Stand: {seat['stand']} Row: {seat['row']} Seat number: {seat['number']}")])
            url = result_['url']
            layout = [
                *seat_info,
                [sg.Button('Buy', button_color=('white', 'green'), key=f'url_{url}')]
            ]
            frame = sg.Frame(title="Checkout success", layout=layout)
            columns.append([frame])
    return columns


def display_results_window(results):
    layout = [
        [sg.Text('Checkout results:')],
        [sg.Column(create_ticket_display(results), scrollable=True, size=(600, 750), vertical_scroll_only=True)]
    ]

    # Create the window
    window = sg.Window("Chelsea ticket bot", layout, icon="../resources/icon.ico")

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event.startswith('url_'):
            url = event.split('_', 1)[-1]
            webbrowser.open(url)
        if event == sg.WIN_CLOSED:
            break

    window.close()
