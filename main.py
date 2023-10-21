# from libraries.pararius_alert import ParsePage

# import PySimpleGUI as sg

# sg.theme('DarkAmber')   # Add a touch of color
# # All the stuff inside your window.
# layout = [  [sg.Text('Some text on Row 1'), sg.InputText()],
#             [sg.Text('Enter something on Row 2'), sg.InputText()],
#             [sg.Button('Ok'), sg.Button('Cancel')] ]

# # Create the Window
# window = sg.Window('Window Title', layout)
# # Event Loop to process "events" and get the "values" of the inputs
# while True:
#     event, values = window.read()
#     if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
#         break
#     print('You entered ', values[0])

# window.close()

from libraries.pararius_alert import ParsePage
import PySimpleGUI as sg

def main():
    sg.theme('LightGrey6')

    url_input = sg.InputText(key='-URL-', size=(30, 1))
    phone_input = sg.InputText(key='-PHONE-', size=(15, 1))
    
    layout = [
        [sg.Text('Enter URL:')],
        [url_input],
        [sg.Text('Enter Phone Number:')],
        [phone_input],
        [sg.Button('Setup Telegram', key='-SETUP_TELEGRAM-')],
        [sg.Button('Parse', key='-PARSE-')],
        [sg.Image(data=sg.DEFAULT_BASE64_LOADING_GIF, key='-LOADING-', visible=False)],
        [sg.Button('Cancel')]
    ]

    window = sg.Window('Simple GUI', layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        if event == '-SETUP_TELEGRAM-':
            # Show instructions for setting up Telegram
            sg.popup('Lorem Ipsum for Telegram Setup Instructions')
        if event == '-PARSE-':
            # Show loading icon
            window['-LOADING-'].update(visible=True)
            window.refresh()

            # Hide loading icon
            # window['-LOADING-'].update(visible=False)
            # window.refresh()

            # Perform parsing here (you can replace this with your actual parsing function)
            url = values['-URL-']
            phone = values['-PHONE-']
            parse_result = ParsePage(url)

            # Show the parsing result in a popup (replace with your specific output)
            sg.popup(f'Parsing Result: {parse_result}')

    window.close()

if __name__ == '__main__':
    main()

