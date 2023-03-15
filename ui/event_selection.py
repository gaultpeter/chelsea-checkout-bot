import PySimpleGUI as sg
import textwrap


def get_event_id(matches, index):
    if int(index) >= 0:
        index = int(index)
        return matches[index][0]


def event_selection_window(events):
    rows = []
    top_row = ['id', 'name', 'venue', 'description']


    # Calculate the maximum number of rows needed for the table
    max_rows = 1
    for chelsea_event in events:
        wrapped_description = textwrap.fill(chelsea_event['description'], width=100)
        num_rows = len(wrapped_description.split('\n'))
        if num_rows > max_rows:
            max_rows = num_rows

        rows.append([chelsea_event['id'], chelsea_event['name'], chelsea_event['venue'], wrapped_description])



    tbl1 = sg.Table(values=rows, headings=top_row,
                key='-TABLE-',
                selected_row_colors='blue on yellow',
                enable_events=True,
                enable_click_events=True,
                justification="left",
                auto_size_columns=False,
                col_widths=[5, 40, 20, 75],
                row_height=max_rows*18)

    layout = [[tbl1], [sg.Text("Match selected: "), sg.Text(key="-SELECTED-EVENT-"), sg.Button(button_text='Continue', key="-SUBMIT-", disabled=True)]]

    window = sg.Window("Chelsea ticket bot", layout, resizable=True)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if '+CLICKED+' in event:
            event_id = get_event_id(rows, format(event[2][0]))
            if event_id is not None:
                window['-SELECTED-EVENT-'].update(event_id)
                window["-SUBMIT-"].update(disabled=False)
        if event == "-SUBMIT-":
            window.close()
            return window['-SELECTED-EVENT-'].get()

        if event == sg.WIN_CLOSED:
            break
    window.close()
