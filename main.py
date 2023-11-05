from libraries.pararius_alert import ParsePage
import PySimpleGUI as sg

def store_last_session_data(searchResults):
    with open('previousSearchResults.txt', 'w') as file:
        file.write(searchResults)

def main():
    sg.theme('SystemDefaultForReal')

    url_input = sg.InputText(key='-URL-', size=(60, 1))
    token_input = sg.InputText(key='-PHONE-', size=(60, 1))
    
    # # Load the saved phone number from a text file if it exists
    # try:
    #     with open('phone_number.txt', 'r') as file:
    #         phone = file.read()
    #         phone_input.update(phone)
    # except FileNotFoundError:
    #     phone = ''

    parseLayout = [
        [sg.Text('Enter URL:')],
        [url_input],
        [sg.Button('Parse', key='-PARSE-')],
        [sg.Image(data=sg.DEFAULT_BASE64_LOADING_GIF, key='-LOADING-', visible=False)],
        [sg.Button('Cancel')]
    ]

    telegramLayout = [
        [sg.Text('To setup your phone to receive notifications form the app follow the next steps:')],
        [sg.Text('1. Go to https://telegram.me/BotFather and send the message "/newbot" to the chat')],
        [sg.Text('2. Open the terminal and type "telegram-send --configure"')],
        [sg.Text('If the system does not recognise the command add your Python\\Script to PATH')],
        [sg.Text('3. Copy and paste the token you received from BotFather in the terminal')],
        [sg.Text('4. Now you will receive a notification every time the parser detects a new accomodation')],
        [sg.Text('Please visit the project\'s github page or the About section in the app to learn more about the app and it\'s limitations')]
    ]

    aboutLayout = [
        [sg.Text('TODO About page')]
    ]

    layout = [[sg.TabGroup([[  sg.Tab('Parse', parseLayout),
                               sg.Tab('How to setup Telegram', telegramLayout),
                               sg.Tab('About', aboutLayout)
                            ]], key='-TAB GROUP-', expand_x=True, expand_y=True),

               ]]
    

    window = sg.Window('Pararius.nl Alert ', layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break

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

