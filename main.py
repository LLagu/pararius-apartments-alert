from threading import Thread
from libraries.pararius_alert import ParsePage
from libraries.file_management import *
import PySimpleGUI as sg

def main():
    sg.theme('SystemDefaultForReal')

    url_input = sg.InputText(key='-URL-', size=(60, 1))
    msg_input = [sg.Multiline(size=(60, 15), key='-MSG-', autoscroll=True, auto_refresh=True)]

    parseLayout = [
        [sg.Text('Enter URL:')],
        [url_input],
        [sg.Button('Parse', key='-PARSE-')],
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

    messageLayout = [
        [sg.Text('Insert your message to broker. It will be sent as part of the notification so that you can copy and paste it quickly.')],
        [sg.Text('Leave it blank to use the previously inserted text')],
        msg_input
    ]

    aboutLayout = [
        [sg.Text('Scraping and notification application for pararius.nl\n')],
        [sg.Text('Known issues and future updates:')],
        [sg.Text('- Installation of the required python packages is manual or via `install_dependencies.py`.\n Future updates will detect missing libraries and install them automatically.\n')],
        [sg.Text('- No cancel button implementation yet. The only way to not parse is to close the app')]
    ]

    layout = [[sg.TabGroup([[  sg.Tab('Parse', parseLayout),
                               sg.Tab('How to setup Telegram', telegramLayout),
                               sg.Tab('Custom Message', messageLayout),
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
                url_input.update(loadFileContent("previousUrl.txt"))
                url = previousUrl
            else:
                url = values['-URL-']
                storeFile('previousUrl.txt', url)

            previousMsg = loadFileContent("previousMsg.txt")
            if values['-MSG-'] == '' and previousMsg != '':
                msg_input[0].update(loadFileContent("previousMsg.txt"))
                msg = previousMsg
            else:
                msg = values['-MSG-']
                storeFile('previousMsg.txt', msg)

            if thread is None:
                thread = Thread(target=ParsePage, args=(url, msg))
                thread.daemon = True
                thread.start()
            
    window.close()

if __name__ == '__main__':
    main()

