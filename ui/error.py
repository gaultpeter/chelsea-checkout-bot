import PySimpleGUI as sg


def display_error(error):
    layout = [[sg.Text(error)], [sg.OK()]]
    window = sg.Window('Error', layout, keep_on_top=True, icon="../resources/icon.ico")
    window.close()

