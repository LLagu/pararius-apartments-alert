def GetUserOptions(options):
    
    inputIsValid = False
    while not inputIsValid:
        firstSetup = input('Is this your first time running this script on this computer? (Y/N) ')
        if firstSetup.lower() == 'y':
            options.append(True)
            inputIsValid = True
        elif firstSetup.lower() == 'n':
            options.append(False)
            inputIsValid = True
        else:
            print('Type Y for yes or N for no')

    inputIsValid = False
    while not inputIsValid:
        newTelegramNumber = input('Do you want to setup a new phone number? (Y/N): ')
        if newTelegramNumber.lower() == 'y':
            options.append(True)
            inputIsValid = True
        elif newTelegramNumber.lower() == 'n':
            options.append(False)
            inputIsValid = True
        else:
            print('Type Y for yes or N for no')

    url = input('Paste your desired Pararius link here: ')
    options.append(str(url))