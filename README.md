# pararius-apartments-alert
Scraping and notification application for pararius.nl

## Requirements
Python libraries: 'bs4', 'selenium', 'webdriver-manager','gtts', 'telegram_send', 'pysimplegui'

Manual install or run 
`python3 ./libraries/install_dependencies.py`

## RUN
`python3 ./main.py`

## Known issues and future updates
    - The script notifies the user when a change is detected, not necessarily when a new apartment is posted. So if an apartment is removed it will also send a notification, but that is of course a false positive. Future implementations will circumvent that.
    - No cancel button implementation yet. To parse another url simply paste the new one an the thread in the background will pick it up, but the only way to not parse is to close the app
    - Installation of the required python packages is manual or via the script mentione above. Future updates will detect missing libraries and install them automatically.
    


