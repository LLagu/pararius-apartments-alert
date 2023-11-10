from threading import Thread
from libraries.pararius_alert import ParsePage
from libraries.file_management import *
import PySimpleGUI as sg

def main():
    sg.theme('SystemDefaultForReal')

    url_input = sg.InputText(key='-URL-', size=(60, 1))

    parseLayout = [
        [sg.Text('Enter URL:')],
        [url_input],
        [sg.Button('Parse', key='-PARSE-')],
        [sg.Image(data=sg.DEFAULT_BASE64_LOADING_GIF, key='-LOADING-', visible=False)],
        [sg.Multiline(size=(60,15), font='Courier 8', expand_x=True, expand_y=True, write_only=True,
                                    reroute_stdout=True, reroute_stderr=True, echo_stdout_stderr=True, autoscroll=True, auto_refresh=True)],
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

    thread = None
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            if thread is not None:
                thread._stop()
            break

        if event == '-PARSE-':
            print("Parsing started")

            previousUrl = loadFileContent("previousUrl.txt")
            if values['-URL-'] == '' and previousUrl != '':
                print("Using the url from the previous session")
                url_input.update(loadFileContent("previousUrl.txt"))
                url = previousUrl
            else:
                url = values['-URL-']
                storeFile('previousUrl.txt', url)

            if thread is None:
                thread = Thread(target=ParsePage, args=(url,))
                thread.daemon = True
                thread.start()
            
    window.close()

if __name__ == '__main__':
    main()

