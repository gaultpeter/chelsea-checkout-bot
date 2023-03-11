import textwrap

import PySimpleGUI as sg


def get_id(matches, index):
    index = int(index)
    return matches[index][0]


def event_selection_window(events):
    rows = []
    top_row = ['id', 'name', 'venue', 'description']

    for chelsea_event in events:
        rows.append([chelsea_event['id'], chelsea_event['name'], chelsea_event['venue'],
                     textwrap.fill(chelsea_event['description'], 80)])

    tbl1 = sg.Table(values=rows, headings=top_row,
                    display_row_numbers=False,
                    justification='center', key='-TABLE-',
                    selected_row_colors='red on yellow',
                    enable_events=True,
                    expand_x=True,
                    expand_y=True,
                    enable_click_events=True,
                    row_height=80)
    layout = [[tbl1]]

    window = sg.Window("Chelsea ticket bot - Event selection", layout, resizable=True).finalize()
    window.maximize()
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if '+CLICKED+' in event:
            sg.popup(get_id(rows, format(event[2][0])))
    window.close()



