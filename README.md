# pararius-apartments-alert
Scraping and notification application for pararius.nl

## Requirements
Python libraries: 'bs4', 'selenium', 'webdriver-manager','gtts', 'telegram_send', 'pysimplegui'

Manual install or run 
`python3 ./libraries/install_dependencies.py`

## RUN
`python3 ./main.py`

## Known issues and future updates
- Installation of the required python packages is manual or via the script mentione above. Future updates will detect missing libraries and install them automatically.
- No cancel button implementation yet. To parse another url simply paste the new one an the thread in the background will pick it up, but the only way to not parse is to close the app



